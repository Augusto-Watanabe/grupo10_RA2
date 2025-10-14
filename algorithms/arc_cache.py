"""
Implementação do algoritmo de cache ARC (Adaptive Replacement Cache)
Combina LRU e LFU com adaptação dinâmica ao padrão de acesso

Aluno - Algoritmo ARC
"""

from collections import OrderedDict
from typing import Tuple
import time
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar os módulos
sys.path.append(str(Path(__file__).parent.parent))

from core.cache_interface import CacheInterface


class ARCCache(CacheInterface):
    """
    Implementação do algoritmo ARC (Adaptive Replacement Cache).
    
    Funcionamento:
    - Mantém duas listas: LRU (recém acessados) e LFU (frequentemente acessados)
    - Mantém duas listas fantasmas: B1 (recém removidos de LRU) e B2 (recém removidos de LFU)
    - Usa um parâmetro p para balancear entre LRU e LFU
    - Adapta p dinamicamente baseado nos acertos nas listas fantasmas
    
    Exemplo de comportamento adaptativo:
    - Se muitos acertos em B1 (padrão de acesso sequencial): aumenta p, favorece LRU
    - Se muitos acertos em B2 (padrão de acesso repetitivo): diminui p, favorece LFU
    
    Vantagem: Adapta-se automaticamente ao padrão de acesso sem configuração manual
    """
    
    def __init__(self, capacity: int = 10):
        """
        Inicializa o cache ARC
        
        Args:
            capacity: capacidade máxima do cache (padrão: 10 textos)
        """
        super().__init__(capacity)
        
        # Listas principais (partição do cache real)
        self.LRU = OrderedDict()  # Recém acessados (uma vez)
        self.LFU = OrderedDict()  # Frequentemente acessados (mais de uma vez)
        
        # Listas fantasmas (apenas chaves, sem conteúdo)
        self.B1 = OrderedDict()  # Recém removidos de LRU
        self.B2 = OrderedDict()  # Recém removidos de LFU
        
        # Parâmetro de adaptação (balanceia entre LRU e LFU)
        self.p = 0
        
        # Tamanho alvo para LRU (LFU terá capacity - target_LRU_size)
        self.target_LRU_size = 0
        
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
        
        # CASE 1: HIT em LRU ou LFU (texto está no cache)
        if text_number in self.LRU or text_number in self.LFU:
            self.hits += 1
            self._handle_cache_hit(text_number)
            
            # Recupera o conteúdo
            if text_number in self.LRU:
                content = self.LRU[text_number]
            else:
                content = self.LFU[text_number]
                
            load_time = time.time() - start_time
            self.load_times.append(load_time)
            return content, load_time, True
        
        # CASE 2: HIT em B1 (texto foi removido recentemente de LRU)
        elif text_number in self.B1:
            self._handle_ghost_hit_B1(text_number)
            
        # CASE 3: HIT em B2 (texto foi removido recentemente de LFU)  
        elif text_number in self.B2:
            self._handle_ghost_hit_B2(text_number)
        
        # CASE 4: MISS completo (não está em nenhuma lista)
        else:
            self.misses += 1
        
        # Se necessário, faz evicção para liberar espaço
        if self._should_evict():
            self._evict()
        
        # Carrega o texto do disco
        content, disk_load_time = loader_function(text_number)
        
        # Adiciona ao cache na lista apropriada
        self._add_to_cache(text_number, content)
        
        total_time = time.time() - start_time
        self.load_times.append(total_time)
        
        return content, total_time, False
    
    def _handle_cache_hit(self, text_number: int):
        """
        Processa um acerto no cache (texto estava em LRU ou LFU)
        """
        if text_number in self.LRU:
            # Move de LRU para LFU (agora é frequentemente acessado)
            content = self.LRU.pop(text_number)
            self.LFU[text_number] = content
        elif text_number in self.LFU:
            # Já está em LFU, apenas marca como recentemente usado
            self.LFU.move_to_end(text_number)
    
    def _handle_ghost_hit_B1(self, text_number: int):
        """
        Processa acerto em B1 (padrão de acesso sequencial detectado)
        """
        # Aumenta p para favorecer LRU (acesso sequencial)
        delta = 1
        if len(self.B2) > len(self.B1):
            delta = len(self.B2) // len(self.B1)
        self.p = min(self.p + delta, self.capacity)
        
        # Remove de B1
        if text_number in self.B1:
            del self.B1[text_number]
    
    def _handle_ghost_hit_B2(self, text_number: int):
        """
        Processa acerto em B2 (padrão de acesso repetitivo detectado)
        """
        # Diminui p para favorecer LFU (acesso repetitivo)
        delta = 1
        if len(self.B1) > len(self.B2):
            delta = len(self.B1) // len(self.B2)
        self.p = max(self.p - delta, 0)
        
        # Remove de B2
        if text_number in self.B2:
            del self.B2[text_number]
    
    def _should_evict(self) -> bool:
        """
        Verifica se é necessário fazer evicção
        """
        total_LRU_size = len(self.LRU) + len(self.B1)
        return total_LRU_size >= self.capacity
    
    def _evict(self):
        """
        Remove itens seguindo a política ARC
        """
        # LRU tem mais itens que o tamanho alvo
        if len(self.LRU) > self.target_LRU_size:
            # Remove de LRU (LRU)
            if self.LRU:
                oldest, content = self.LRU.popitem(last=False)
                self.B1[oldest] = None
                # Limita tamanho de B1
                if len(self.B1) > self.capacity:
                    self.B1.popitem(last=False)
        else:
            # Remove de LFU (LRU)
            if self.LFU:
                oldest, content = self.LFU.popitem(last=False)
                self.B2[oldest] = None
                # Limita tamanho de B2
                if len(self.B2) > self.capacity:
                    self.B2.popitem(last=False)
    
    def _add_to_cache(self, text_number: int, content: str):
        """
        Adiciona um novo item ao cache na lista apropriada
        """
        # Se veio de B2, vai para LFU (era frequentemente acessado)
        if text_number in self.B2:
            self.LFU[text_number] = content
        # Caso contrário, vai para LRU (novo acesso)
        else:
            self.LRU[text_number] = content
        
        # Atualiza tamanho alvo de LRU baseado em p
        self.target_LRU_size = self.p
    
    def is_in_cache(self, text_number: int) -> bool:
        """
        Verifica se um texto está no cache (LRU ou LFU)
        """
        return text_number in self.LRU or text_number in self.LFU
    
    def is_full(self) -> bool:
        """
        Verifica se o cache está cheio (LRU + LFU atingiu capacidade)
        """
        return len(self.LRU) + len(self.LFU) >= self.capacity
    
    def size(self) -> int:
        """
        Retorna o número de itens atualmente no cache
        """
        return len(self.LRU) + len(self.LFU)
    
    def clear(self):
        """
        Limpa o cache e reseta as métricas
        """
        super().clear()
        self.LRU.clear()
        self.LFU.clear()
        self.B1.clear()
        self.B2.clear()
        self.p = 0
        self.target_LRU_size = 0
    
    def get_cache_state(self) -> dict:
        """
        Retorna o estado interno do cache (útil para debugging)
        
        Returns:
            dict: estado das listas LRU, LFU, B1, B2 e parâmetros
        """
        return {
            'LRU': list(self.LRU.keys()),
            'LFU': list(self.LFU.keys()),
            'B1': list(self.B1.keys()),
            'B2': list(self.B2.keys()),
            'p': self.p,
            'target_LRU_size': self.target_LRU_size,
            'total_size': self.size()
        }
    
    def __str__(self) -> str:
        """Representação em string do cache"""
        state = self.get_cache_state()
        return (f"ARCCache(capacity={self.capacity}, size={self.size()}, "
                f"p={self.p}, LRU={len(self.LRU)}, LFU={len(self.LFU)})")


