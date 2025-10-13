"""
Interface abstrata para algoritmos de cache
Define a estrutura que todos os algoritmos devem seguir
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict
import time


class CacheInterface(ABC):
    """
    Classe abstrata que define a interface para algoritmos de cache.
    Todos os algoritmos (FIFO, LRU, LFU, etc.) devem herdar desta classe.
    """
    
    def __init__(self, capacity: int = 10):
        """
        Inicializa a estrutura base do cache
        
        Args:
            capacity: capacidade máxima do cache (padrão: 10 textos)
        """
        self.capacity = capacity
        self.cache = {}  # Dicionário {text_number: content}
        
        # Métricas de performance
        self.hits = 0        # Número de vezes que o texto estava no cache
        self.misses = 0      # Número de vezes que o texto NÃO estava no cache
        self.total_requests = 0
        self.load_times = []  # Lista de tempos de carregamento
    
    @abstractmethod
    def get(self, text_number: int, loader_function) -> Tuple[str, float, bool]:
        """
        Método abstrato para obter um texto do cache.
        Cada algoritmo implementa sua própria lógica.
        
        Args:
            text_number: número do texto desejado
            loader_function: função para carregar do disco se não estiver no cache
            
        Returns:
            tuple: (conteúdo, tempo_de_carregamento, cache_hit)
                - conteúdo: string com o texto
                - tempo: tempo em segundos para obter o texto
                - cache_hit: True se estava no cache, False se carregou do disco
        """
        pass
    
    @abstractmethod
    def _evict(self) -> int:
        """
        Método abstrato para escolher qual item remover do cache.
        Cada algoritmo implementa sua própria política de remoção.
        
        Returns:
            int: número do texto que foi removido
        """
        pass
    
    def is_full(self) -> bool:
        """Verifica se o cache está cheio"""
        return len(self.cache) >= self.capacity
    
    def is_in_cache(self, text_number: int) -> bool:
        """Verifica se um texto está no cache"""
        return text_number in self.cache
    
    def size(self) -> int:
        """Retorna o número de itens atualmente no cache"""
        return len(self.cache)
    
    def clear(self):
        """Limpa o cache e reseta as métricas"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        self.total_requests = 0
        self.load_times.clear()
    
    def get_metrics(self) -> Dict:
        """
        Retorna as métricas de performance do cache
        
        Returns:
            dict: métricas incluindo hit rate, miss rate, tempos, etc.
        """
        hit_rate = (self.hits / self.total_requests * 100) if self.total_requests > 0 else 0
        miss_rate = (self.misses / self.total_requests * 100) if self.total_requests > 0 else 0
        avg_load_time = sum(self.load_times) / len(self.load_times) if self.load_times else 0
        
        return {
            'algorithm': self.__class__.__name__,
            'capacity': self.capacity,
            'current_size': self.size(),
            'total_requests': self.total_requests,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'miss_rate': miss_rate,
            'avg_load_time': avg_load_time,
            'total_load_time': sum(self.load_times)
        }
    
    def print_metrics(self):
        """Exibe as métricas de forma formatada"""
        metrics = self.get_metrics()
        print(f"\n{'='*60}")
        print(f"Métricas do Cache - {metrics['algorithm']}")
        print(f"{'='*60}")
        print(f"Capacidade: {metrics['capacity']} textos")
        print(f"Itens no cache: {metrics['current_size']}")
        print(f"Total de requisições: {metrics['total_requests']}")
        print(f"Cache Hits: {metrics['hits']} ({metrics['hit_rate']:.2f}%)")
        print(f"Cache Misses: {metrics['misses']} ({metrics['miss_rate']:.2f}%)")
        print(f"Tempo médio de carregamento: {metrics['avg_load_time']:.4f}s")
        print(f"Tempo total: {metrics['total_load_time']:.4f}s")
        print(f"{'='*60}\n")
    
    def __str__(self) -> str:
        """Representação em string do cache"""
        return f"{self.__class__.__name__}(capacity={self.capacity}, size={self.size()})"
    
    def __repr__(self) -> str:
        return self.__str__()


class BaseCache(CacheInterface):
    """
    Implementação base com funcionalidades comuns.
    Pode ser usado como exemplo ou classe auxiliar.
    """
    
    def get(self, text_number: int, loader_function) -> Tuple[str, float, bool]:
        """
        Implementação básica do get (não usa nenhum algoritmo específico)
        """
        self.total_requests += 1
        start_time = time.time()
        
        # Verifica se está no cache (HIT)
        if self.is_in_cache(text_number):
            self.hits += 1
            content = self.cache[text_number]
            load_time = time.time() - start_time
            self.load_times.append(load_time)
            return content, load_time, True
        
        # Não está no cache (MISS) - precisa carregar do disco
        self.misses += 1
        
        # Se o cache está cheio, remove um item
        if self.is_full():
            removed = self._evict()
            del self.cache[removed]
        
        # Carrega do disco
        content, disk_load_time = loader_function(text_number)
        
        # Adiciona ao cache
        self.cache[text_number] = content
        
        total_time = time.time() - start_time
        self.load_times.append(total_time)
        
        return content, total_time, False
    
    def _evict(self) -> int:
        """
        Implementação base: remove o primeiro item (FIFO simplificado)
        """
        if not self.cache:
            return None
        return next(iter(self.cache))


# Exemplo de uso e teste
if __name__ == "__main__":
    print("=== Teste da Interface de Cache ===\n")
    
    # Função mock para simular carregamento do disco
    def mock_loader(text_number):
        """Simula carregamento do disco"""
        time.sleep(0.1)  # Simula latência
        return f"Conteúdo do texto {text_number}", 0.1
    
    # Testa a implementação base
    cache = BaseCache(capacity=3)
    
    print(f"Cache criado: {cache}\n")
    
    # Simula requisições
    for i in [1, 2, 3, 1, 4, 2]:
        content, load_time, was_hit = cache.get(i, mock_loader)
        status = "HIT ✓" if was_hit else "MISS ✗"
        print(f"Texto {i}: {status} - Tempo: {load_time:.4f}s")
    
    # Exibe métricas
    cache.print_metrics()
    
    print(f"Conteúdo atual do cache: {list(cache.cache.keys())}")