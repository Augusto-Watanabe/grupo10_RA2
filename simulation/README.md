# Módulos de Simulação e Relatórios

Este diretório abriga toda a lógica para executar as simulações de performance dos algoritmos de cache e para gerar os relatórios visuais com os resultados.

## Conteúdo

-   **`simulation_engine.py`**: O motor da simulação. Orquestra a execução dos testes para cada algoritmo, gerenciando múltiplos usuários e padrões de acesso.

-   **`request_generator.py`**: Responsável por criar as sequências de requisições de acesso aos textos, seguindo os padrões definidos (aleatório, Poisson e ponderado).

-   **`report_generator.py`**: Gera todos os gráficos e visualizações comparativas (Hit Rate, Tempo de Carregamento, Heatmaps, etc.) a partir dos dados coletados pela simulação.

-   **`simulation_mode.py`**: Ponto de entrada que integra todos os componentes acima para executar o "modo de simulação" completo, desde a configuração até a apresentação dos resultados e recomendações.
