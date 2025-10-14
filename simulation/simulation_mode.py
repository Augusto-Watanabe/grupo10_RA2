"""
Modo de simulação completo para análise de algoritmos de cache
Integra geração de requisições, simulação e relatórios

Aluno D - Módulo de Simulação
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from simulation.simulation_engine import SimulationEngine
from simulation.report_generator import ReportGenerator
from core.text_loader import TextLoader
from algorithms.fifo_cache import FIFOCache
from algorithms.lru_cache import LRUCache
from algorithms.lfu_cache import LFUCache
from algorithms.arc_cache import ARCCache


def run_simulation_mode(loader: TextLoader, 
                       cache_capacity: int = 10,
                       num_users: int = 3,
                       requests_per_user: int = 200):
    """
    Executa o modo de simulação completo
    
    Args:
        loader: instância do TextLoader
        cache_capacity: capacidade do cache
        num_users: número de usuários por padrão
        requests_per_user: número de requisições por usuário
    """
    print("\n" + "🎯"*35)
    print("MODO DE SIMULAÇÃO ATIVADO")
    print("🎯"*35)
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    SISTEMA DE ANÁLISE DE CACHE                   ║
║                                                                  ║
║  Este modo irá:                                                  ║
║  • Simular 3 usuários para cada algoritmo                        ║
║  • Testar 3 padrões de acesso diferentes                         ║
║  • Medir cache hits, misses e tempos de carregamento             ║
║  • Gerar relatórios visuais comparativos                         ║
║                                                                  ║
║  Algoritmos a serem testados:                                    ║
║    ✓ FIFO (First In, First Out)                                 ║
║    ✓ LRU (Least Recently Used)                                  ║
║    ✓ LFU (Least Frequently Used)                                ║
║    ✓ ARC (Adaptive Replacement Cache) ⭐ Avançado              ║
║                                                                  ║
║  Padrões de acesso:                                              ║
║    • Aleatório: distribuição uniforme                            ║
║    • Poisson: distribuição com λ=30                              ║
║    • Ponderado: textos 30-40 com 43% de probabilidade            ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    input("Pressione ENTER para iniciar a simulação...")
    
    # Inicializa componentes
    print("\n📊 Inicializando simulação...")
    engine = SimulationEngine(loader)
    
    # Define algoritmos a serem testados
    algorithms = [FIFOCache, LRUCache, LFUCache, ARCCache]
    
    # Executa simulação
    try:
        results = engine.simulate_all_algorithms(
            algorithms,
            cache_capacity=cache_capacity,
            num_users=num_users,
            requests_per_user=requests_per_user
        )
        
        # Exibe resumo textual
        engine.print_summary()
        
        # Gera relatórios visuais
        print("\n📈 Gerando relatórios visuais...")
        report_gen = ReportGenerator(output_dir="docs")
        report_gen.generate_full_report(results)
        
        # Análise e recomendação
        print_recommendation(engine.get_summary_statistics())
        
        print("\n" + "="*70)
        print("✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*70)
        print("\nPróximos passos:")
        print("  1. Verifique os gráficos gerados em: docs/")
        print("  2. Analise o resumo acima para escolher o melhor algoritmo")
        print("  3. Configure o algoritmo escolhido para uso em produção")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulação interrompida pelo usuário.")
        print("Dados parciais podem ter sido salvos.")
    except Exception as e:
        print(f"\n\n❌ Erro durante a simulação: {e}")
        import traceback
        traceback.print_exc()


def print_recommendation(summary: dict):
    """
    Analisa resultados e imprime recomendação de algoritmo
    
    Args:
        summary: estatísticas resumidas dos resultados
    """
    print("\n" + "="*70)
    print("🎯 ANÁLISE E RECOMENDAÇÃO")
    print("="*70)
    
    if not summary:
        print("Sem dados suficientes para recomendação.")
        return
    
    # Calcula hit rate médio geral de cada algoritmo
    overall_performance = {}
    
    for algorithm, patterns_data in summary.items():
        total_hit_rate = 0
        count = 0
        
        for pattern, data in patterns_data.items():
            total_hit_rate += data['avg_hit_rate']
            count += 1
        
        if count > 0:
            overall_performance[algorithm] = total_hit_rate / count
    
    # Ordena por performance
    sorted_algos = sorted(overall_performance.items(), 
                         key=lambda x: x[1], reverse=True)
    
    print("\n📊 Ranking Geral (Hit Rate Médio):\n")
    
    medals = ["🥇", "🥈", "🥉", "  "]
    
    for i, (algorithm, hit_rate) in enumerate(sorted_algos):
        medal = medals[min(i, 3)]
        bar_length = int(hit_rate / 2)
        bar = "█" * bar_length
        print(f"{medal} {algorithm:<15} {hit_rate:>6.2f}% {bar}")
    
    # Recomendação baseada em cenário
    print("\n" + "-"*70)
    print("💡 RECOMENDAÇÕES POR CENÁRIO:")
    print("-"*70)
    
    best_by_pattern = {}
    for pattern in ['random', 'poisson', 'weighted']:
        best = max(summary.items(),
                  key=lambda x: x[1].get(pattern, {}).get('avg_hit_rate', 0))
        best_by_pattern[pattern] = (best[0], 
                                    best[1].get(pattern, {}).get('avg_hit_rate', 0))
    
    print(f"""