# Testes e exemplos de uso
if __name__ == "__main__":
    print("="*70)
    print("TESTE DO ALGORITMO ARC (Adaptive Replacement Cache)")
    print("="*70)
    
    # Função mock para simular carregamento do disco
    def mock_loader(text_number):
        """Simula carregamento do disco com latência"""
        time.sleep(0.05)  # 50ms de latência
        content = f"Conteúdo simulado do texto {text_number} " * 100
        return content, 0.05
    
    # Cria um cache ARC com capacidade reduzida para facilitar o teste
    cache = ARCCache(capacity=4)
    
    print(f"\nCache criado: {cache}")
    print(f"Capacidade: {cache.capacity} textos\n")
    
    # Sequência de testes que demonstra o comportamento adaptativo do ARC
    # Mistura acesso sequencial (1,2,3,4) e repetitivo (1,1,2,2)
    test_sequence = [1, 2, 3, 1, 1, 2, 2, 4, 5, 1, 6]
    
    print("Sequência de requisições:", test_sequence)
    print("Observe como o ARC se adapta aos padrões de acesso\n")
    print("Executando requisições:\n")
    
    for i, text_num in enumerate(test_sequence, 1):
        content, load_time, was_hit = cache.get(text_num, mock_loader)
        
        status = "HIT ✓ " if was_hit else "MISS ✗"
        state = cache.get_cache_state()
        
        print(f"{i}. Texto {text_num}: {status} | "
              f"Tempo: {load_time:.4f}s")
        print(f"   Estado: LRU={state['LRU']}, LFU={state['LFU']}")
        print(f"   Fantasmas: B1={state['B1']}, B2={state['B2']}")
        print(f"   Parâmetro p: {state['p']}")
        
        if i == 4:
            print("   ↑ Texto 1 acessado novamente - move de LRU para LFU")
        elif i == 8:
            print("   ↑ Acesso sequencial detectado - p aumenta")
        elif i == 10:
            print("   ↑ Acesso repetitivo detectado - p diminui")
    
    # Exibe métricas finais
    print("\n" + "="*70)
    cache.print_metrics()
    
    # Análise detalhada
    print("="*70)
    final_state = cache.get_cache_state()
    print("Estado final:")
    print(f"  LRU (recém acessados): {final_state['LRU']}")
    print(f"  LFU (frequentemente acessados): {final_state['LFU']}")
    print(f"  B1 (fantasmas LRU): {final_state['B1']}")
    print(f"  B2 (fantasmas LFU): {final_state['B2']}")
    print(f"  Parâmetro p: {final_state['p']}")
    print("="*70)