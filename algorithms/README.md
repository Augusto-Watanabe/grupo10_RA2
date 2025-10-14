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
    8. Texto 1: HIT ✓  | Freq: {1: 4, 2: 3, 4: 1}
    9. Texto 2: HIT ✓  | Freq: {1: 4, 2: 3, 4: 1}
    10. Texto 1: HIT ✓  | Freq: {1: 5, 2: 3, 4: 1}
    11. Texto 5: MISS ✗ | Freq: {1: 5, 2: 3, 5: 1}
    12. Texto 1: HIT ✓  | Freq: {1: 6, 2: 3, 5: 1}
    13. Texto 6: MISS ✗ | Freq: {1: 6, 2: 3, 6: 1}

    Quando LFU é superior:
    ✓ Há itens "quentes" (hot items) acessados repetidamente
    ✓ Padrão de acesso tem favoritos claros
    ✓ Ex: Textos de referência, documentos importantes

ARC (Adaptive Replacement Cache)
#Executar o código arc_cache.py retorna um teste básico da implementação do algoritmo

    Funcionamento com 4 listas:
    - T1: Itens acessados recentemente (uma vez)
    - T2: Itens acessados frequentemente (mais de uma vez)
    - B1: Fantasmas de T1 (itens removidos recentemente)
    - B2: Fantasmas de T2 (itens removidos frequentemente)

    Sequência: [1, 2, 3, 1, 1, 2, 2, 4, 5, 1, 6] com capacidade 4

    1. Texto 1: MISS ✗ | T1=[1], T2=[], B1=[], B2=[], p=0
    2. Texto 2: MISS ✗ | T1=[1,2], T2=[], B1=[], B2=[], p=0
    3. Texto 3: MISS ✗ | T1=[1,2,3], T2=[], B1=[], B2=[], p=0
    4. Texto 1: HIT ✓  | T1=[2,3], T2=[1], B1=[], B2=[], p=0
       ↑ Move de T1 para T2 (agora é frequentemente acessado)
    5. Texto 1: HIT ✓  | T1=[2,3], T2=[1], B1=[], B2=[], p=0
    6. Texto 2: HIT ✓  | T1=[3], T2=[1,2], B1=[], B2=[], p=0
    7. Texto 2: HIT ✓  | T1=[3], T2=[1,2], B1=[], B2=[], p=0
    8. Texto 4: MISS ✗ | T1=[3,4], T2=[1,2], B1=[], B2=[], p=0
    9. Texto 5: MISS ✗ | T1=[4,5], T2=[1,2], B1=[3], B2=[], p=1
       ↑ Remove 3 (LRU de T1), detecta padrão sequencial (aumenta p)
    10. Texto 1: HIT ✓ | T1=[4,5], T2=[2,1], B1=[3], B2=[], p=1
    11. Texto 6: MISS ✗ | T1=[5,6], T2=[2,1], B1=[3,4], B2=[], p=2
       ↑ Remove 4, mantém itens frequentes 1 e 2 em T2

    Comportamento Adaptativo:
    - Acesso sequencial (3,4,5,6): Aumenta p → favorece T1
    - Acesso repetitivo (1,2): Diminui p → favorece T2
    - "Aprende" com acertos fantasmas em B1 e B2

    Vantagens do ARC:
    ✓✓ Combina benefícios do LRU e LFU
    ✓✓ Adapta-se automaticamente ao padrão de acesso
    ✓✓ Usa histórico de remoções para tomar decisões inteligentes
    ✓✓ Excelente para cargas de trabalho mistas

    Quando ARC é superior:
    ✓ Padrões de acesso variáveis (sequenciais + repetitivos)
    ✓ Cargas de trabalho imprevisíveis
    ✓ Cenários onde outros algoritmos falham consistentemente

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

    ARC (Adaptive Replacement Cache):
    Adapta-se dinamicamente ao padrão de acesso
    [T1:1,2,3 T2:] → acessa 1 → [T1:2,3 T2:1] HIT
    [T1:2,3 T2:1] → acessa 1 → [T1:2,3 T2:1] HIT  
    [T1:2,3 T2:1] → acessa 4 → [T1:3,4 T2:1] ← Remove 2 (p=0, favorece T1)
    [T1:3,4 T2:1] → acessa 2 → [T1:4 T2:1,2] ← Remove 3, detecta padrão
    [T1:4 T2:1,2] → acessa 5 → [T1:4,5 T2:1,2] ← Ajusta p dinamicamente
    ✓✓✓ Mantém itens frequentes E se adapta ao padrão de acesso!

Resumo Final:
- FIFO: Simples, previsível, bom para acesso sequencial
- LRU: Bom para acesso temporal localizado, mantém itens recentes
- LFU: Excelente para itens "quentes" com acesso repetitivo
- ARC: O mais inteligente, adapta-se automaticamente, ideal para cargas mistas

Recomendações de Uso:
- Acesso sequencial: FIFO ou ARC
- Acesso repetitivo: LFU ou ARC  
- Padrões mistos/desconhecidos: ARC
- Recursos limitados: FIFO (menor overhead)
- Performance máxima: ARC (maior inteligência)