1. Para acesso ALEATÓRIO (navegação exploratória):
   → Melhor: {best_by_pattern['random'][0]} ({best_by_pattern['random'][1]:.1f}% hit rate)
   
2. Para acesso com POISSON (padrão com concentração):
   → Melhor: {best_by_pattern['poisson'][0]} ({best_by_pattern['poisson'][1]:.1f}% hit rate)
   
3. Para acesso PONDERADO (documentos favoritos):
   → Melhor: {best_by_pattern['weighted'][0]} ({best_by_pattern['weighted'][1]:.1f}% hit rate)
    """)
    
    print("-"*70)
    print("🏆 RECOMENDAÇÃO FINAL PARA 'TEXTO É VIDA':")
    print("-"*70)
    
    best_overall = sorted_algos[0]
    
    print(f"""
Algoritmo Recomendado: {best_overall[0]}
Hit Rate Médio: {best_overall[1]:.2f}%

Justificativa:
• Advogados tendem a revisitar documentos importantes (padrão ponderado)
• Há documentos de referência frequentemente consultados
• O padrão de acesso não é puramente sequencial

{get_algorithm_description(best_overall[0])}

Configuração Sugerida:
• Capacidade do cache: 10 textos (balança memória e performance)
• Considere aumentar para 15-20 se houver memória disponível
• Monitore métricas em produção para ajustes
    """)
    
    print("="*70)


def get_algorithm_description(algorithm_name: str) -> str:
    """Retorna descrição do algoritmo"""
    descriptions = {
        'FIFOCache': """
Características do FIFO:
✓ Simples e previsível
✓ Baixo overhead de processamento
✗ Não considera padrão de reutilização
→ Melhor para acesso sequencial único""",
        
        'LRUCache': """
Características do LRU:
✓ Excelente para localidade temporal
✓ Adapta-se bem a mudanças
✓ Bom equilíbrio geral
→ Melhor escolha para a maioria dos casos""",
        
        'LFUCache': """
Características do LFU:
✓ Protege itens muito acessados
✓ Ideal para "hot items"
✓ Resistente a scans
→ Melhor para documentos de referência""",
        
        'ARCCache': """
Características do ARC:
✓ Adapta-se automaticamente
✓ Combina vantagens de LRU e LFU
✓ Estado-da-arte em caching
✓ Usado em sistemas reais (ZFS, PostgreSQL)
→ Melhor performance adaptativa"""
    }
    
    return descriptions.get(algorithm_name, "")


# Execução standalone para testes
if __name__ == "__main__":
    print("="*70)
    print("TESTE DO MODO DE SIMULAÇÃO")
    print("="*70)
    
    # Mock loader para teste rápido
    class MockLoader:
        def load_text(self, num):
            import time
            time.sleep(0.001)
            return f"Conteúdo do texto {num} " * 200, 0.001
    
    loader = MockLoader()
    
    # Executa com parâmetros reduzidos para teste
    run_simulation_mode(
        loader,
        cache_capacity=5,
        num_users=2,  # Reduzido para teste rápido
        requests_per_user=50  # Reduzido para teste rápido
    )