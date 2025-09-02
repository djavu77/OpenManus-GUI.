"""
Widget de Status dos Sistemas
"""

import customtkinter as ctk
import threading
import time
from typing import Dict
from services.openmanus_service import OpenManusService
from services.spongecake_service import SpongecakeService
from services.ollama_service import OllamaService


class StatusWidget(ctk.CTkFrame):
    """Widget para mostrar status dos sistemas"""
    
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        
        self.config_manager = config_manager
        
        # Inicializar serviços
        self.services = {
            'openmanus': OpenManusService(config_manager),
            'spongecake': SpongecakeService(config_manager),
            'ollama': OllamaService(config_manager)
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface do widget"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Status dos Sistemas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 5))
        
        # Status indicators
        self.status_indicators = {}
        
        systems = [
            ("OpenManus", "openmanus"),
            ("Spongecake", "spongecake"),
            ("Ollama", "ollama")
        ]
        
        for i, (display_name, service_key) in enumerate(systems):
            # Nome do sistema
            name_label = ctk.CTkLabel(self, text=f"{display_name}:")
            name_label.grid(row=i+1, column=0, sticky="w", padx=(10, 5), pady=2)
            
            # Indicador de status
            status_indicator = ctk.CTkLabel(
                self,
                text="⚫",
                font=ctk.CTkFont(size=20),
                text_color="red"
            )
            status_indicator.grid(row=i+1, column=1, padx=5, pady=2)
            
            # Label de status
            status_label = ctk.CTkLabel(self, text="Parado")
            status_label.grid(row=i+1, column=2, sticky="w", padx=5, pady=2)
            
            self.status_indicators[service_key] = {
                'indicator': status_indicator,
                'label': status_label
            }
    
    def update_status(self):
        """Atualizar status de todos os sistemas"""
        for service_key, service in self.services.items():
            try:
                is_running = service.is_running()
                status_info = self.status_indicators[service_key]
                
                if is_running:
                    status_info['indicator'].configure(text="🟢", text_color="green")
                    status_info['label'].configure(text="Executando")
                else:
                    status_info['indicator'].configure(text="⚫", text_color="red")
                    status_info['label'].configure(text="Parado")
                    
            except Exception as e:
                status_info = self.status_indicators[service_key]
                status_info['indicator'].configure(text="🟡", text_color="orange")
                status_info['label'].configure(text="Erro")
    
    def get_service_status(self, service_name: str) -> bool:
        """Obter status de um serviço específico"""
        if service_name in self.services:
            return self.services[service_name].is_running()
        return False