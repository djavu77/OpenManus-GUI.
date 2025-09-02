"""
Aba de Controle do OpenManus
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import subprocess
import json
from pathlib import Path

from ..widgets.config_editor import ConfigEditor
from services.openmanus_service import OpenManusService


class OpenManusTab(ctk.CTkFrame):
    """Aba para gerenciar OpenManus"""
    
    def __init__(self, parent, config_manager, log_manager):
        super().__init__(parent)
        
        self.config_manager = config_manager
        self.log_manager = log_manager
        self.service = OpenManusService(config_manager)
        
        self.setup_ui()
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
    
    def setup_ui(self):
        """Configurar interface da aba"""
        # Painel de controle
        self.create_control_panel()
        
        # Configurações
        self.create_config_panel()
        
        # Task Manager
        self.create_task_panel()
        
        # Agent Flow Visualizer
        self.create_flow_panel()
    
    def create_control_panel(self):
        """Criar painel de controle"""
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        control_frame.grid_columnconfigure(3, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            control_frame,
            text="Controle do OpenManus",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=4, pady=(10, 15))
        
        # Botões de controle
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="▶️ Iniciar",
            command=self.start_service,
            fg_color="green"
        )
        self.start_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="⏹️ Parar",
            command=self.stop_service,
            fg_color="red"
        )
        self.stop_btn.grid(row=1, column=1, padx=5, pady=5)
        
        self.restart_btn = ctk.CTkButton(
            control_frame,
            text="🔄 Reiniciar",
            command=self.restart_service,
            fg_color="orange"
        )
        self.restart_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Seleção de modo
        mode_label = ctk.CTkLabel(control_frame, text="Modo de Execução:")
        mode_label.grid(row=2, column=0, sticky="w", padx=5, pady=(10, 5))
        
        self.mode_var = ctk.StringVar(value="main.py")
        self.mode_combo = ctk.CTkComboBox(
            control_frame,
            values=["main.py", "run_mcp.py", "run_flow.py"],
            variable=self.mode_var
        )
        self.mode_combo.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=(10, 5))
        
        # Status atual
        self.status_label = ctk.CTkLabel(
            control_frame,
            text="Status: Parado",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=3, column=0, columnspan=4, pady=(5, 10))
    
    def create_config_panel(self):
        """Criar painel de configuração"""
        config_frame = ctk.CTkFrame(self)
        config_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(5, 10), pady=10)
        
        # Título
        title = ctk.CTkLabel(
            config_frame,
            text="Configurações",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 15))
        
        # Editor de configuração
        self.config_editor = ConfigEditor(config_frame, self.config_manager)
        self.config_editor.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def create_task_panel(self):
        """Criar painel de gerenciamento de tarefas"""
        task_frame = ctk.CTkFrame(self)
        task_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(5, 10))
        task_frame.grid_columnconfigure(0, weight=1)
        task_frame.grid_rowconfigure(2, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            task_frame,
            text="Gerenciador de Tarefas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 15))
        
        # Input de tarefa
        input_frame = ctk.CTkFrame(task_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.task_entry = ctk.CTkTextbox(input_frame, height=80)
        self.task_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        execute_btn = ctk.CTkButton(
            input_frame,
            text="🚀 Executar Tarefa",
            command=self.execute_task
        )
        execute_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Histórico de tarefas
        history_label = ctk.CTkLabel(task_frame, text="Histórico de Execuções:")
        history_label.grid(row=2, column=0, sticky="nw", padx=10, pady=(10, 5))
        
        self.history_listbox = tk.Listbox(task_frame, height=8)
        self.history_listbox.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        
        # Scrollbar para histórico
        scrollbar = tk.Scrollbar(task_frame, orient="vertical")
        scrollbar.grid(row=3, column=2, sticky="ns", pady=(0, 10))
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)
    
    def create_flow_panel(self):
        """Criar painel de visualização de fluxo"""
        flow_frame = ctk.CTkFrame(self)
        flow_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=(5, 10))
        
        # Título
        title = ctk.CTkLabel(
            flow_frame,
            text="Visualizador de Fluxo de Agentes",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 15))
        
        # Canvas para diagrama
        self.flow_canvas = tk.Canvas(
            flow_frame,
            bg="white",
            height=200
        )
        self.flow_canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Desenhar diagrama inicial
        self.draw_flow_diagram()
    
    def draw_flow_diagram(self):
        """Desenhar diagrama de fluxo dos agentes"""
        self.flow_canvas.delete("all")
        
        # Exemplo de diagrama simples
        agents = ["Manus", "Browser", "ToolCall", "ReAct"]
        x_start = 50
        y_center = 100
        box_width = 80
        box_height = 40
        spacing = 120
        
        for i, agent in enumerate(agents):
            x = x_start + i * spacing
            
            # Desenhar caixa do agente
            self.flow_canvas.create_rectangle(
                x, y_center - box_height//2,
                x + box_width, y_center + box_height//2,
                fill="lightblue", outline="blue", width=2
            )
            
            # Texto do agente
            self.flow_canvas.create_text(
                x + box_width//2, y_center,
                text=agent, font=("Arial", 10, "bold")
            )
            
            # Seta para próximo agente
            if i < len(agents) - 1:
                self.flow_canvas.create_line(
                    x + box_width, y_center,
                    x + spacing, y_center,
                    arrow=tk.LAST, width=2, fill="blue"
                )
    
    def start_service(self):
        """Iniciar serviço OpenManus"""
        def start():
            try:
                mode = self.mode_var.get()
                self.service.start(mode)
                self.status_label.configure(text=f"Status: Executando ({mode})")
                self.log_manager.log_info(f"OpenManus iniciado em modo {mode}")
            except Exception as e:
                self.status_label.configure(text=f"Status: Erro - {e}")
                messagebox.showerror("Erro", f"Falha ao iniciar OpenManus: {e}")
        
        threading.Thread(target=start, daemon=True).start()
    
    def stop_service(self):
        """Parar serviço OpenManus"""
        def stop():
            try:
                self.service.stop()
                self.status_label.configure(text="Status: Parado")
                self.log_manager.log_info("OpenManus parado")
            except Exception as e:
                self.status_label.configure(text=f"Status: Erro - {e}")
                messagebox.showerror("Erro", f"Falha ao parar OpenManus: {e}")
        
        threading.Thread(target=stop, daemon=True).start()
    
    def restart_service(self):
        """Reiniciar serviço OpenManus"""
        def restart():
            try:
                self.stop_service()
                threading.Timer(2.0, self.start_service).start()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao reiniciar OpenManus: {e}")
        
        threading.Thread(target=restart, daemon=True).start()
    
    def execute_task(self):
        """Executar tarefa no OpenManus"""
        task_text = self.task_entry.get("1.0", "end-1c").strip()
        
        if not task_text:
            messagebox.showwarning("Aviso", "Digite uma tarefa para executar")
            return
        
        def execute():
            try:
                # Adicionar ao histórico
                timestamp = time.strftime("%H:%M:%S")
                self.history_listbox.insert(0, f"[{timestamp}] {task_text[:50]}...")
                
                # Executar tarefa
                result = self.service.execute_task(task_text)
                
                # Log do resultado
                self.log_manager.log_info(f"Tarefa executada: {task_text[:100]}")
                
                # Limpar entrada
                self.task_entry.delete("1.0", "end")
                
                messagebox.showinfo("Sucesso", "Tarefa executada com sucesso!")
                
            except Exception as e:
                self.log_manager.log_error(f"Erro ao executar tarefa: {e}")
                messagebox.showerror("Erro", f"Falha ao executar tarefa: {e}")
        
        threading.Thread(target=execute, daemon=True).start()