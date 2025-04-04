# main.py - Combined API Server and Gradio UI

import gradio as gr
import uvicorn
import asyncio
import datetime
import os
import json
import re
import time
import uuid
import webbrowser
import threading
from pathlib import Path
from typing import Dict, List, Optional, Union, Literal, Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# --- Assuming app structure is accessible ---
# It might be cleaner to move agent/schema etc. to a top-level package
# For now, assume relative imports work or adjust sys.path if needed
from app.agent.manus import Manus
from app.logger import logger
from app.schema import AgentState, Message as AgentMessage, Memory

# --- Constants ---
HISTORY_DIR = Path("chatsHistory")
HOST = "127.0.0.1" # Use 127.0.0.1 for local access
PORT = 7860 # Use Gradio's default port
BASE_URL = f"http://{HOST}:{PORT}"

# --- Agent Initialization ---
agent_instance: Optional[Manus] = None
agent_initialized = False
agent_lock = asyncio.Lock() # Lock to prevent concurrent access issues with the single agent

async def initialize_agent_once():
    """Initialize the Manus agent instance if not already done."""
    global agent_instance, agent_initialized
    # No lock needed here as it's called once before server starts
    if not agent_initialized:
        logger.info("Initializing Manus agent...")
        try:
            agent_instance = Manus()
            agent_instance.state = AgentState.IDLE
            agent_initialized = True
            logger.info("Manus agent initialized.")
        except Exception as e:
             logger.error(f"Failed to initialize Manus agent: {e}", exc_info=True)
             # Exit if agent fails to initialize? Or let server start but API fail?
             # Let's exit for now.
             print(f"\nFATAL: Failed to initialize Manus agent: {e}\n")
             exit(1) # Exit the script

    if not agent_instance:
         print("\nFATAL: Agent instance is None after initialization attempt.\n")
         exit(1)
    return agent_instance

# --- File Persistence Helper Functions ---
def sanitize_filename(name: str) -> str:
    """Removes invalid characters for filenames."""
    name = re.sub(r'[^\w\s-]', '', name).strip()
    # Replace multiple spaces/hyphens with single underscore
    name = re.sub(r'[\s-]+', '_', name)
    if not name:
        name = "untitled_chat"
    # Limit length? e.g., name = name[:100]
    return name

