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

LFU
#Executar o código lfu_cache.py retorna um teste básico da implementação do algoritmo
    Sequência: [1, 2, 3, 1, 2, 1, 4, 1, 2, 1, 5, 1, 6]
    Textos 1 e 2 são muito populares (acessados repetidamente)

    1. Texto 1: MISS ✗ | Freq: {1: 1}
    2. Texto 2: MISS ✗ | Freq: {1: 1, 2: 1}
    3. Texto 3: MISS ✗ | Freq: {1: 1, 2: 1, 3: 1}
    4. Texto 1: HIT ✓  | Freq: {1: 2, 2: 1, 3: 1}
    5. Texto 2: HIT ✓  | Freq: {1: 2, 2: 2, 3: 1}
    6. Texto 1: HIT ✓  | Freq: {1: 3, 2: 2, 3: 1}
    7. Texto 4: MISS ✗ | Freq: {1: 3, 2: 2, 4: 1}
    8. Texto 1: HIT ✓  | Freq: {1: 4, 2: 2, 4: 1}
    9. Texto 2: HIT ✓  | Freq: {1: 4, 2: 3, 4: 1}
    10. Texto 1: HIT ✓  | Freq: {1: 5, 2: 3, 4: 1}
    11. Texto 5: MISS ✗ | Freq: {1: 5, 2: 3, 5: 1}
    12. Texto 1: HIT ✓  | Freq: {1: 6, 2: 3, 5: 1}
    13. Texto 6: MISS ✗ | Freq: {1: 6, 2: 3, 6: 1}

    Quando LFU é superior:
    ✓ Há itens "quentes" (hot items) acessados repetidamente
    ✓ Padrão de acesso tem favoritos claros
    ✓ Ex: Textos de referência, documentos importantes


Comparação entre algoritmos
    Sequência: [1, 2, 3, 1, 1, 4, 2, 5] com capacidade 3

    FIFO (First In, First Out):
    Remove sempre o mais ANTIGO (ordem de inserção)
    [1, 2, 3] → acessa 1 → [1, 2, 3] HIT
    [1, 2, 3] → acessa 1 → [1, 2, 3] HIT
    [1, 2, 3] → acessa 4 → [2, 3, 4] ← Remove 1 (mais antigo)
    ❌ Perdeu texto 1 que foi muito usado!    

    LRU (Least Recently Used):
    Remove o menos RECENTEMENTE usado
    [1, 2, 3] → acessa 1 → [2, 3, 1] HIT (move pro final)
    [2, 3, 1] → acessa 1 → [2, 3, 1] HIT (já está no final)
    [2, 3, 1] → acessa 4 → [3, 1, 4] ← Remove 2 (menos recente)
    ✓ Manteve texto 1, mas esquece frequência

    LFU (Least Frequently Used):
    Remove o menos FREQUENTEMENTE usado
    [1(1), 2(1), 3(1)] → acessa 1 → [1(2), 2(1), 3(1)] HIT
    [1(2), 2(1), 3(1)] → acessa 1 → [1(3), 2(1), 3(1)] HIT
    [1(3), 2(1), 3(1)] → acessa 4 → [1(3), 2(1), 4(1)] ← Remove 3
    [1(3), 2(1), 4(1)] → acessa 2 → [1(3), 2(2), 4(1)] HIT
    [1(3), 2(2), 4(1)] → acessa 5 → [1(3), 2(2), 5(1)] ← Remove 4 (menor freq)
    ✓✓ Mantém itens frequentes mesmo se não recentes!


    