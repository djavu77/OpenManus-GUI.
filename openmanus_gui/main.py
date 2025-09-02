#!/usr/bin/env python3
"""
OpenManus Control Center - Interface Gráfica Unificada
Gerencia OpenManus + Spongecake + Ollama de forma integrada
"""

import sys
import os
import threading
from pathlib import Path

# Adicionar o diretório atual ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    import customtkinter as ctk
    from gui.main_window import MainWindow
    from utils.config_manager import ConfigManager
    from utils.log_manager import LogManager
except ImportError as e:
    print(f"Erro ao importar dependências: {e}")
    print("Instale as dependências com: pip install customtkinter psutil docker toml")
    sys.exit(1)


def main():
    """Função principal da aplicação"""
    # Configurar tema escuro por padrão
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Inicializar gerenciadores
    config_manager = ConfigManager()
    log_manager = LogManager()
    
    # Criar e executar janela principal
    app = MainWindow(config_manager, log_manager)
    
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\nEncerrando aplicação...")
        app.cleanup()
    except Exception as e:
        print(f"Erro na aplicação: {e}")
        app.cleanup()


if __name__ == "__main__":
    main()