def save_session_file(session_id: str, messages: List[AgentMessage]):
    """Saves a session's messages to a JSON file."""
    try:
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        filename = sanitize_filename(session_id) + ".json"
        filepath = HISTORY_DIR / filename
        # Use Pydantic's model_dump for proper serialization, including datetimes etc.
        messages_as_dicts = [msg.model_dump(mode='json') for msg in messages]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(messages_as_dicts, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved session '{session_id}' to {filepath}")
    except Exception as e:
        logger.error(f"Error saving session '{session_id}' to file: {e}", exc_info=True)
        # Cannot use gr.Warning here as it's outside Gradio context
        print(f"Warning: Failed to save session '{session_id}': {e}")

def load_session_data() -> Dict[str, List[AgentMessage]]:
    """Loads all session data from the history directory."""
    sessions = {}
    HISTORY_DIR.mkdir(parents=True, exist_ok=True) # Ensure directory exists before reading
    try:
        # Sort files based on the numeric part of "Chat X" or alphabetically otherwise
        def sort_key(p: Path):
            name = p.stem
            if name.startswith("Chat ") and len(name.split(" ")) > 1 and name.split(" ")[1].isdigit():
                try: return (0, int(name.split(" ")[1])) # Prioritize "Chat X" numerically
                except ValueError: return (1, name) # Fallback for malformed "Chat X"
            return (1, name) # Sort others alphabetically
        session_files = sorted(HISTORY_DIR.glob("*.json"), key=sort_key)
        for filepath in session_files:
            # Use the actual filename stem as the session ID key
            session_id_from_filename = filepath.stem
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    messages_data_str = f.read()
                    if not messages_data_str.strip(): messages = []
                    else:
                         messages_data = json.loads(messages_data_str)
                         # Use model_validate for each dict in the list
                         messages = [AgentMessage.model_validate(msg_data) for msg_data in messages_data]
                    sessions[session_id_from_filename] = messages
                logger.debug(f"Loaded session '{session_id_from_filename}' from {filepath}")
            except Exception as e: logger.error(f"Error loading session file {filepath}: {e}", exc_info=True)
    except Exception as e: logger.error(f"Error reading history directory '{HISTORY_DIR}': {e}", exc_info=True)

    if not sessions:
        logger.info("No chat history found. Starting with 'Chat 1'.")
        default_session_id = "Chat 1"
        sessions[default_session_id] = []
        save_session_file(default_session_id, [])
    logger.info(f"Loaded {len(sessions)} sessions.")
    return sessions

def delete_session_file(session_id: str):
    """Deletes the JSON file for a given session ID."""
    try:
        filename = sanitize_filename(session_id) + ".json"
        filepath = HISTORY_DIR / filename
        if filepath.exists():
            filepath.unlink()
            logger.info(f"Deleted session file: {filepath}")
        else: logger.warning(f"Attempted to delete non-existent session file: {filepath}")
    except Exception as e: logger.error(f"Error deleting session file for '{session_id}': {e}", exc_info=True)

def rename_session_file(old_session_id: str, new_session_id: str):
    """Renames the JSON file for a session."""
    try:
        old_filename = sanitize_filename(old_session_id) + ".json"
        new_filename = sanitize_filename(new_session_id) + ".json"
        old_filepath = HISTORY_DIR / old_filename
        new_filepath = HISTORY_DIR / new_filename
        if old_filepath.exists():
            if not new_filepath.exists(): old_filepath.rename(new_filepath); logger.info(f"Renamed session file from {old_filename} to {new_filename}")
            else: logger.error(f"Rename failed: Target file '{new_filename}' already exists.")
        else: logger.warning(f"Attempted to rename non-existent session file: {old_filepath}")
    except Exception as e: logger.error(f"Error renaming session file from '{old_session_id}' to '{new_session_id}': {e}", exc_info=True)

# --- Gradio UI Helper Function ---
def format_history_for_chatbot(messages: list[AgentMessage]) -> list[list[str | None]]:
    """Converts message list to Gradio Chatbot list-of-lists format."""
    chatbot_history = []
    user_msg_content = None
    assistant_msg_parts = []
    for msg in messages:
        if msg.role == "user":
            if assistant_msg_parts:
                 if user_msg_content is not None: chatbot_history.append([user_msg_content, "\n\n".join(assistant_msg_parts)])
                 else: logger.warning("Found assistant messages without preceding user message."); chatbot_history.append([None, "\n\n".join(assistant_msg_parts)])
                 assistant_msg_parts = []
            user_msg_content = msg.content
        elif msg.role == "assistant":
             thought_prefix = "**Assistant Thoughts/Plan:**\n" if msg.content else ""
             tool_calls_str = ""
             if msg.tool_calls: tool_calls_str = "\n**Requesting Tools:**\n" + "\n".join([f"- `{tc.function.name}`(`{tc.function.arguments or '{}'}`)" for tc in msg.tool_calls])
             assistant_msg_parts.append(f"{thought_prefix}{msg.content or ''}{tool_calls_str}")
        elif msg.role == "tool":
             tool_content = str(msg.content); is_code = "```" in tool_content or "\n" in tool_content.strip(); formatted_content = f"```\n{tool_content}\n```" if is_code else tool_content
             if len(tool_content) > 500 and "..." not in tool_content[-10:]: formatted_content = formatted_content[:500] + "..."
             assistant_msg_parts.append(f"**Tool Result (`{msg.name}`):**\n{formatted_content}")
        elif msg.role == "system": assistant_msg_parts.append(f"**System Note:**\n{msg.content}")
    if user_msg_content is not None: chatbot_history.append([user_msg_content, "\n\n".join(assistant_msg_parts) if assistant_msg_parts else None])
    elif assistant_msg_parts: chatbot_history.append([None, "\n\n".join(assistant_msg_parts)])
    return chatbot_history

# --- Gradio Session Management Functions ---
def rename_chat_session_ui(session_id: str, new_name: str, session_data: dict):
    """UI handler for renaming session."""
    if not session_id or session_id not in session_data: gr.Warning(f"Session '{session_id}' not found!"); return session_id, session_data, gr.Radio(choices=list(session_data.keys()), value=session_id), gr.Textbox(value="")
    if not new_name or not new_name.strip(): gr.Warning("New name cannot be empty!"); return session_id, session_data, gr.Radio(choices=list(session_data.keys()), value=session_id), gr.Textbox(value="")
    new_name = new_name.strip()
    if new_name == session_id: return session_id, session_data, gr.Radio(choices=list(session_data.keys()), value=session_id), gr.Textbox(value="")
    if new_name in session_data: gr.Warning(f"Name '{new_name}' already exists!"); return session_id, session_data, gr.Radio(choices=list(session_data.keys()), value=session_id), gr.Textbox(value="")

    logger.info(f"Renaming session '{session_id}' to '{new_name}'")
    rename_session_file(session_id, new_name) # Rename file
    session_data[new_name] = session_data.pop(session_id) # Rename in memory

    updated_choices = list(session_data.keys())
    updated_choices.sort(key=lambda x: int(x.split(" ")[1]) if x.startswith("Chat ") and len(x.split(" ")) > 1 and x.split(" ")[1].isdigit() else float('inf'))
    return new_name, session_data, gr.Radio(choices=updated_choices, value=new_name), gr.Textbox(value="")

def delete_chat_session_ui(session_id: str, session_data: dict):
    """UI handler for deleting session."""
    if not session_id or session_id not in session_data: gr.Warning(f"Session '{session_id}' not found!"); return session_id, session_data, gr.Radio(choices=list(session_data.keys()), value=session_id), []
    if len(session_data) <= 1: gr.Warning("Cannot delete the last chat session!"); return session_id, session_data, gr.Radio(choices=list(session_data.keys()), value=session_id), format_history_for_chatbot(session_data.get(session_id, []))

    logger.info(f"Deleting session '{session_id}'")
    delete_session_file(session_id) # Delete file
    del session_data[session_id] # Delete from memory

    updated_choices = list(session_data.keys())
    updated_choices.sort(key=lambda x: int(x.split(" ")[1]) if x.startswith("Chat ") and len(x.split(" ")) > 1 and x.split(" ")[1].isdigit() else float('inf'))
    new_active_session_id = updated_choices[-1] if updated_choices else None
    new_chatbot_history = format_history_for_chatbot(session_data.get(new_active_session_id, [])) if new_active_session_id else []
    return new_active_session_id, session_data, gr.Radio(choices=updated_choices, value=new_active_session_id), new_chatbot_history

def start_new_chat_session_ui(session_data: dict):
    """UI handler for starting new session."""
    max_num = 0
    for key in session_data.keys():
        if key.startswith("Chat "):
            try:
                parts = key.split(" ")
                if len(parts) > 1 and parts[1].isdigit():
                    num = int(parts[1])
                    if num > max_num:
                        max_num = num
            except ValueError:
                continue # Ignore keys not matching the pattern
    new_session_id = f"Chat {max_num + 1}"

    session_data[new_session_id] = []
    save_session_file(new_session_id, [])
    logger.info(f"Started and saved new chat session: {new_session_id}")

    updated_choices = list(session_data.keys())
    updated_choices.sort(key=lambda x: int(x.split(" ")[1]) if x.startswith("Chat ") and len(x.split(" ")) > 1 and x.split(" ")[1].isdigit() else float('inf'))
    return new_session_id, session_data, [], gr.Radio(choices=updated_choices, value=new_session_id)

def load_chat_session_ui(session_id: str, session_data: dict):
    """UI handler for loading session."""
    if not session_id or session_id not in session_data:
        logger.warning(f"Attempted to load invalid session ID: {session_id}")
        if session_data:
             sorted_keys = list(session_data.keys()); sorted_keys.sort(key=lambda x: int(x.split(" ")[1]) if x.startswith("Chat ") and len(x.split(" ")) > 1 and x.split(" ")[1].isdigit() else float('inf'))
             latest_session_id = sorted_keys[-1] if sorted_keys else None
             if latest_session_id: logger.warning(f"Falling back to latest session: {latest_session_id}"); return format_history_for_chatbot(session_data.get(latest_session_id, [])), latest_session_id, gr.Radio(value=latest_session_id)
        return [], None, gr.Radio(value=None)
    logger.info(f"Loading chat session: {session_id}")
    history_messages = session_data.get(session_id, [])
    formatted_history = format_history_for_chatbot(history_messages)
    return formatted_history, session_id, gr.Radio(value=session_id)

# --- Gradio Chat Execution Logic ---
async def run_chat_ui(message: str, chat_history_formatted: list[list[str | None]], active_session_id: str, session_data: dict):
    """UI handler for running chat, streaming, and saving."""
    if not active_session_id: yield chat_history_formatted + [[message, "Error: No active session selected."]], session_data; return
    agent = await initialize_agent_once()
    if not agent: yield chat_history_formatted + [[message, "Error: Agent not initialized"]], session_data; return

    async with agent_lock: # Use lock for agent execution
        current_history_messages = session_data.get(active_session_id, [])
        agent.memory.messages = current_history_messages.copy()
        agent.state = AgentState.IDLE; agent.current_step = 0
        logger.info(f"UI: Loaded {len(agent.memory.messages)} messages for session {active_session_id}.")

        chat_history_formatted.append([message, None])
        yield chat_history_formatted, session_data

        assistant_response_stream = ""
        try:
            async for update in agent.run(request=message):
                assistant_response_stream = update
                if chat_history_formatted: chat_history_formatted[-1][1] = assistant_response_stream
                yield chat_history_formatted, session_data
            if agent.state == AgentState.FINISHED:
                success_message = "<br><br><span style='color:green; font-weight:bold;'>✅ Succeed / 完成</span>"
                if chat_history_formatted: chat_history_formatted[-1][1] = (chat_history_formatted[-1][1] or "") + success_message
                logger.info("UI: Appended success message.")
                yield chat_history_formatted, session_data
        except Exception as e:
            logger.error(f"UI: Error during agent run for session {active_session_id}: {e}", exc_info=True)
            error_msg = f"An error occurred: {str(e)}"
            if chat_history_formatted: chat_history_formatted[-1][1] = (chat_history_formatted[-1][1] or "") + f"\n\n**Error:** {error_msg}"
            if agent: agent.state = AgentState.ERROR
            yield chat_history_formatted, session_data
        finally:
            if agent and agent.memory:
                 if active_session_id in session_data:
                      session_data[active_session_id] = agent.memory.messages.copy()
                      save_session_file(active_session_id, session_data[active_session_id])
                      logger.info(f"UI: Saved final state for session {active_session_id}")
                 else: logger.warning(f"UI: Session '{active_session_id}' was deleted during run, cannot save.")
            else: logger.error("UI: Agent or memory not available for saving.")
            yield chat_history_formatted, session_data

# --- OpenAI Compatible API Models ---
class ChatMessage(BaseModel): role: Literal["system", "user", "assistant", "tool"]; content: Optional[str] = None
class ChatCompletionRequest(BaseModel): model: str; messages: List[ChatMessage]; stream: Optional[bool] = False
class ChoiceDelta(BaseModel): role: Optional[Literal["assistant"]] = None; content: Optional[str] = None
class ChatCompletionChunkChoice(BaseModel): index: int = 0; delta: ChoiceDelta; finish_reason: Optional[Literal["stop", "length", "tool_calls", "error"]] = None
class ChatCompletionChunk(BaseModel): id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex}"); object: str = "chat.completion.chunk"; created: int = Field(default_factory=lambda: int(time.time())); model: str; choices: List[ChatCompletionChunkChoice]
class ChatCompletionChoice(BaseModel): index: int = 0; message: ChatMessage; finish_reason: Optional[Literal["stop", "length", "tool_calls", "error"]] = None
class Usage(BaseModel): prompt_tokens: Optional[int] = None; completion_tokens: Optional[int] = None; total_tokens: Optional[int] = None
class ChatCompletionResponse(BaseModel): id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex}"); object: str = "chat.completion"; created: int = Field(default_factory=lambda: int(time.time())); model: str; choices: List[ChatCompletionChoice]; usage: Optional[Usage] = None

