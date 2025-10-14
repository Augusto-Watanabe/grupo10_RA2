"""
Motor de simulação para testar algoritmos de cache
Simula múltiplos usuários com diferentes padrões de acesso

Aluno D - Módulo de Simulação
"""

import time
from typing import Dict, List, Tuple
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from simulation.request_generator import RequestGenerator
from core.text_loader import TextLoader


class SimulationEngine:
    """
    Motor de simulação para testar e comparar algoritmos de cache
    """
    
    def __init__(self, text_loader: TextLoader):
        """
        Inicializa o motor de simulação
        
        Args:
            text_loader: instância do carregador de textos
        """
        self.loader = text_loader
        self.results = []
    
    def simulate_user(self, cache, requests: List[int], 
                     user_id: int, pattern: str) -> Dict:
        """
        Simula um único usuário acessando textos
        
        Args:
            cache: instância do algoritmo de cache
            requests: lista de números de textos a acessar
            user_id: identificador do usuário
            pattern: padrão de acesso usado
            
        Returns:
            dict: métricas coletadas durante a simulação
        """
        # Limpa o cache antes de começar
        cache.clear()
        
        # Função wrapper para o loader
        def load_from_disk(num):
            return self.loader.load_text(num)
        
        # Coleta de dados
        access_log = []
        text_miss_count = {}  # Conta misses por texto
        text_hit_count = {}   # Conta hits por texto
        
        print(f"  Simulando Usuário {user_id} com padrão '{pattern}'...")
        
        start_time = time.time()
        
        for request_num, text_num in enumerate(requests, 1):
            # Executa o acesso
            content, load_time, was_hit = cache.get(text_num, load_from_disk)
            
            # Registra o acesso
            access_log.append({
                'request_num': request_num,
                'text_num': text_num,
                'was_hit': was_hit,
                'load_time': load_time
            })
            
            # Conta hits e misses por texto
            if was_hit:
                text_hit_count[text_num] = text_hit_count.get(text_num, 0) + 1
            else:
                text_miss_count[text_num] = text_miss_count.get(text_num, 0) + 1
        
        total_time = time.time() - start_time
        
        # Coleta métricas finais
        metrics = cache.get_metrics()
        
        result = {
            'user_id': user_id,
            'pattern': pattern,
            'algorithm': cache.__class__.__name__,
            'total_requests': len(requests),
            'hits': metrics['hits'],
            'misses': metrics['misses'],
            'hit_rate': metrics['hit_rate'],
            'miss_rate': metrics['miss_rate'],
            'avg_load_time': metrics['avg_load_time'],
            'total_load_time': metrics['total_load_time'],
            'simulation_time': total_time,
            'access_log': access_log,
            'text_miss_count': text_miss_count,
            'text_hit_count': text_hit_count
        }
        
        print(f"    ✓ Concluído: {metrics['hits']} hits, "
              f"{metrics['misses']} misses ({metrics['hit_rate']:.1f}% hit rate)")
        
        return result
    
    def simulate_algorithm(self, cache_class, cache_capacity: int = 10,
                          num_users: int = 3, requests_per_user: int = 200) -> List[Dict]:
        """
        Simula um algoritmo com múltiplos usuários e padrões
        
        Args:
            cache_class: classe do algoritmo de cache
            cache_capacity: capacidade do cache
            num_users: número de usuários a simular por padrão
            requests_per_user: número de requisições por usuário
            
        Returns:
            list: lista de resultados de todas as simulações
        """
        algorithm_name = cache_class.__name__
        print(f"\n{'='*70}")
        print(f"Simulando algoritmo: {algorithm_name}")
        print(f"{'='*70}")
        
        patterns = ['random', 'poisson', 'weighted']
        results = []
        
        for pattern in patterns:
            print(f"\nPadrão de acesso: {pattern.upper()}")
            
            for user_id in range(1, num_users + 1):
                # Cria nova instância do cache para cada usuário
                cache = cache_class(capacity=cache_capacity)
                
                # Gera requisições para este usuário
                generator = RequestGenerator(total_texts=100, seed=user_id * 100)
                requests = generator.generate_user_requests(requests_per_user, pattern)
                
                # Simula o usuário
                result = self.simulate_user(cache, requests, user_id, pattern)
                results.append(result)
        
        print(f"\n✓ Simulação de {algorithm_name} concluída!")
        print(f"  Total de cenários testados: {len(results)}")
        
        return results
    
    def simulate_all_algorithms(self, algorithms: List, 
                               cache_capacity: int = 10,
                               num_users: int = 3, 
                               requests_per_user: int = 200) -> Dict[str, List[Dict]]:
        """
        Simula todos os algoritmos fornecidos
        
        Args:
            algorithms: lista de classes de algoritmos de cache
            cache_capacity: capacidade do cache
            num_users: número de usuários por padrão
            requests_per_user: número de requisições por usuário
            
        Returns:
            dict: resultados organizados por algoritmo
        """
        print("\n" + "🚀"*35)
        print("INICIANDO SIMULAÇÃO COMPLETA")
        print("🚀"*35)
        print(f"\nConfigurações:")
        print(f"  Capacidade do cache: {cache_capacity} textos")
        print(f"  Usuários por padrão: {num_users}")
        print(f"  Requisições por usuário: {requests_per_user}")
        print(f"  Padrões de acesso: random, poisson, weighted")
        print(f"  Algoritmos: {', '.join([alg.__name__ for alg in algorithms])}")
        
        all_results = {}
        
        for cache_class in algorithms:
            results = self.simulate_algorithm(
                cache_class, 
                cache_capacity, 
                num_users, 
                requests_per_user
            )
            all_results[cache_class.__name__] = results
        
        print("\n" + "="*70)
        print("✅ SIMULAÇÃO COMPLETA CONCLUÍDA")
        print("="*70)
        
        # Salva resultados
        self.results = all_results
        
        return all_results
    
    def get_summary_statistics(self) -> Dict:
        """
        Calcula estatísticas resumidas dos resultados
        
        Returns:
            dict: estatísticas por algoritmo e padrão
        """
        if not self.results:
            return {}
        
        summary = {}
        
        for algorithm, results in self.results.items():
            summary[algorithm] = {}
            
            # Agrupa por padrão
            patterns = set(r['pattern'] for r in results)
            
            for pattern in patterns:
                pattern_results = [r for r in results if r['pattern'] == pattern]
                
                summary[algorithm][pattern] = {
                    'avg_hit_rate': sum(r['hit_rate'] for r in pattern_results) / len(pattern_results),
                    'avg_miss_rate': sum(r['miss_rate'] for r in pattern_results) / len(pattern_results),
                    'avg_load_time': sum(r['avg_load_time'] for r in pattern_results) / len(pattern_results),
                    'total_hits': sum(r['hits'] for r in pattern_results),
                    'total_misses': sum(r['misses'] for r in pattern_results),
                    'num_users': len(pattern_results)
                }
        
        return summary
    
    def print_summary(self):
        """Exibe um resumo dos resultados"""
        summary = self.get_summary_statistics()
        
        if not summary:
            print("Nenhum resultado disponível para resumo.")
            return
        
        print("\n" + "="*70)
        print("RESUMO DOS RESULTADOS")
        print("="*70)
        
        patterns = ['random', 'poisson', 'weighted']
        
        for pattern in patterns:
            print(f"\n{'='*70}")
            print(f"Padrão: {pattern.upper()}")
            print(f"{'='*70}")
            print(f"{'Algoritmo':<15} {'Hit Rate':<12} {'Avg Time':<12} {'Hits':<10} {'Misses':<10}")
            print("-"*70)
            
            for algorithm, patterns_data in summary.items():
                if pattern in patterns_data:
                    data = patterns_data[pattern]
                    print(f"{algorithm:<15} "
                          f"{data['avg_hit_rate']:>6.2f}%     "
                          f"{data['avg_load_time']:>8.4f}s    "
                          f"{data['total_hits']:<10} "
                          f"{data['total_misses']:<10}")
            
            # Determina o melhor algoritmo para este padrão
            best_algo = max(summary.items(), 
                           key=lambda x: x[1].get(pattern, {}).get('avg_hit_rate', 0))
            if pattern in best_algo[1]:
                print(f"\n🏆 Melhor: {best_algo[0]} "
                      f"({best_algo[1][pattern]['avg_hit_rate']:.2f}% hit rate)")


# Teste do motor de simulação
if __name__ == "__main__":
    from algorithms.fifo_cache import FIFOCache
    from algorithms.lru_cache import LRUCache
    from algorithms.lfu_cache import LFUCache
    
    print("="*70)
    print("TESTE DO MOTOR DE SIMULAÇÃO")
    print("="*70)
    
    # Carregador de textos (mock para teste)
    class MockLoader:
        def load_text(self, num):
            time.sleep(0.01)  # Simula latência
            return f"Conteúdo do texto {num}", 0.01
    
    loader = MockLoader()
    engine = SimulationEngine(loader)
    
    # Simula com parâmetros reduzidos para teste rápido
    algorithms = [FIFOCache, LRUCache, LFUCache]
    
    results = engine.simulate_all_algorithms(
        algorithms,
        cache_capacity=5,
        num_users=2,  # Reduzido para teste
        requests_per_user=50  # Reduzido para teste
    )
    
    # Exibe resumo
    engine.print_summary()
    
    print("\n" + "="*70)
    print("Teste concluído! ✅")
    print("="*70)