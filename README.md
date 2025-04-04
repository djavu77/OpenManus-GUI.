<p align="center">
  <img src="assets/logo.jpg" width="200"/>
</p>

<p align="center">
  <strong>OpenManus: Your Versatile AI Agent Framework</strong>
</p>

<p align="center">
  [English](README.md) | <a href="README_zh.md">中文</a> | <a href="README_ko.md">한국어</a> | <a href="README_ja.md">日本語</a>
</p>

<p align="center">
  <a href="https://github.com/mannaandpoem/OpenManus/stargazers"><img src="https://img.shields.io/github/stars/mannaandpoem/OpenManus?style=social" alt="GitHub stars"></a>
  &amp;ensp;
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  &amp;ensp;
  <a href="https://discord.gg/DYn29wFk9z"><img src="https://dcbadge.vercel.app/api/server/DYn29wFk9z?style=flat" alt="Discord Follow"></a>
  &amp;ensp;
  <a href="https://huggingface.co/spaces/lyh-917/OpenManusDemo"><img src="https://img.shields.io/badge/Demo-Hugging%20Face-yellow" alt="Demo"></a>
</p>

---

## 👋 Introduction

Inspired by Manus, **OpenManus** provides an open-source framework for building versatile AI agents capable of tackling various tasks. We aim to empower users to bring their ideas to life without needing an invitation code.

This version integrates a user-friendly **Web UI** (built with Gradio) for interactive chat and session management, alongside an **OpenAI-compatible API** (built with FastAPI) for programmatic access.

