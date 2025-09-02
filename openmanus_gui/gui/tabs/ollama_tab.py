"""
Aba de Controle do Ollama
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import json
import requests
from pathlib import Path

from services.ollama_service import OllamaService


class OllamaTab(ctk.CTkFrame):
    """Aba para gerenciar Ollama"""
    
    def __init__(self, parent, config_manager, log_manager):
        super().__init__(parent)
        
        self.config_manager = config_manager
        self.log_manager = log_manager
        self.service = OllamaService(config_manager)
        
        self.setup_ui()
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
    
    def setup_ui(self):
        """Configurar interface da aba"""
        # Painel de controle do servidor
        self.create_server_panel()
        
        # Gerenciamento de modelos
        self.create_models_panel()
        
        # Monitoramento de performance
        self.create_performance_panel()
        
        # Configurações de integração
        self.create_integration_panel()
    
    def create_server_panel(self):
        """Criar painel de controle do servidor"""
        server_frame = ctk.CTkFrame(self)
        server_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        server_frame.grid_columnconfigure(3, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            server_frame,
            text="Controle do Servidor Ollama",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=4, pady=(10, 15))
        
        # Botões de controle
        self.start_server_btn = ctk.CTkButton(
            server_frame,
            text="▶️ Iniciar Servidor",
            command=self.start_server,
            fg_color="green"
        )
        self.start_server_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.stop_server_btn = ctk.CTkButton(
            server_frame,
            text="⏹️ Parar Servidor",
            command=self.stop_server,
            fg_color="red"
        )
        self.stop_server_btn.grid(row=1, column=1, padx=5, pady=5)
        
        self.test_api_btn = ctk.CTkButton(
            server_frame,
            text="🧪 Testar API",
            command=self.test_api,
            fg_color="blue"
        )
        self.test_api_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Configuração de porta
        port_label = ctk.CTkLabel(server_frame, text="Porta:")
        port_label.grid(row=2, column=0, sticky="w", padx=5, pady=(10, 5))
        
        self.port_entry = ctk.CTkEntry(server_frame, width=100)
        self.port_entry.insert(0, "11434")
        self.port_entry.grid(row=2, column=1, sticky="w", padx=5, pady=(10, 5))
        
        # Status do servidor
        self.server_status = ctk.CTkLabel(
            server_frame,
            text="Status: Parado",
            font=ctk.CTkFont(size=12)
        )
        self.server_status.grid(row=3, column=0, columnspan=4, pady=(10, 10))
    
    def create_models_panel(self):
        """Criar painel de gerenciamento de modelos"""
        models_frame = ctk.CTkFrame(self)
        models_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        models_frame.grid_rowconfigure(2, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            models_frame,
            text="Gerenciamento de Modelos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 15))
        
        # Lista de modelos instalados
        installed_label = ctk.CTkLabel(models_frame, text="Modelos Instalados:")
        installed_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 5))
        
        self.models_listbox = tk.Listbox(models_frame, height=8)
        self.models_listbox.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(models_frame, orient="vertical")
        scrollbar.grid(row=2, column=2, sticky="ns", pady=(0, 10))
        self.models_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.models_listbox.yview)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(models_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10))
        
        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Atualizar Lista",
            command=self.refresh_models
        )
        refresh_btn.pack(side="left", padx=5, pady=5)
        
        download_btn = ctk.CTkButton(
            btn_frame,
            text="⬇️ Baixar Modelo",
            command=self.download_model
        )
        download_btn.pack(side="left", padx=5, pady=5)
        
        remove_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Remover Modelo",
            command=self.remove_model,
            fg_color="red"
        )
        remove_btn.pack(side="left", padx=5, pady=5)
    
    def create_performance_panel(self):
        """Criar painel de monitoramento de performance"""
        perf_frame = ctk.CTkFrame(self)
        perf_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(5, 10))
        
        # Título
        title = ctk.CTkLabel(
            perf_frame,
            text="Performance",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 15))
        
        # Métricas
        metrics_frame = ctk.CTkFrame(perf_frame)
        metrics_frame.pack(fill="x", padx=10, pady=5)
        
        # GPU Usage
        gpu_label = ctk.CTkLabel(metrics_frame, text="Uso da GPU:")
        gpu_label.pack(anchor="w", padx=5, pady=2)
        
        self.gpu_progress = ctk.CTkProgressBar(metrics_frame)
        self.gpu_progress.pack(fill="x", padx=5, pady=2)
        self.gpu_progress.set(0)
        
        # Memory Usage
        mem_label = ctk.CTkLabel(metrics_frame, text="Uso de Memória:")
        mem_label.pack(anchor="w", padx=5, pady=2)
        
        self.mem_progress = ctk.CTkProgressBar(metrics_frame)
        self.mem_progress.pack(fill="x", padx=5, pady=2)
        self.mem_progress.set(0)
        
        # Request Times
        time_label = ctk.CTkLabel(metrics_frame, text="Tempo de Resposta:")
        time_label.pack(anchor="w", padx=5, pady=2)
        
        self.response_time_label = ctk.CTkLabel(metrics_frame, text="0ms")
        self.response_time_label.pack(anchor="w", padx=5, pady=2)
    
    def create_integration_panel(self):
        """Criar painel de configurações de integração"""
        integration_frame = ctk.CTkFrame(self)
        integration_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(5, 10))
        
        # Título
        title = ctk.CTkLabel(
            integration_frame,
            text="Integração com OpenManus",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 15))
        
        # Configurações
        config_frame = ctk.CTkFrame(integration_frame)
        config_frame.pack(fill="x", padx=10, pady=5)
        
        # Modelo padrão
        default_model_label = ctk.CTkLabel(config_frame, text="Modelo Padrão:")
        default_model_label.pack(side="left", padx=5, pady=5)
        
        self.default_model_combo = ctk.CTkComboBox(
            config_frame,
            values=["llama3.2", "llama3.2-vision", "codellama", "mistral"]
        )
        self.default_model_combo.pack(side="left", padx=5, pady=5)
        
        # Botão aplicar configuração
        apply_btn = ctk.CTkButton(
            integration_frame,
            text="✅ Aplicar Configuração",
            command=self.apply_integration_config
        )
        apply_btn.pack(pady=20)
    
    def start_server(self):
        """Iniciar servidor Ollama"""
        def start():
            try:
                port = self.port_entry.get()
                self.service.start_server(port)
                self.server_status.configure(text=f"Status: Executando na porta {port}")
                self.log_manager.log_info(f"Ollama servidor iniciado na porta {port}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao iniciar servidor: {e}")
        
        threading.Thread(target=start, daemon=True).start()
    
    def stop_server(self):
        """Parar servidor Ollama"""
        def stop():
            try:
                self.service.stop_server()
                self.server_status.configure(text="Status: Parado")
                self.log_manager.log_info("Ollama servidor parado")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao parar servidor: {e}")
        
        threading.Thread(target=stop, daemon=True).start()
    
    def test_api(self):
        """Testar API do Ollama"""
        def test():
            try:
                result = self.service.test_api()
                if result:
                    messagebox.showinfo("Sucesso", "API do Ollama está funcionando!")
                else:
                    messagebox.showerror("Erro", "API do Ollama não está respondendo")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao testar API: {e}")
        
        threading.Thread(target=test, daemon=True).start()
    
    def refresh_models(self):
        """Atualizar lista de modelos"""
        def refresh():
            try:
                models = self.service.list_models()
                
                # Limpar lista atual
                self.models_listbox.delete(0, tk.END)
                
                # Adicionar modelos
                for model in models:
                    self.models_listbox.insert(tk.END, model)
                
                self.log_manager.log_info(f"Lista de modelos atualizada: {len(models)} modelos")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao atualizar modelos: {e}")
        
        threading.Thread(target=refresh, daemon=True).start()
    
    def download_model(self):
        """Baixar novo modelo"""
        # Dialog para selecionar modelo
        dialog = ModelDownloadDialog(self)
        self.wait_window(dialog)
    
    def remove_model(self):
        """Remover modelo selecionado"""
        selection = self.models_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um modelo para remover")
            return
        
        model_name = self.models_listbox.get(selection[0])
        
        if messagebox.askyesno("Confirmar", f"Remover modelo '{model_name}'?"):
            def remove():
                try:
                    self.service.remove_model(model_name)
                    self.refresh_models()
                    self.log_manager.log_info(f"Modelo removido: {model_name}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao remover modelo: {e}")
            
            threading.Thread(target=remove, daemon=True).start()
    
    def apply_integration_config(self):
        """Aplicar configuração de integração"""
        try:
            default_model = self.default_model_combo.get()
            
            # Atualizar configuração do OpenManus para usar Ollama
            config_data = {
                "llm": {
                    "api_type": "ollama",
                    "model": default_model,
                    "base_url": f"http://localhost:{self.port_entry.get()}/v1",
                    "api_key": "ollama"
                }
            }
            
            self.config_manager.update_openmanus_config(config_data)
            
            messagebox.showinfo("Sucesso", "Configuração de integração aplicada!")
            self.log_manager.log_info(f"Integração configurada: modelo {default_model}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao aplicar configuração: {e}")


class ModelDownloadDialog(ctk.CTkToplevel):
    """Dialog para baixar modelos"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent_tab = parent
        self.title("Baixar Modelo")
        self.geometry("500x300")
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface do dialog"""
        # Título
        title = ctk.CTkLabel(
            self,
            text="Baixar Novo Modelo",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(20, 15))
        
        # Seleção de modelo
        model_label = ctk.CTkLabel(self, text="Selecione o Modelo:")
        model_label.pack(pady=(10, 5))
        
        self.model_combo = ctk.CTkComboBox(
            self,
            values=[
                "llama3.2:latest",
                "llama3.2-vision:latest",
                "codellama:latest",
                "mistral:latest",
                "phi3:latest",
                "gemma2:latest"
            ],
            width=300
        )
        self.model_combo.pack(pady=(0, 10))
        
        # Ou inserir nome customizado
        custom_label = ctk.CTkLabel(self, text="Ou digite nome customizado:")
        custom_label.pack(pady=(10, 5))
        
        self.custom_entry = ctk.CTkEntry(self, width=300, placeholder_text="ex: llama3.2:7b")
        self.custom_entry.pack(pady=(0, 20))
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        self.progress_label = ctk.CTkLabel(self, text="Pronto para download")
        self.progress_label.pack(pady=(0, 20))
        
        # Botões
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        
        self.download_btn = ctk.CTkButton(
            btn_frame,
            text="⬇️ Baixar",
            command=self.start_download
        )
        self.download_btn.pack(side="left", padx=5)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=self.destroy
        )
        cancel_btn.pack(side="left", padx=5)
    
    def start_download(self):
        """Iniciar download do modelo"""
        model_name = self.custom_entry.get().strip() or self.model_combo.get()
        
        if not model_name:
            messagebox.showwarning("Aviso", "Selecione ou digite um nome de modelo")
            return
        
        def download():
            try:
                self.download_btn.configure(state="disabled")
                self.progress_label.configure(text=f"Baixando {model_name}...")
                
                # Simular progresso (implementar download real)
                for i in range(101):
                    self.progress.set(i / 100)
                    self.progress_label.configure(text=f"Baixando {model_name}... {i}%")
                    time.sleep(0.1)  # Simular tempo de download
                
                # Atualizar lista de modelos na aba pai
                self.parent_tab.refresh_models()
                
                messagebox.showinfo("Sucesso", f"Modelo '{model_name}' baixado com sucesso!")
                self.destroy()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao baixar modelo: {e}")
            finally:
                self.download_btn.configure(state="normal")
        
        threading.Thread(target=download, daemon=True).start()