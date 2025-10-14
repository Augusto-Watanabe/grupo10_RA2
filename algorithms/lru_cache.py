"""
Implementação do algoritmo de cache LRU (Least Recently Used)
Remove o item usado há mais tempo quando o cache está cheio

Aluno C - Algoritmo LRU
"""

from collections import OrderedDict
from typing import Tuple
import time
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(str(Path(__file__).parent.parent))

from core.cache_interface import CacheInterface


class LRUCache(CacheInterface):
    """
    Implementação do algoritmo LRU (Least Recently Used).
    
    Funcionamento:
    - Mantém rastreamento de quando cada item foi acessado (leitura ou inserção)
    - Quando o cache está cheio, remove o item usado há MAIS tempo
    - Diferente do FIFO, considera TODOS os acessos, não apenas inserção
    - Usa OrderedDict para manter ordem de uso eficientemente
    
    Exemplo:
        Cache com capacidade 3, sequência: 1, 2, 3, 1, 4
        1. Acessa 1: [1]
        2. Acessa 2: [1, 2]
        3. Acessa 3: [1, 2, 3]
        4. Acessa 1: [2, 3, 1]        ← 1 vai pro final (mais recente)
        5. Acessa 4: [3, 1, 4]        ← Remove 2 (menos usado recentemente)
        
    Vantagem sobre FIFO: Se um item é acessado frequentemente, 
    ele permanece no cache mesmo que seja antigo.
    """
    
    def __init__(self, capacity: int = 10):
        """
        Inicializa o cache LRU
        
        Args:
            capacity: capacidade máxima do cache (padrão: 10 textos)
        """
        # Não usa self.cache do pai, usa OrderedDict diretamente
        # para ter controle sobre a ordem
        super().__init__(capacity)
        
        # OrderedDict mantém ordem de inserção e permite mover itens
        self.cache = OrderedDict()
        
        # Dicionário auxiliar para rastrear último acesso (timestamp)
        self.last_access = {}
    
    def get(self, text_number: int, loader_function) -> Tuple[str, float, bool]:
        """
        Obtém um texto do cache ou carrega do disco
        Move o item para o final (marca como recentemente usado)
        
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
            
            # Move para o final (marca como recentemente usado)
            # Isso é a chave do LRU!
            self.cache.move_to_end(text_number)
            self.last_access[text_number] = time.time()
            
            content = self.cache[text_number]
            load_time = time.time() - start_time
            self.load_times.append(load_time)
            return content, load_time, True
        
        # CACHE MISS - texto não está no cache
        self.misses += 1
        
        # Se o cache está cheio, remove o menos usado recentemente (LRU)
        if self.is_full():
            removed = self._evict()
            del self.cache[removed]
            if removed in self.last_access:
                del self.last_access[removed]
        
        # Carrega o texto do disco
        content, disk_load_time = loader_function(text_number)
        
        # Adiciona ao cache (vai automaticamente para o final)
        self.cache[text_number] = content
        self.last_access[text_number] = time.time()
        
        total_time = time.time() - start_time
        self.load_times.append(total_time)
        
        return content, total_time, False
    
    def _evict(self) -> int:
        """
        Remove o item usado há mais tempo (Least Recently Used)
        
        Returns:
            int: número do texto que foi removido
        """
        if not self.cache:
            return None
        
        # O primeiro item do OrderedDict é o menos usado recentemente
        # porque movemos itens acessados para o final
        least_recently_used = next(iter(self.cache))
        return least_recently_used
    
    def clear(self):
        """Limpa o cache e reseta as métricas"""
        super().clear()
        self.cache = OrderedDict()
        self.last_access.clear()
    
    def get_access_order(self) -> list:
        """
        Retorna a ordem de acesso atual (útil para debugging)
        Do menos recente (será removido primeiro) ao mais recente
        
        Returns:
            list: números dos textos na ordem de uso
        """
        return list(self.cache.keys())
    
    def __str__(self) -> str:
        """Representação em string do cache"""
        order = self.get_access_order()
        return f"LRUCache(capacity={self.capacity}, size={self.size()}, order={order})"


# Testes e exemplos de uso
if __name__ == "__main__":
    print("="*70)
    print("TESTE DO ALGORITMO LRU (Least Recently Used)")
    print("="*70)
    
    # Função mock para simular carregamento do disco
    def mock_loader(text_number):
        """Simula carregamento do disco com latência"""
        time.sleep(0.05)  # 50ms de latência
        content = f"Conteúdo simulado do texto {text_number} " * 100
        return content, 0.05
    
    # Cria um cache LRU com capacidade reduzida para facilitar o teste
    cache = LRUCache(capacity=3)
    
    print(f"\nCache criado: {cache}")
    print(f"Capacidade: {cache.capacity} textos\n")
    
    # Sequência de testes que demonstra a diferença entre LRU e FIFO
    test_sequence = [1, 2, 3, 1, 4, 2, 5]
    
    print("Sequência de requisições:", test_sequence)
    print("\nExecutando requisições:\n")
    
    for i, text_num in enumerate(test_sequence, 1):
        content, load_time, was_hit = cache.get(text_num, mock_loader)
        
        status = "HIT ✓ " if was_hit else "MISS ✗"
        access_order = cache.get_access_order()
        
        print(f"{i}. Texto {text_num}: {status} | "
              f"Tempo: {load_time:.4f}s | "
              f"Ordem: {access_order}")
        
        if i == 4:
            print("   ↑ Texto 1 move para o final (recém acessado)")
        elif i == 5:
            print("   ↑ Remove 3 (menos usado), não 1 (foi acessado recentemente)")
    
    # Exibe métricas finais
    print("\n" + "="*70)
    cache.print_metrics()