# --- FastAPI App and API Endpoint ---
app = FastAPI(title="OpenManus API & UI Server")

@app.post("/v1/chat/completions", tags=["Chat"])
async def chat_completions_api(request: ChatCompletionRequest):
    """OpenAI-compatible Chat Completion endpoint."""
    agent = await initialize_agent_once()
    async with agent_lock: # Use lock for exclusive agent access
        agent.memory.messages = []; agent.state = AgentState.IDLE; agent.current_step = 0
        for msg in request.messages: agent.memory.add_message(AgentMessage(role=msg.role, content=msg.content or ""))
        logger.info(f"API: Processing request for model '{request.model}'. Stream: {request.stream}")
        last_user_message = agent.memory.messages[-1].content if agent.memory.messages and agent.memory.messages[-1].role == "user" else ""
        request_id = f"chatcmpl-{uuid.uuid4().hex}"

        if request.stream:
            async def stream_generator():
                previous_content = ""; final_finish_reason = "stop"; chunk_model_name = request.model; yielded_initial = False
                try:
                    async for update in agent.run(request=last_user_message):
                        delta_content = update[len(previous_content):]; previous_content = update
                        delta = ChoiceDelta()
                        if not yielded_initial and delta_content: delta.role = "assistant"; yielded_initial = True
                        if delta_content:
                            delta.content = delta_content
                            chunk = ChatCompletionChunk(id=request_id, model=chunk_model_name, choices=[ChatCompletionChunkChoice(delta=delta)])
                            yield f"data: {chunk.model_dump_json(exclude_none=True)}\n\n"; await asyncio.sleep(0.01)
                    if agent.state == AgentState.ERROR: final_finish_reason = "error"
                    elif agent.current_step >= agent.max_steps: final_finish_reason = "length"
                except Exception as e: logger.error(f"API Stream Error: {e}", exc_info=True); final_finish_reason = "error"
                finally:
                    final_chunk = ChatCompletionChunk(id=request_id, model=chunk_model_name, choices=[ChatCompletionChunkChoice(delta=ChoiceDelta(), finish_reason=final_finish_reason)])
                    yield f"data: {final_chunk.model_dump_json(exclude_none=True)}\n\n"; yield "data: [DONE]\n\n"
                    logger.info(f"API Stream finished for {request_id} with reason: {final_finish_reason}")
            return StreamingResponse(stream_generator(), media_type="text/event-stream")
        else: # Non-streaming
            final_response_content = ""; final_finish_reason = "stop"
            try:
                async for update in agent.run(request=last_user_message): final_response_content = update
                if agent.state == AgentState.ERROR: final_finish_reason = "error"
                elif agent.current_step >= agent.max_steps: final_finish_reason = "length"
            except Exception as e: logger.error(f"API Non-Stream Error: {e}", exc_info=True); raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")
            response = ChatCompletionResponse(id=request_id, model=request.model, choices=[ChatCompletionChoice(message=ChatMessage(role="assistant", content=final_response_content), finish_reason=final_finish_reason)])
            logger.info(f"API Non-Stream request {request_id} completed with reason: {final_finish_reason}")
            return response

