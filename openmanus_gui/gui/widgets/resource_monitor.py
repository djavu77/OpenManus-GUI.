"""
Widget de Monitoramento de Recursos
"""

import customtkinter as ctk
import psutil
import threading
import time


class ResourceMonitor(ctk.CTkFrame):
    """Widget para monitorar recursos do sistema"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface do widget"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Recursos do Sistema",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        
        # CPU
        cpu_label = ctk.CTkLabel(self, text="CPU:")
        cpu_label.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=2)
        
        self.cpu_value = ctk.CTkLabel(self, text="0%")
        self.cpu_value.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # RAM
        ram_label = ctk.CTkLabel(self, text="RAM:")
        ram_label.grid(row=2, column=0, sticky="w", padx=(10, 5), pady=2)
        
        self.ram_value = ctk.CTkLabel(self, text="0 GB")
        self.ram_value.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        # GPU (se disponível)
        gpu_label = ctk.CTkLabel(self, text="GPU:")
        gpu_label.grid(row=3, column=0, sticky="w", padx=(10, 5), pady=2)
        
        self.gpu_value = ctk.CTkLabel(self, text="N/A")
        self.gpu_value.grid(row=3, column=1, sticky="w", padx=5, pady=2)
        
        # Disco
        disk_label = ctk.CTkLabel(self, text="Disco:")
        disk_label.grid(row=4, column=0, sticky="w", padx=(10, 5), pady=(2, 10))
        
        self.disk_value = ctk.CTkLabel(self, text="0%")
        self.disk_value.grid(row=4, column=1, sticky="w", padx=(5, 10), pady=(2, 10))
    
    def update(self):
        """Atualizar valores dos recursos"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=None)
            self.cpu_value.configure(text=f"{cpu_percent:.1f}%")
            
            # RAM
            memory = psutil.virtual_memory()
            ram_gb = memory.used / (1024**3)
            ram_percent = memory.percent
            self.ram_value.configure(text=f"{ram_gb:.1f}GB ({ram_percent:.1f}%)")
            
            # Disco
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.disk_value.configure(text=f"{disk_percent:.1f}%")
            
            # GPU (tentar obter info da GPU)
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    self.gpu_value.configure(text=f"{gpu.load*100:.1f}%")
                else:
                    self.gpu_value.configure(text="N/A")
            except ImportError:
                self.gpu_value.configure(text="N/A")
            except Exception:
                self.gpu_value.configure(text="Erro")
                
        except Exception as e:
            print(f"Erro ao atualizar recursos: {e}")