Observações sobre o comportamento dos tipos de cache:



FIFO
#Executar o código fifo_cache.py retorna um teste básico da implementação do algoritmo

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

LRU
#Executar o código lru_cache.py retorna um teste básico da implementação do algoritmo

    sequência [1, 2, 3, 1, 4, 2, 5]:
    1. [1]           MISS
    2. [1, 2]        MISS
    3. [1, 2, 3]     MISS
    4. [2, 3, 1]     HIT   ← Acessa 1, move pro final (mais recente)
    5. [3, 1, 4]     MISS  ← Remove 2 (menos usado recentemente)
    6. [1, 4, 2]     MISS  ← Remove 3, mas 1 permanece!
    7. [4, 2, 5]     MISS  ← Remove 1 

    Vantagens LRU:
    ✓ Mantém itens frequentemente acessados por mais tempo
    ✓ Se adapta melhor a padrões de acesso não-sequenciais
    ✓ É geralmente superior em cenários reais