# --- Build Gradio UI ---
initial_session_data = load_session_data()
initial_session_ids = list(initial_session_data.keys())
initial_session_ids.sort(key=lambda x: int(x.split(" ")[1]) if x.startswith("Chat ") and len(x.split(" ")) > 1 and x.split(" ")[1].isdigit() else float('inf'))
active_session_id_on_load = initial_session_ids[-1] if initial_session_ids else "Chat 1"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    session_state = gr.State(initial_session_data)
    active_session_id_state = gr.State(active_session_id_on_load)
    with gr.Row():
        with gr.Column(scale=1, min_width=250):
            gr.Markdown("## Chat History")
            new_chat_btn = gr.Button("➕ New Chat")
            history_radio = gr.Radio(label="Sessions", choices=initial_session_ids, value=active_session_id_on_load, type="value")
            gr.Markdown("### Manage Selected Session")
            rename_textbox = gr.Textbox(label="New Name", placeholder="Enter new name...", scale=3, show_label=False)
            with gr.Row(): rename_btn = gr.Button("Rename", scale=1); delete_btn = gr.Button("Delete", scale=1, variant="stop")
        with gr.Column(scale=4):
            # Load initial chat history for the active session - Correct Indentation
            initial_chatbot_history = format_history_for_chatbot(initial_session_data.get(active_session_id_on_load, []))
            chatbot = gr.Chatbot(
                label="OpenManus Agent",
                value=initial_chatbot_history, # Set initial value
                render_markdown=True,
                height=700,
                show_label=False,
                bubble_full_width=False
            )
            with gr.Row(): # Correct Indentation
                 msg_textbox = gr.Textbox(placeholder="Enter your request...", scale=7, container=False, show_label=False)
                 send_btn = gr.Button("Send", scale=1, variant="primary", min_width=100)
    # --- Define Gradio Interactions ---
    submit_event = msg_textbox.submit(fn=run_chat_ui, inputs=[msg_textbox, chatbot, active_session_id_state, session_state], outputs=[chatbot, session_state])
    submit_event.then(lambda: gr.Textbox(value=""), outputs=[msg_textbox])
    click_event = send_btn.click(fn=run_chat_ui, inputs=[msg_textbox, chatbot, active_session_id_state, session_state], outputs=[chatbot, session_state])
    click_event.then(lambda: gr.Textbox(value=""), outputs=[msg_textbox])
    new_chat_btn.click(fn=start_new_chat_session_ui, inputs=[session_state], outputs=[active_session_id_state, session_state, chatbot, history_radio])
    history_radio.change(fn=load_chat_session_ui, inputs=[history_radio, session_state], outputs=[chatbot, active_session_id_state, history_radio])
    rename_btn.click(fn=rename_chat_session_ui, inputs=[active_session_id_state, rename_textbox, session_state], outputs=[active_session_id_state, session_state, history_radio, rename_textbox])
    delete_btn.click(fn=delete_chat_session_ui, inputs=[active_session_id_state, session_state], outputs=[active_session_id_state, session_state, history_radio, chatbot])

