"""
Módulo de leitura de textos do disco
Responsável por carregar os arquivos de texto numerados de 1 a 100
"""

import os
import time
from pathlib import Path

class TextLoader:
    """Classe responsável por gerenciar o carregamento de textos do disco"""
    
    def __init__(self, texts_directory="texts"):
        """
        Inicializa o carregador de textos
        
        Args:
            texts_directory: caminho para o diretório contendo os textos
        """
        self.texts_dir = Path(texts_directory)
        self.total_texts = 100
        
        # Verifica se o diretório existe
        if not self.texts_dir.exists():
            raise FileNotFoundError(f"Diretório '{texts_directory}' não encontrado")
    
    def load_text(self, text_number):
        """
        Carrega um texto específico do disco
        
        Args:
            text_number: número do texto (1-100)
            
        Returns:
            tuple: (conteúdo do texto, tempo de carregamento em segundos)
            
        Raises:
            ValueError: se o número do texto for inválido
            FileNotFoundError: se o arquivo não existir
        """
        # Validação do número
        if not isinstance(text_number, int):
            raise ValueError("O número do texto deve ser um inteiro")
        
        if text_number < 1 or text_number > self.total_texts:
            raise ValueError(f"Número do texto deve estar entre 1 e {self.total_texts}")
        
        # Construção do caminho do arquivo
        filename = f"texto_{text_number}.txt"
        file_path = self.texts_dir / filename
        
        if file_path is None:
            raise FileNotFoundError(
                f"Arquivo para o texto {text_number} não encontrado. "
            )
        
        # Medição do tempo de carregamento (simula disco lento)
        start_time = time.time()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            load_time = time.time() - start_time
            
            return content, load_time
            
        except Exception as e:
            raise IOError(f"Erro ao ler o arquivo {file_path}: {str(e)}")

# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    loader = TextLoader()
    
    print("=== Teste do TextLoader ===\n")
    
    # Testa carregamento de um texto
    try:
        text_num = 1
        content, load_time = loader.load_text(text_num)
        print(f"✓ Texto {text_num} carregado com sucesso!")
        print(f"  Tempo de carregamento: {load_time:.4f}s")
        print(f"  Tamanho: {len(content)} caracteres")
        print(f"  Palavras: {len(content.split())}")
        print(f"  Primeiros 100 caracteres:")
        print(f"  {content[:100]}...\n")
    except Exception as e:
        print(f"✗ Erro ao carregar texto {text_num}: {e}\n")