Our team members [@Xinbin Liang](https://github.com/mannaandpoem) and [@Jinyu Xiang](https://github.com/XiangJinyu) (core authors), along with [@Zhaoyang Yu](https://github.com/MoshiQAQ), [@Jiayi Zhang](https://github.com/didiforgithub), and [@Sirui Hong](https://github.com/stellaHSR), from the [@MetaGPT](https://github.com/geekan/MetaGPT) team, initiated this project and continue its development. We welcome suggestions, contributions, and feedback!

## ✨ Features

*   **Multi-Turn Conversation**: Engage in extended dialogues with context retention.
*   **Web UI**: Interact with the agent through an intuitive web interface featuring:
    *   Streaming responses for real-time updates.
    *   Session management (create, rename, delete, switch conversations).
    *   Persistent chat history stored locally in the `chatsHistory/` directory.
*   **OpenAI-Compatible API**: Integrate OpenManus into your applications using the familiar OpenAI SDK format (`/v1/chat/completions` endpoint). Supports both streaming and non-streaming modes.
*   **Versatile Tools**: Equipped with tools for:
    *   Web Browsing (`BrowserUseTool`)
    *   Code Execution (Python in a sandbox environment)
    *   File Operations (String replacement editor)
    *   Web Search (Google, Bing, DuckDuckGo, Baidu)
    *   Bash Command Execution (via sandbox terminal)
*   **Extensible Framework**: Built with a clear, object-oriented structure (`BaseAgent` -> `ReActAgent` -> `ToolCallAgent` -> `BrowserAgent` -> `Manus`).

## 📸 Screenshots

**Web UI:**
![OpenManus Web UI Screenshot 1](https://github.com/Hank-Chromela/Hank-Chroela-images/blob/main/1743753144854.png?raw=true)

**Session Management:**
![OpenManus Web UI Screenshot 2](https://github.com/Hank-Chromela/Hank-Chroela-images/blob/main/1743753160804.png?raw=true)

## 🚀 Installation

We recommend using `uv` for faster installation and dependency management.

**Option 1: Using `uv` (Recommended)**

1.  Install `uv` (if you haven't already):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Or follow instructions at https://github.com/astral-sh/uv
    ```
2.  Clone the repository:
    ```bash
    git clone https://github.com/mannaandpoem/OpenManus.git
    cd OpenManus
    ```
3.  Create and activate a virtual environment:
    ```bash
    uv venv --python 3.12 # Or your preferred Python 3.10+ version
    source .venv/bin/activate  # Unix/macOS
    # .venv\Scripts\activate    # Windows
    ```
4.  Install dependencies:
    ```bash
    uv pip install -r requirements.txt
    ```

**Option 2: Using `conda`**

1.  Create and activate a conda environment:
    ```bash
    conda create -n open_manus python=3.12 -y
    conda activate open_manus
    ```
2.  Clone the repository:
    ```bash
    git clone https://github.com/mannaandpoem/OpenManus.git
    cd OpenManus
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

**Install Playwright Browsers (Required for Browser Tool)**
```bash
playwright install --with-deps
```

## ⚙️ Configuration

OpenManus requires configuration for the Large Language Model (LLM) you intend to use.

1.  Copy the example configuration file:
    ```bash
    cp config/config.example.toml config/config.toml
    ```
2.  Edit `config/config.toml` to add your API keys and customize settings (e.g., model name, base URL). The agent primarily uses the `[llm.default]` section unless specific configurations are accessed differently in the code.
    ```toml
    # Example for default OpenAI settings
    [llm.default]
    model = "gpt-4o" # Or gpt-3.5-turbo, etc.
    api_type = "openai" # or "azure", "aws"
    base_url = "https://api.openai.com/v1"
    api_key = "sk-..."  # IMPORTANT: Replace with your actual OpenAI API key
    max_tokens = 4096
    temperature = 0.0
    # api_version = "..." # Required for Azure

    # Example for a vision model (if needed separately)
    # [llm.vision]
    # model = "gpt-4o"
    # ... other settings ...
    ```
    **Note:** While the UI allows overriding these settings at runtime, the initial configuration is still loaded from this file.

## ▶️ Running the Application

Simply run the `main.py` script:

```bash
python main.py
```

This command will:
1.  Initialize the Manus agent.
2.  Start a web server hosting both the Gradio UI and the FastAPI API.
3.  Attempt to automatically open the Gradio Web UI in your default browser (usually at `http://127.0.0.1:7860`).
4.  Make the OpenAI-compatible API available at `http://127.0.0.1:7860/v1/chat/completions`.

You should see output similar to this in your terminal:
```
INFO:     Starting server on http://127.0.0.1:7860
INFO:     Gradio UI available at http://127.0.0.1:7860/
INFO:     API Docs available at http://127.0.0.1:7860/docs
INFO:     OpenAI compatible API endpoint at http://127.0.0.1:7860/v1/chat/completions
INFO:     Uvicorn running on http://127.0.0.1:7860 (Press CTRL+C to quit)
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Attempting to open browser at http://127.0.0.1:7860
INFO:     Browser open command issued for http://127.0.0.1:7860
```

## 💻 Using the Web UI

*   Navigate to `http://127.0.0.1:7860` in your browser if it didn't open automatically.
*   **Chat**: Enter your requests in the message box at the bottom and press Enter or click "Send". The agent's thoughts, tool usage, and final response will stream into the chat window.
*   **Session Management**:
    *   Use the left sidebar to manage conversations.
    *   Click "➕ New Chat" to start a fresh conversation.
    *   Select a session from the list to load its history.
    *   Use the "Manage Selected Session" section below the list to rename or delete the currently selected chat (you cannot delete the last remaining chat).
*   **Persistence**: Chat history and session names are automatically saved in the `chatsHistory/` directory as JSON files and will be reloaded when you restart the application.

## 🔌 Using the API

The server exposes an OpenAI-compatible API endpoint at `/v1/chat/completions`. You can use standard OpenAI client libraries (like the official Python `openai` library) to interact with it.

**Configuration in Client:**

*   **Base URL**: `http://127.0.0.1:7860/v1`
*   **API Key**: Any non-empty string (e.g., `"not-needed"`). The server does not validate the key.
*   **Model**: Any non-empty string (e.g., `"openmanus"`). The server uses the configured Manus agent regardless of the model name sent.

**Example using `openai` Python library:**

```python
# test_api.py
import openai

# Configure the client
client = openai.OpenAI(
    base_url="http://127.0.0.1:7860/v1",
    api_key="not-needed", # Provide a dummy key
)

# Non-streaming request
try:
    completion = client.chat.completions.create(
        model="openmanus-local", # Model name is required but ignored by server
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    print("Non-Streaming Response:")
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"API Error: {e}")

# Streaming request
try:
    stream = client.chat.completions.create(
        model="openmanus-local",
        messages=[
            {"role": "user", "content": "Explain quantum entanglement briefly."}
        ],
        stream=True
    )
    print("\nStreaming Response:")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print()
except Exception as e:
    print(f"API Streaming Error: {e}")
```

## 🙌 Contributing

We welcome contributions! Please feel free to submit issues or pull requests.

Before submitting a pull request, please ensure your changes pass pre-commit checks:
```bash
# Install pre-commit hooks (if you haven't already)
pre-commit install
# Run checks on all files
pre-commit run --all-files
```

You can also reach out via email: mannaandpoem@gmail.com

## 💬 Community

Join our community group (details/link if available, otherwise remove or update).
*(Placeholder for community link/image)*

## 🙏 Acknowledgements

Special thanks to [anthropic-computer-use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) and [browser-use](https://github.com/browser-use/browser-use) for foundational support.

We also appreciate the work from [AAAJ](https://github.com/metauto-ai/agent-as-a-judge), [MetaGPT](https://github.com/geekan/MetaGPT), [OpenHands](https://github.com/All-Hands-AI/OpenHands), and [SWE-agent](https://github.com/SWE-agent/SWE-agent).

Thanks to StepFun (阶跃星辰) for Hugging Face demo space support.

OpenManus is built by contributors from the MetaGPT community.

## 📜 Citation

If you use OpenManus in your research or work, please cite it as follows:

```bibtex
@misc{openmanus2025,
  author = {Xinbin Liang and Jinyu Xiang and Zhaoyang Yu and Jiayi Zhang and Sirui Hong and Your Name Here (if contributing)},
  title = {OpenManus: An Open-Source Framework for Versatile AI Agents with UI and API},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/mannaandpoem/OpenManus}},
}
