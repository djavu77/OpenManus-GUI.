"""
Aba de Controle do Spongecake
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import subprocess
import json
import webbrowser
from pathlib import Path

from services.spongecake_service import SpongecakeService


class SpongecakeTab(ctk.CTkFrame):
    """Aba para gerenciar Spongecake"""
    
    def __init__(self, parent, config_manager, log_manager):
        super().__init__(parent)
        
        self.config_manager = config_manager
        self.log_manager = log_manager
        self.service = SpongecakeService(config_manager)
        
        self.setup_ui()
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)
    
    def setup_ui(self):
        """Configurar interface da aba"""
        # Painel de controle
        self.create_control_panel()
        
        # Scripts de automação
        self.create_scripts_panel()
        
        # Monitoramento
        self.create_monitoring_panel()
        
        # Interface web proxy
        self.create_web_panel()
    
    def create_control_panel(self):
        """Criar painel de controle"""
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        control_frame.grid_columnconfigure(4, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            control_frame,
            text="Controle do Spongecake",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=5, pady=(10, 15))
        
        # Botões de controle
        self.start_btn = ctk.CTkButton(
            control_frame,
            text="▶️ Iniciar Backend",
            command=self.start_backend,
            fg_color="green"
        )
        self.start_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.start_frontend_btn = ctk.CTkButton(
            control_frame,
            text="🌐 Iniciar Frontend",
            command=self.start_frontend,
            fg_color="blue"
        )
        self.start_frontend_btn.grid(row=1, column=1, padx=5, pady=5)
        
        self.stop_btn = ctk.CTkButton(
            control_frame,
            text="⏹️ Parar Tudo",
            command=self.stop_service,
            fg_color="red"
        )
        self.stop_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Status e URL
        self.status_label = ctk.CTkLabel(control_frame, text="Status: Parado")
        self.status_label.grid(row=2, column=0, columnspan=3, pady=(10, 5))
        
        self.url_label = ctk.CTkLabel(
            control_frame,
            text="URL: http://localhost:3000",
            text_color="blue",
            cursor="hand2"
        )
        self.url_label.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        self.url_label.bind("<Button-1>", lambda e: webbrowser.open("http://localhost:3000"))
    
    def create_scripts_panel(self):
        """Criar painel de scripts de automação"""
        scripts_frame = ctk.CTkFrame(self)
        scripts_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        scripts_frame.grid_rowconfigure(2, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            scripts_frame,
            text="Scripts de Automação",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 15))
        
        # Lista de scripts
        scripts_label = ctk.CTkLabel(scripts_frame, text="Scripts Disponíveis:")
        scripts_label.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 5))
        
        self.scripts_listbox = tk.Listbox(scripts_frame, height=6)
        self.scripts_listbox.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        
        # Carregar scripts padrão
        default_scripts = [
            "LinkedIn Auto-Connect",
            "Amazon Product Scraper",
            "Data Entry Automation",
            "Email Management",
            "Social Media Posting"
        ]
        
        for script in default_scripts:
            self.scripts_listbox.insert(tk.END, script)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(scripts_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10))
        
        execute_script_btn = ctk.CTkButton(
            btn_frame,
            text="▶️ Executar Script",
            command=self.execute_script
        )
        execute_script_btn.pack(side="left", padx=5, pady=5)
        
        create_script_btn = ctk.CTkButton(
            btn_frame,
            text="➕ Criar Script",
            command=self.create_script
        )
        create_script_btn.pack(side="left", padx=5, pady=5)
    
    def create_monitoring_panel(self):
        """Criar painel de monitoramento"""
        monitor_frame = ctk.CTkFrame(self)
        monitor_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(5, 10))
        
        # Título
        title = ctk.CTkLabel(
            monitor_frame,
            text="Monitoramento",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 15))
        
        # Status do Docker
        docker_frame = ctk.CTkFrame(monitor_frame)
        docker_frame.pack(fill="x", padx=10, pady=5)
        
        docker_label = ctk.CTkLabel(docker_frame, text="Docker Container:")
        docker_label.pack(side="left", padx=5, pady=5)
        
        self.docker_status = ctk.CTkLabel(docker_frame, text="⚫ Parado", text_color="red")
        self.docker_status.pack(side="right", padx=5, pady=5)
        
        # Performance
        perf_frame = ctk.CTkFrame(monitor_frame)
        perf_frame.pack(fill="x", padx=10, pady=5)
        
        perf_label = ctk.CTkLabel(perf_frame, text="Performance:")
        perf_label.pack(side="left", padx=5, pady=5)
        
        self.perf_label = ctk.CTkLabel(perf_frame, text="CPU: 0% | RAM: 0MB")
        self.perf_label.pack(side="right", padx=5, pady=5)
        
        # Gravação de tela
        record_frame = ctk.CTkFrame(monitor_frame)
        record_frame.pack(fill="x", padx=10, pady=5)
        
        self.record_btn = ctk.CTkButton(
            record_frame,
            text="🔴 Iniciar Gravação",
            command=self.toggle_recording
        )
        self.record_btn.pack(pady=10)
    
    def create_web_panel(self):
        """Criar painel de interface web"""
        web_frame = ctk.CTkFrame(self)
        web_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(5, 10))
        
        # Título
        title = ctk.CTkLabel(
            web_frame,
            text="Interface Web",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 15))
        
        # Botões de acesso
        btn_frame = ctk.CTkFrame(web_frame)
        btn_frame.pack(pady=10)
        
        open_web_btn = ctk.CTkButton(
            btn_frame,
            text="🌐 Abrir Interface Web",
            command=lambda: webbrowser.open("http://localhost:3000")
        )
        open_web_btn.pack(side="left", padx=5)
        
        open_admin_btn = ctk.CTkButton(
            btn_frame,
            text="⚙️ Painel Admin",
            command=lambda: webbrowser.open("http://localhost:3000/admin")
        )
        open_admin_btn.pack(side="left", padx=5)
    
    def start_backend(self):
        """Iniciar backend do Spongecake"""
        def start():
            try:
                self.service.start_backend()
                self.status_label.configure(text="Status: Backend Executando")
                self.docker_status.configure(text="🟢 Executando", text_color="green")
                self.log_manager.log_info("Spongecake backend iniciado")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao iniciar backend: {e}")
        
        threading.Thread(target=start, daemon=True).start()
    
    def start_frontend(self):
        """Iniciar frontend do Spongecake"""
        def start():
            try:
                self.service.start_frontend()
                self.status_label.configure(text="Status: Frontend + Backend Executando")
                self.log_manager.log_info("Spongecake frontend iniciado")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao iniciar frontend: {e}")
        
        threading.Thread(target=start, daemon=True).start()
    
    def stop_service(self):
        """Parar serviço Spongecake"""
        def stop():
            try:
                self.service.stop()
                self.status_label.configure(text="Status: Parado")
                self.docker_status.configure(text="⚫ Parado", text_color="red")
                self.log_manager.log_info("Spongecake parado")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao parar Spongecake: {e}")
        
        threading.Thread(target=stop, daemon=True).start()
    
    def execute_script(self):
        """Executar script selecionado"""
        selection = self.scripts_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um script para executar")
            return
        
        script_name = self.scripts_listbox.get(selection[0])
        
        def execute():
            try:
                result = self.service.execute_script(script_name)
                self.log_manager.log_info(f"Script executado: {script_name}")
                messagebox.showinfo("Sucesso", f"Script '{script_name}' executado com sucesso!")
            except Exception as e:
                self.log_manager.log_error(f"Erro ao executar script: {e}")
                messagebox.showerror("Erro", f"Falha ao executar script: {e}")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def create_script(self):
        """Criar novo script de automação"""
        # Abrir dialog para criar script
        dialog = ScriptCreatorDialog(self)
        self.wait_window(dialog)
    
    def toggle_recording(self):
        """Alternar gravação de tela"""
        if self.record_btn.cget("text") == "🔴 Iniciar Gravação":
            self.record_btn.configure(text="⏹️ Parar Gravação", fg_color="red")
            self.service.start_recording()
        else:
            self.record_btn.configure(text="🔴 Iniciar Gravação", fg_color="green")
            self.service.stop_recording()


class ScriptCreatorDialog(ctk.CTkToplevel):
    """Dialog para criar novos scripts"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Criar Novo Script")
        self.geometry("600x400")
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface do dialog"""
        # Nome do script
        name_label = ctk.CTkLabel(self, text="Nome do Script:")
        name_label.pack(pady=(20, 5))
        
        self.name_entry = ctk.CTkEntry(self, width=400)
        self.name_entry.pack(pady=(0, 10))
        
        # Descrição
        desc_label = ctk.CTkLabel(self, text="Descrição:")
        desc_label.pack(pady=(10, 5))
        
        self.desc_entry = ctk.CTkTextbox(self, height=100, width=400)
        self.desc_entry.pack(pady=(0, 10))
        
        # Código do script
        code_label = ctk.CTkLabel(self, text="Código Python:")
        code_label.pack(pady=(10, 5))
        
        self.code_entry = ctk.CTkTextbox(self, height=150, width=400)
        self.code_entry.pack(pady=(0, 20))
        
        # Botões
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Salvar Script",
            command=self.save_script
        )
        save_btn.pack(side="left", padx=5)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=self.destroy
        )
        cancel_btn.pack(side="left", padx=5)
    
    def save_script(self):
        """Salvar novo script"""
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get("1.0", "end-1c").strip()
        code = self.code_entry.get("1.0", "end-1c").strip()
        
        if not name or not code:
            messagebox.showwarning("Aviso", "Nome e código são obrigatórios")
            return
        
        try:
            # Salvar script (implementar lógica de salvamento)
            script_data = {
                "name": name,
                "description": desc,
                "code": code,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Aqui você salvaria o script em arquivo ou banco de dados
            messagebox.showinfo("Sucesso", f"Script '{name}' criado com sucesso!")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar script: {e}")