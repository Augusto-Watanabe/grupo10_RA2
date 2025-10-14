"""
Gerador de relatórios e gráficos para análise de performance dos algoritmos
Cria visualizações comparativas salvos em /docs/

Aluno D - Módulo de Simulação
"""

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import defaultdict
import numpy as np


class ReportGenerator:
    """
    Classe para gerar relatórios e gráficos de análise de cache
    """
    
    def __init__(self, output_dir: str = "docs"):
        """
        Inicializa o gerador de relatórios
        
        Args:
            output_dir: diretório onde os gráficos serão salvos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Configuração de estilo
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10
    
    def generate_hit_rate_comparison(self, results: dict, filename: str = "hit_rate_comparison.png"):
        """
        Gera gráfico comparando hit rate entre algoritmos e padrões
        
        Args:
            results: dicionário com resultados {algorithm: [user_results]}
            filename: nome do arquivo de saída
        """
        # Prepara dados
        data = defaultdict(lambda: defaultdict(list))
        
        for algorithm, user_results in results.items():
            for result in user_results:
                pattern = result['pattern']
                hit_rate = result['hit_rate']
                data[algorithm][pattern].append(hit_rate)
        
        # Calcula médias
        algorithms = list(data.keys())
        patterns = ['random', 'poisson', 'weighted']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(patterns))
        width = 0.2
        multiplier = 0
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        
        for i, algorithm in enumerate(algorithms):
            means = [np.mean(data[algorithm][p]) if p in data[algorithm] else 0 
                    for p in patterns]
            offset = width * multiplier
            bars = ax.bar(x + offset, means, width, label=algorithm, 
                         color=colors[i % len(colors)], alpha=0.8)
            
            # Adiciona valores nas barras
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}%',
                       ha='center', va='bottom', fontsize=9)
            
            multiplier += 1
        
        ax.set_xlabel('Padrão de Acesso', fontsize=12, fontweight='bold')
        ax.set_ylabel('Hit Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Comparação de Hit Rate por Algoritmo e Padrão de Acesso', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x + width * (len(algorithms) - 1) / 2)
        ax.set_xticklabels([p.capitalize() for p in patterns])
        ax.legend(loc='upper left', framealpha=0.9)
        ax.set_ylim(0, max([max(means) for means in 
                           [[np.mean(data[a][p]) if p in data[a] else 0 
                             for p in patterns] for a in algorithms]]) * 1.2)
        
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {filename}")
    
    def generate_load_time_comparison(self, results: dict, filename: str = "load_time_comparison.png"):
        """
        Gera gráfico comparando tempo médio de carregamento
        
        Args:
            results: dicionário com resultados
            filename: nome do arquivo de saída
        """
        # Prepara dados
        data = defaultdict(lambda: defaultdict(list))
        
        for algorithm, user_results in results.items():
            for result in user_results:
                pattern = result['pattern']
                avg_time = result['avg_load_time']
                data[algorithm][pattern].append(avg_time)
        
        algorithms = list(data.keys())
        patterns = ['random', 'poisson', 'weighted']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(patterns))
        width = 0.2
        multiplier = 0
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        
        for i, algorithm in enumerate(algorithms):
            means = [np.mean(data[algorithm][p]) * 1000 if p in data[algorithm] else 0 
                    for p in patterns]  # Converte para ms
            offset = width * multiplier
            bars = ax.bar(x + offset, means, width, label=algorithm, 
                         color=colors[i % len(colors)], alpha=0.8)
            
            # Adiciona valores
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}',
                       ha='center', va='bottom', fontsize=9)
            
            multiplier += 1
        
        ax.set_xlabel('Padrão de Acesso', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tempo Médio de Carregamento (ms)', fontsize=12, fontweight='bold')
        ax.set_title('Comparação de Tempo de Carregamento por Algoritmo', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x + width * (len(algorithms) - 1) / 2)
        ax.set_xticklabels([p.capitalize() for p in patterns])
        ax.legend(loc='upper left', framealpha=0.9)
        
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {filename}")
    
    def generate_miss_distribution(self, results: dict, filename: str = "miss_distribution.png"):
        """
        Gera gráfico mostrando distribuição de misses por texto
        
        Args:
            results: dicionário com resultados
            filename: nome do arquivo de saída
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Distribuição de Cache Misses por Texto', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        algorithms = list(results.keys())[:4]  # Máximo 4 algoritmos
        
        for idx, algorithm in enumerate(algorithms):
            ax = axes[idx // 2, idx % 2]
            
            # Agrega misses de todos os usuários
            total_misses = defaultdict(int)
            
            for result in results[algorithm]:
                for text_num, count in result['text_miss_count'].items():
                    total_misses[text_num] += count
            
            if total_misses:
                # Ordena por número do texto
                texts = sorted(total_misses.keys())
                misses = [total_misses[t] for t in texts]
                
                # Destaca textos 30-40 (região "quente")
                colors = ['#e74c3c' if 30 <= t <= 40 else '#3498db' for t in texts]
                
                ax.bar(texts, misses, color=colors, alpha=0.7, width=0.8)
                ax.set_xlabel('Número do Texto', fontsize=11, fontweight='bold')
                ax.set_ylabel('Total de Cache Misses', fontsize=11, fontweight='bold')
                ax.set_title(f'{algorithm}', fontsize=12, fontweight='bold')
                ax.grid(axis='y', alpha=0.3)
                
                # Marca a região 30-40
                ax.axvspan(30, 40, alpha=0.1, color='red', label='Região 30-40 (43% prob.)')
                ax.legend(loc='upper right', fontsize=9)
            else:
                ax.text(0.5, 0.5, 'Sem dados', ha='center', va='center',
                       transform=ax.transAxes, fontsize=14)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {filename}")
    
    def generate_pattern_comparison(self, results: dict, filename: str = "pattern_comparison.png"):
        """
        Gera gráfico comparando performance em diferentes padrões
        
        Args:
            results: dicionário com resultados
            filename: nome do arquivo de saída
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle('Performance por Padrão de Acesso', 
                    fontsize=16, fontweight='bold')
        
        patterns = ['random', 'poisson', 'weighted']
        pattern_names = ['Aleatório', 'Poisson (λ=30)', 'Ponderado (30-40: 43%)']
        
        for idx, (pattern, pattern_name) in enumerate(zip(patterns, pattern_names)):
            ax = axes[idx]
            
            # Coleta dados para este padrão
            algorithms = []
            hit_rates = []
            miss_rates = []
            
            for algorithm, user_results in results.items():
                pattern_results = [r for r in user_results if r['pattern'] == pattern]
                if pattern_results:
                    algorithms.append(algorithm)
                    avg_hit = np.mean([r['hit_rate'] for r in pattern_results])
                    avg_miss = np.mean([r['miss_rate'] for r in pattern_results])
                    hit_rates.append(avg_hit)
                    miss_rates.append(avg_miss)
            
            # Gráfico de barras empilhadas
            x = np.arange(len(algorithms))
            width = 0.6
            
            bars1 = ax.bar(x, hit_rates, width, label='Hit Rate', 
                          color='#2ecc71', alpha=0.8)
            bars2 = ax.bar(x, miss_rates, width, bottom=hit_rates,
                          label='Miss Rate', color='#e74c3c', alpha=0.8)
            
            # Adiciona valores
            for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
                # Hit rate
                height1 = bar1.get_height()
                ax.text(bar1.get_x() + bar1.get_width()/2., height1/2,
                       f'{height1:.1f}%', ha='center', va='center',
                       fontsize=10, fontweight='bold', color='white')
                # Miss rate
                height2 = bar2.get_height()
                ax.text(bar2.get_x() + bar2.get_width()/2., 
                       height1 + height2/2, f'{height2:.1f}%',
                       ha='center', va='center', fontsize=10, 
                       fontweight='bold', color='white')
            
            ax.set_ylabel('Percentual (%)', fontsize=11, fontweight='bold')
            ax.set_title(pattern_name, fontsize=12, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(algorithms, rotation=0)
            ax.set_ylim(0, 105)
            ax.legend(loc='upper right', framealpha=0.9)
            ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {filename}")
    
    def generate_performance_heatmap(self, results: dict, filename: str = "performance_heatmap.png"):
        """
        Gera heatmap de performance (algoritmo x padrão)
        
        Args:
            results: dicionário com resultados
            filename: nome do arquivo de saída
        """
        # Prepara dados para heatmap
        algorithms = list(results.keys())
        patterns = ['random', 'poisson', 'weighted']
        
        heatmap_data = []
        
        for algorithm in algorithms:
            row = []
            for pattern in patterns:
                pattern_results = [r for r in results[algorithm] 
                                 if r['pattern'] == pattern]
                if pattern_results:
                    avg_hit_rate = np.mean([r['hit_rate'] for r in pattern_results])
                    row.append(avg_hit_rate)
                else:
                    row.append(0)
            heatmap_data.append(row)
        
        # Cria heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        
        im = ax.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
        
        # Configurações
        ax.set_xticks(np.arange(len(patterns)))
        ax.set_yticks(np.arange(len(algorithms)))
        ax.set_xticklabels([p.capitalize() for p in patterns], fontsize=11)
        ax.set_yticklabels(algorithms, fontsize=11)
        
        # Adiciona valores nas células
        for i in range(len(algorithms)):
            for j in range(len(patterns)):
                text = ax.text(j, i, f'{heatmap_data[i][j]:.1f}%',
                             ha="center", va="center", color="black",
                             fontsize=12, fontweight='bold')
        
        ax.set_title('Heatmap de Hit Rate: Algoritmo vs Padrão de Acesso',
                    fontsize=14, fontweight='bold', pad=20)
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Hit Rate (%)', rotation=270, labelpad=20, fontsize=11)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {filename}")
    
    def generate_top_texts_analysis(self, results: dict, filename: str = "top_texts_analysis.png"):
        """
        Analisa os textos mais e menos acessados
        
        Args:
            results: dicionário com resultados
            filename: nome do arquivo de saída
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análise dos Textos Mais Solicitados', 
                    fontsize=16, fontweight='bold')
        
        algorithms = list(results.keys())[:4]
        
        for idx, algorithm in enumerate(algorithms):
            ax = axes[idx // 2, idx % 2]
            
            # Conta total de acessos por texto
            total_accesses = defaultdict(int)
            
            for result in results[algorithm]:
                for access in result['access_log']:
                    total_accesses[access['text_num']] += 1
            
            if total_accesses:
                # Top 20 textos mais acessados
                top_texts = sorted(total_accesses.items(), 
                                  key=lambda x: x[1], reverse=True)[:20]
                
                texts = [t[0] for t in top_texts]
                counts = [t[1] for t in top_texts]
                
                # Destaca textos 30-40
                colors = ['#e74c3c' if 30 <= t <= 40 else '#3498db' 
                         for t in texts]
                
                bars = ax.barh(range(len(texts)), counts, color=colors, alpha=0.7)
                ax.set_yticks(range(len(texts)))
                ax.set_yticklabels([f'Texto {t}' for t in texts], fontsize=9)
                ax.set_xlabel('Número de Acessos', fontsize=11, fontweight='bold')
                ax.set_title(f'{algorithm} - Top 20 Textos', 
                           fontsize=12, fontweight='bold')
                ax.grid(axis='x', alpha=0.3)
                
                # Adiciona valores
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    ax.text(width, bar.get_y() + bar.get_height()/2,
                           f' {int(width)}', ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico salvo: {filename}")
    
    def generate_full_report(self, results: dict):
        """
        Gera relatório completo com todos os gráficos
        
        Args:
            results: dicionário com resultados da simulação
        """
        print("\n" + "="*70)
        print("GERANDO RELATÓRIO COMPLETO")
        print("="*70)
        print(f"Diretório de saída: {self.output_dir.absolute()}\n")
        
        self.generate_hit_rate_comparison(results)
        self.generate_load_time_comparison(results)
        self.generate_miss_distribution(results)
        self.generate_pattern_comparison(results)
        self.generate_performance_heatmap(results)
        self.generate_top_texts_analysis(results)
        
        print("\n" + "="*70)
        print("✅ RELATÓRIO COMPLETO GERADO COM SUCESSO!")
        print("="*70)
        print(f"\nArquivos gerados em: {self.output_dir.absolute()}")
        print("  • hit_rate_comparison.png")
        print("  • load_time_comparison.png")
        print("  • miss_distribution.png")
        print("  • pattern_comparison.png")
        print("  • performance_heatmap.png")
        print("  • top_texts_analysis.png")
        print("="*70)


# Teste do gerador de relatórios
if __name__ == "__main__":
    print("="*70)
    print("TESTE DO GERADOR DE RELATÓRIOS")
    print("="*70)
    
    # Dados mockados para teste
    mock_results = {
        'FIFOCache': [
            {
                'user_id': 1, 'pattern': 'random', 'algorithm': 'FIFOCache',
                'hits': 45, 'misses': 155, 'hit_rate': 22.5, 'miss_rate': 77.5,
                'avg_load_time': 0.015, 'total_load_time': 3.0,
                'text_miss_count': {i: np.random.randint(1, 5) for i in range(1, 101)},
                'text_hit_count': {i: np.random.randint(0, 3) for i in range(1, 51)},
                'access_log': [{'text_num': i % 100 + 1, 'was_hit': i % 4 == 0, 
                              'load_time': 0.01} for i in range(200)]
            },
            {
                'user_id': 1, 'pattern': 'poisson', 'algorithm': 'FIFOCache',
                'hits': 38, 'misses': 162, 'hit_rate': 19.0, 'miss_rate': 81.0,
                'avg_load_time': 0.016, 'total_load_time': 3.2,
                'text_miss_count': {i: np.random.randint(1, 6) for i in range(1, 101)},
                'text_hit_count': {i: np.random.randint(0, 2) for i in range(1, 51)},
                'access_log': [{'text_num': i % 100 + 1, 'was_hit': i % 5 == 0,
                              'load_time': 0.01} for i in range(200)]
            },
            {
                'user_id': 1, 'pattern': 'weighted', 'algorithm': 'FIFOCache',
                'hits': 52, 'misses': 148, 'hit_rate': 26.0, 'miss_rate': 74.0,
                'avg_load_time': 0.014, 'total_load_time': 2.8,
                'text_miss_count': {i: np.random.randint(2, 8) if 30 <= i <= 40 
                                   else np.random.randint(0, 3) for i in range(1, 101)},
                'text_hit_count': {i: np.random.randint(1, 4) for i in range(30, 41)},
                'access_log': [{'text_num': 35 if i % 2 == 0 else i % 100 + 1,
                              'was_hit': i % 4 == 0, 'load_time': 0.01} 
                              for i in range(200)]
            }
        ],
        'LRUCache': [
            {
                'user_id': 1, 'pattern': 'random', 'algorithm': 'LRUCache',
                'hits': 58, 'misses': 142, 'hit_rate': 29.0, 'miss_rate': 71.0,
                'avg_load_time': 0.013, 'total_load_time': 2.6,
                'text_miss_count': {i: np.random.randint(1, 4) for i in range(1, 101)},
                'text_hit_count': {i: np.random.randint(0, 4) for i in range(1, 51)},
                'access_log': [{'text_num': i % 100 + 1, 'was_hit': i % 3 == 0,
                              'load_time': 0.01} for i in range(200)]
            },
            {
                'user_id': 1, 'pattern': 'poisson', 'algorithm': 'LRUCache',
                'hits': 64, 'misses': 136, 'hit_rate': 32.0, 'miss_rate': 68.0,
                'avg_load_time': 0.012, 'total_load_time': 2.4,
                'text_miss_count': {i: np.random.randint(1, 5) for i in range(1, 101)},
                'text_hit_count': {i: np.random.randint(0, 3) for i in range(1, 51)},
                'access_log': [{'text_num': i % 100 + 1, 'was_hit': i % 3 == 0,
                              'load_time': 0.01} for i in range(200)]
            },
            {
                'user_id': 1, 'pattern': 'weighted', 'algorithm': 'LRUCache',
                'hits': 78, 'misses': 122, 'hit_rate': 39.0, 'miss_rate': 61.0,
                'avg_load_time': 0.011, 'total_load_time': 2.2,
                'text_miss_count': {i: np.random.randint(1, 6) if 30 <= i <= 40
                                   else np.random.randint(0, 2) for i in range(1, 101)},
                'text_hit_count': {i: np.random.randint(2, 6) for i in range(30, 41)},
                'access_log': [{'text_num': 35 if i % 2 == 0 else i % 100 + 1,
                              'was_hit': i % 3 == 0, 'load_time': 0.01}
                              for i in range(200)]
            }
        ]
    }
    
    generator = ReportGenerator(output_dir="docs_test")
    generator.generate_full_report(mock_results)
    
    print("\nTeste concluído! ✅")
    print("Verifique os gráficos gerados em docs_test/")