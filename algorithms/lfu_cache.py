"""
Implementação do algoritmo de cache LFU (Least Frequently Used)
Remove o item menos frequentemente usado quando o cache está cheio

Aluno D - Algoritmo LFU
"""

from collections import defaultdict, OrderedDict
from typing import Tuple
import time
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(str(Path(__file__).parent.parent))

from core.cache_interface import CacheInterface


class LFUCache(CacheInterface):
    """
    Implementação do algoritmo LFU (Least Frequently Used).
    
    Funcionamento:
    - Conta quantas vezes cada item foi acessado (frequência)
    - Quando o cache está cheio, remove o item com MENOR frequência
    - Em caso de empate, remove o menos recentemente usado (LRU como desempate)
    - Usa estrutura de dados eficiente para manter contadores
    
    Exemplo:
        Cache com capacidade 3, sequência: 1, 2, 3, 1, 1, 4
        1. Acessa 1: [1(freq=1)]
        2. Acessa 2: [1(1), 2(1)]
        3. Acessa 3: [1(1), 2(1), 3(1)]
        4. Acessa 1: [1(2), 2(1), 3(1)]     ← freq de 1 aumenta
        5. Acessa 1: [1(3), 2(1), 3(1)]     ← freq de 1 aumenta
        6. Acessa 4: [1(3), 3(1), 4(1)]     ← Remove 2 (menor freq, usado há mais tempo)
        
    Vantagem sobre LRU: Mantém itens que são acessados MUITAS vezes,
    mesmo que não sejam os mais recentes.
    """
    
    def __init__(self, capacity: int = 10):
        """
        Inicializa o cache LFU
        
        Args:
            capacity: capacidade máxima do cache (padrão: 10 textos)
        """
        super().__init__(capacity)
        
        # Contador de frequência para cada texto
        self.frequency = defaultdict(int)
        
        # Para desempate: usa ordem de acesso (LRU)
        # Mantém ordem de acesso para cada nível de frequência
        self.freq_to_items = defaultdict(OrderedDict)
        
        # Frequência mínima atual no cache
        self.min_freq = 0
    
    def get(self, text_number: int, loader_function) -> Tuple[str, float, bool]:
        """
        Obtém um texto do cache ou carrega do disco
        Incrementa a frequência de acesso
        
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
            
            # Atualiza a frequência
            self._update_frequency(text_number)
            
            content = self.cache[text_number]
            load_time = time.time() - start_time
            self.load_times.append(load_time)
            return content, load_time, True
        
        # CACHE MISS - texto não está no cache
        self.misses += 1
        
        # Se o cache está cheio, remove o menos frequentemente usado (LFU)
        if self.is_full():
            removed = self._evict()
            del self.cache[removed]
            del self.frequency[removed]
        
        # Carrega o texto do disco
        content, disk_load_time = loader_function(text_number)
        
        # Adiciona ao cache com frequência 1
        self.cache[text_number] = content
        self.frequency[text_number] = 1
        self.freq_to_items[1][text_number] = None
        self.min_freq = 1
        
        total_time = time.time() - start_time
        self.load_times.append(total_time)
        
        return content, total_time, False
    
    def _update_frequency(self, text_number: int):
        """
        Atualiza a frequência de um item quando é acessado
        
        Args:
            text_number: número do texto acessado
        """
        # Pega a frequência atual
        freq = self.frequency[text_number]
        
        # Remove da lista da frequência atual
        del self.freq_to_items[freq][text_number]
        
        # Se a lista da frequência mínima ficou vazia, incrementa min_freq
        if not self.freq_to_items[freq] and freq == self.min_freq:
            self.min_freq += 1
        
        # Incrementa a frequência
        self.frequency[text_number] = freq + 1
        
        # Adiciona na lista da nova frequência
        self.freq_to_items[freq + 1][text_number] = None
    
    def _evict(self) -> int:
        """
        Remove o item menos frequentemente usado (Least Frequently Used)
        Em caso de empate, remove o menos recentemente usado
        
        Returns:
            int: número do texto que foi removido
        """
        if not self.cache:
            return None
        
        # Pega o primeiro item da frequência mínima (menos usado recentemente)
        items_with_min_freq = self.freq_to_items[self.min_freq]
        least_frequently_used = next(iter(items_with_min_freq))
        
        # Remove das estruturas auxiliares
        del items_with_min_freq[least_frequently_used]
        
        return least_frequently_used
    
    def clear(self):
        """Limpa o cache e reseta as métricas"""
        super().clear()
        self.frequency.clear()
        self.freq_to_items.clear()
        self.min_freq = 0
    
    def get_frequency_stats(self) -> dict:
        """
        Retorna estatísticas de frequência (útil para análise)
        
        Returns:
            dict: {text_number: frequency}
        """
        return dict(self.frequency)
    
    def get_items_by_frequency(self) -> dict:
        """
        Retorna itens agrupados por frequência
        
        Returns:
            dict: {frequency: [text_numbers]}
        """
        result = {}
        for freq, items in self.freq_to_items.items():
            if items:
                result[freq] = list(items.keys())
        return result
    
    def __str__(self) -> str:
        """Representação em string do cache"""
        freq_stats = self.get_frequency_stats()
        return f"LFUCache(capacity={self.capacity}, size={self.size()}, min_freq={self.min_freq}, freqs={freq_stats})"


# Testes e exemplos de uso
if __name__ == "__main__":
    print("="*70)
    print("TESTE DO ALGORITMO LFU (Least Frequently Used)")
    print("="*70)
    
    # Função mock para simular carregamento do disco
    def mock_loader(text_number):
        """Simula carregamento do disco com latência"""
        time.sleep(0.05)  # 50ms de latência
        content = f"Conteúdo simulado do texto {text_number} " * 100
        return content, 0.05
    
    # Cria um cache LFU com capacidade reduzida para facilitar o teste
    cache = LFUCache(capacity=3)
    
    print(f"\nCache criado: capacidade de {cache.capacity} textos\n")
    
    # Sequência de testes que demonstra o comportamento LFU
    # Texto 1 será acessado múltiplas vezes
    test_sequence = [1, 2, 3, 1, 1, 4, 2, 5]
    
    print("Sequência de requisições:", test_sequence)
    print("Observe como o texto 1 é acessado 3 vezes (alta frequência)\n")
    print("Executando requisições:\n")
    
    for i, text_num in enumerate(test_sequence, 1):
        content, load_time, was_hit = cache.get(text_num, mock_loader)
        
        status = "HIT ✓ " if was_hit else "MISS ✗"
        freq_stats = cache.get_frequency_stats()
        items_by_freq = cache.get_items_by_frequency()
        
        print(f"{i}. Texto {text_num}: {status} | "
              f"Tempo: {load_time:.4f}s")
        print(f"   Frequências: {freq_stats}")
        print(f"   Por frequência: {items_by_freq}")
        
        if i == 5:
            print("   ↑ Texto 1 tem frequência 3 (acessado 3 vezes)")
        elif i == 6:
            print("   ↑ Remove 3 (freq=1, menos usado), mantém 1 (freq=3)")
    
    # Exibe métricas finais
    print("\n" + "="*70)
    cache.print_metrics()