# --- Mount Gradio App onto FastAPI ---
# Mount after all routes are defined on 'app'
app = gr.mount_gradio_app(app, demo, path="/")

# --- Function to Open Browser ---
def open_browser():
    """Opens the browser to the Gradio UI."""
    try:
        logger.info(f"Attempting to open browser at {BASE_URL}")
        webbrowser.open(BASE_URL)
        logger.info(f"Browser open command issued for {BASE_URL}")
    except Exception as e:
        logger.error(f"Failed to open browser automatically: {e}")
        print(f"\nCould not open browser automatically. Please navigate to {BASE_URL}\n")

# --- Main Execution ---
if __name__ == "__main__":
    # Initialize agent before starting server
    # Use asyncio.run for the async init function
    try:
        asyncio.run(initialize_agent_once())
    except SystemExit: # Catch exit if agent init fails
        exit(1)
    except Exception as e:
        print(f"\nFATAL: Unexpected error during agent initialization: {e}\n")
        exit(1)


    # Use threading.Timer to open browser after a delay
    # This allows Uvicorn to start first
    # Ensure the URL is correct (using HOST and PORT constants)
    threading.Timer(1.5, open_browser).start() # Delay of 1.5 seconds

    logger.info(f"Starting server on {BASE_URL}")
    logger.info(f"Gradio UI available at {BASE_URL}/")
    logger.info(f"API Docs available at {BASE_URL}/docs")
    logger.info(f"OpenAI compatible API endpoint at {BASE_URL}/v1/chat/completions")

    # Run Uvicorn server programmatically
    config = uvicorn.Config(app, host=HOST, port=PORT, log_level="info")
    server = uvicorn.Server(config)
    # Use server.run() which is synchronous in this context
    server.run()
    # uvicorn.run(app, host=HOST, port=PORT) # This also works but might block differently
