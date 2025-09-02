"""
Janela Principal do OpenManus Control Center
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import time
from typing import Dict, Any

from .tabs.openmanus_tab import OpenManusTab
from .tabs.spongecake_tab import SpongecakeTab
from .tabs.ollama_tab import OllamaTab
from .tabs.logs_tab import LogsTab
from .widgets.status_widget import StatusWidget
from .widgets.resource_monitor import ResourceMonitor
from utils.config_manager import ConfigManager
from utils.log_manager import LogManager


class MainWindow(ctk.CTk):
    """Janela principal da aplicação"""
    
    def __init__(self, config_manager: ConfigManager, log_manager: LogManager):
        super().__init__()
        
        self.config_manager = config_manager
        self.log_manager = log_manager
        
        # Configurações da janela
        self.title("OpenManus Control Center")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Variáveis de controle
        self.running = True
        self.update_thread = None
        
        # Configurar layout
        self.setup_ui()
        
        # Iniciar thread de atualização
        self.start_update_thread()
        
        # Configurar evento de fechamento
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Configurar interface do usuário"""
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Barra superior com status e recursos
        self.create_top_bar()
        
        # Área principal com abas
        self.create_main_area()
        
        # Barra inferior com ações rápidas
        self.create_bottom_bar()
    
    def create_top_bar(self):
        """Criar barra superior com status e monitoramento"""
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5))
        top_frame.grid_columnconfigure(1, weight=1)
        
        # Widget de status dos sistemas
        self.status_widget = StatusWidget(top_frame, self.config_manager)
        self.status_widget.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        # Monitor de recursos
        self.resource_monitor = ResourceMonitor(top_frame)
        self.resource_monitor.grid(row=0, column=2, sticky="e", padx=10, pady=10)
    
    def create_main_area(self):
        """Criar área principal com sistema de abas"""
        # Notebook para as abas
        self.notebook = ctk.CTkTabview(self)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        
        # Criar abas
        self.create_tabs()
    
    def create_tabs(self):
        """Criar todas as abas do sistema"""
        # Aba OpenManus
        self.notebook.add("OpenManus")
        self.openmanus_tab = OpenManusTab(
            self.notebook.tab("OpenManus"), 
            self.config_manager, 
            self.log_manager
        )
        
        # Aba Spongecake
        self.notebook.add("Spongecake")
        self.spongecake_tab = SpongecakeTab(
            self.notebook.tab("Spongecake"), 
            self.config_manager, 
            self.log_manager
        )
        
        # Aba Ollama
        self.notebook.add("Ollama")
        self.ollama_tab = OllamaTab(
            self.notebook.tab("Ollama"), 
            self.config_manager, 
            self.log_manager
        )
        
        # Aba Logs
        self.notebook.add("Logs")
        self.logs_tab = LogsTab(
            self.notebook.tab("Logs"), 
            self.log_manager
        )
    
    def create_bottom_bar(self):
        """Criar barra inferior com ações rápidas"""
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10))
        
        # Botões de ação rápida
        quick_actions_frame = ctk.CTkFrame(bottom_frame)
        quick_actions_frame.pack(side="left", padx=10, pady=10)
        
        # Botão Iniciar Todos
        self.start_all_btn = ctk.CTkButton(
            quick_actions_frame,
            text="🚀 Iniciar Todos",
            command=self.start_all_services,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.start_all_btn.pack(side="left", padx=5)
        
        # Botão Parar Todos
        self.stop_all_btn = ctk.CTkButton(
            quick_actions_frame,
            text="⏹️ Parar Todos",
            command=self.stop_all_services,
            fg_color="red",
            hover_color="darkred"
        )
        self.stop_all_btn.pack(side="left", padx=5)
        
        # Botão Reiniciar Todos
        self.restart_all_btn = ctk.CTkButton(
            quick_actions_frame,
            text="🔄 Reiniciar Todos",
            command=self.restart_all_services,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.restart_all_btn.pack(side="left", padx=5)
        
        # Status geral
        self.status_label = ctk.CTkLabel(
            bottom_frame,
            text="Sistema Pronto",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="right", padx=10, pady=10)
    
    def start_update_thread(self):
        """Iniciar thread para atualizações em tempo real"""
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
    
    def update_loop(self):
        """Loop de atualização em tempo real"""
        while self.running:
            try:
                # Atualizar status dos sistemas
                self.after(0, self.update_status)
                
                # Atualizar recursos
                self.after(0, self.resource_monitor.update)
                
                # Aguardar próxima atualização
                time.sleep(2)
                
            except Exception as e:
                self.log_manager.log_error(f"Erro no loop de atualização: {e}")
                time.sleep(5)
    
    def update_status(self):
        """Atualizar status dos sistemas"""
        try:
            self.status_widget.update_status()
        except Exception as e:
            self.log_manager.log_error(f"Erro ao atualizar status: {e}")
    
    def start_all_services(self):
        """Iniciar todos os serviços"""
        def start_services():
            try:
                self.status_label.configure(text="Iniciando serviços...")
                
                # Iniciar Ollama primeiro (dependência)
                self.ollama_tab.start_service()
                time.sleep(2)
                
                # Iniciar OpenManus
                self.openmanus_tab.start_service()
                time.sleep(1)
                
                # Iniciar Spongecake
                self.spongecake_tab.start_service()
                
                self.status_label.configure(text="Todos os serviços iniciados")
                
            except Exception as e:
                self.status_label.configure(text=f"Erro ao iniciar: {e}")
                messagebox.showerror("Erro", f"Falha ao iniciar serviços: {e}")
        
        threading.Thread(target=start_services, daemon=True).start()
    
    def stop_all_services(self):
        """Parar todos os serviços"""
        def stop_services():
            try:
                self.status_label.configure(text="Parando serviços...")
                
                # Parar na ordem inversa
                self.spongecake_tab.stop_service()
                self.openmanus_tab.stop_service()
                self.ollama_tab.stop_service()
                
                self.status_label.configure(text="Todos os serviços parados")
                
            except Exception as e:
                self.status_label.configure(text=f"Erro ao parar: {e}")
                messagebox.showerror("Erro", f"Falha ao parar serviços: {e}")
        
        threading.Thread(target=stop_services, daemon=True).start()
    
    def restart_all_services(self):
        """Reiniciar todos os serviços"""
        def restart_services():
            try:
                self.status_label.configure(text="Reiniciando serviços...")
                
                # Parar todos
                self.stop_all_services()
                time.sleep(3)
                
                # Iniciar todos
                self.start_all_services()
                
            except Exception as e:
                self.status_label.configure(text=f"Erro ao reiniciar: {e}")
                messagebox.showerror("Erro", f"Falha ao reiniciar serviços: {e}")
        
        threading.Thread(target=restart_services, daemon=True).start()
    
    def cleanup(self):
        """Limpeza ao fechar aplicação"""
        self.running = False
        
        # Parar serviços se estiverem rodando
        try:
            self.stop_all_services()
        except:
            pass
        
        # Aguardar thread de atualização
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=2)
    
    def on_closing(self):
        """Evento de fechamento da janela"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair? Todos os serviços serão parados."):
            self.cleanup()
            self.destroy()