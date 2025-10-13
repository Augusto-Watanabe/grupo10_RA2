"""
Implementação do algoritmo de cache FIFO (First In, First Out)
Remove o item mais antigo do cache quando está cheio

Aluno B - Estrutura do Cache e Algoritmo FIFO
"""

from collections import deque
from typing import Tuple
import time
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(str(Path(__file__).parent.parent))

from core.cache_interface import CacheInterface


class FIFOCache(CacheInterface):
    """
    Implementação do algoritmo FIFO (First In, First Out).
    
    Funcionamento:
    - Mantém uma fila (queue) com a ordem de inserção dos textos
    - Quando o cache está cheio, remove o primeiro texto inserido (mais antigo)
    - Simples e previsível, mas não considera a frequência de uso
    
    Exemplo:
        Cache com capacidade 3, sequência de acessos: 1, 2, 3, 4
        1. Insere 1: [1]
        2. Insere 2: [1, 2]
        3. Insere 3: [1, 2, 3]
        4. Insere 4: Remove 1 (mais antigo), insere 4: [2, 3, 4]
    """
    
    def __init__(self, capacity: int = 10):
        """
        Inicializa o cache FIFO
        
        Args:
            capacity: capacidade máxima do cache (padrão: 10 textos)
        """
        super().__init__(capacity)
        self.queue = deque()  # Fila para manter ordem de inserção
    
    def get(self, text_number: int, loader_function) -> Tuple[str, float, bool]:
        """
        Obtém um texto do cache ou carrega do disco
        
        Args:
            text_number: número do texto desejado
            loader_function: função para carregar do disco se necessário
            
        Returns:
            tuple: (conteúdo, tempo_de_carregamento, cache_hit)
        """
        self.total_requests += 1
        start_time = time.time()
        
        # CACHE HIT - texto está no cache
        if self.is_in_cache(text_number):
            self.hits += 1
            content = self.cache[text_number]
            load_time = time.time() - start_time
            self.load_times.append(load_time)
            return content, load_time, True
        
        # CACHE MISS - texto não está no cache
        self.misses += 1
        
        # Se o cache está cheio, remove o mais antigo (FIFO)
        if self.is_full():
            removed = self._evict()
            del self.cache[removed]
        
        # Carrega o texto do disco
        content, disk_load_time = loader_function(text_number)
        
        # Adiciona ao cache e à fila
        self.cache[text_number] = content
        self.queue.append(text_number)
        
        total_time = time.time() - start_time
        self.load_times.append(total_time)
        
        return content, total_time, False
    
    def _evict(self) -> int:
        """
        Remove o item mais antigo do cache (First In, First Out)
        
        Returns:
            int: número do texto que foi removido
        """
        if not self.queue:
            return None
        
        # Remove e retorna o primeiro item da fila (mais antigo)
        oldest = self.queue.popleft()
        return oldest
    
    def clear(self):
        """Limpa o cache e reseta as métricas"""
        super().clear()
        self.queue.clear()
    
    def get_queue_state(self) -> list:
        """
        Retorna o estado atual da fila (útil para debugging)
        
        Returns:
            list: números dos textos na ordem de inserção
        """
        return list(self.queue)
    
    def __str__(self) -> str:
        """Representação em string do cache"""
        return f"FIFOCache(capacity={self.capacity}, size={self.size()}, queue={list(self.queue)})"


# Testes e exemplos de uso
if __name__ == "__main__":
    print("="*70)
    print("TESTE DO ALGORITMO FIFO (First In, First Out)")
    print("="*70)
    
    # Função mock para simular carregamento do disco
    def mock_loader(text_number):
        """Simula carregamento do disco com latência"""
        time.sleep(0.05)  # 50ms de latência
        content = f"Conteúdo simulado do texto {text_number} " * 100
        return content, 0.05
    
    # Cria um cache FIFO com capacidade reduzida para facilitar o teste
    cache = FIFOCache(capacity=3)
    
    print(f"\nCache criado: {cache}")
    print(f"Capacidade: {cache.capacity} textos\n")
    
    # Sequência de testes que demonstra o comportamento FIFO
    test_sequence = [1, 2, 3, 1, 4, 5, 2]
    
    print("Sequência de requisições:", test_sequence)
    print("\nExecutando requisições:\n")
    
    for i, text_num in enumerate(test_sequence, 1):
        content, load_time, was_hit = cache.get(text_num, mock_loader)
        
        status = "HIT ✓ " if was_hit else "MISS ✗"
        queue_state = cache.get_queue_state()
        
        print(f"{i}. Texto {text_num}: {status} | "
              f"Tempo: {load_time:.4f}s | "
              f"Fila: {queue_state}")
    
    # Exibe métricas finais
    print("\n" + "="*70)
    cache.print_metrics()
    
    # Análise detalhada
    print("="*70)
    print("ANÁLISE DO COMPORTAMENTO FIFO")
    print("="*70)
    print("""
Observações sobre o comportamento:
    
1. Requisições [1, 2, 3]: 
   - Todas são MISS, cache enche: [1, 2, 3]

2. Requisição [1]:
   - HIT! O texto 1 já está no cache
   - FIFO não altera a ordem, continua: [1, 2, 3]

3. Requisição [4]:
   - MISS! Cache está cheio
   - Remove o mais antigo (1): [2, 3]
   - Adiciona 4: [2, 3, 4]

4. Requisição [5]:
   - MISS! Remove o mais antigo (2): [3, 4]
   - Adiciona 5: [3, 4, 5]

5. Requisição [2]:
   - MISS! O texto 2 foi removido anteriormente
   - Remove o mais antigo (3): [4, 5]
   - Adiciona 2: [4, 5, 2]
    
Vantagens do FIFO:
✓ Simples de implementar
✓ Previsível e justo
✓ Baixo overhead de processamento

Desvantagens do FIFO:
✗ Não considera frequência de uso
✗ Pode remover itens ainda relevantes
✗ Não se adapta ao padrão de acesso
    """)
    
    print("="*70)
    print("Estado final da fila:", cache.get_queue_state())
    print("Textos no cache:", list(cache.cache.keys()))
    print("="*70)