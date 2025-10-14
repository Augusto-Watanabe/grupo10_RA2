# Relatórios e Gráficos da Simulação

Este diretório armazena todos os relatórios visuais e gráficos gerados pelo `report_generator.py` ao final da execução do modo de simulação.

Os arquivos aqui presentes são o resultado da análise comparativa de performance entre os diferentes algoritmos de cache (FIFO, LRU, LFU, ARC) sob vários padrões de acesso.

## Arquivos Gerados

-   `hit_rate_comparison.png`: Comparativo da Taxa de Acertos (Hit Rate).
-   `load_time_comparison.png`: Comparativo do Tempo Médio de Carregamento.
-   `miss_distribution.png`: Distribuição de Cache Misses por texto.
-   `pattern_comparison.png`: Performance de Hit/Miss Rate por padrão de acesso.
-   `performance_heatmap.png`: Heatmap de performance (Algoritmo vs. Padrão).
-   `top_texts_analysis.png`: Análise dos textos mais acessados.