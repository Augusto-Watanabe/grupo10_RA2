# Simulador de Algoritmos de Cache para Leitura de Textos

Este projeto é um aplicativo de terminal desenvolvido para simular e analisar a performance de diferentes algoritmos de cache (FIFO, LRU, LFU) em um cenário de leitura de textos a partir de um disco lento.

A simulação modela o acesso concorrente de múltiplos "usuários" a um conjunto de 100 arquivos de texto, utilizando diferentes padrões de acesso (aleatório, Poisson e ponderado). Ao final, o sistema gera um relatório visual completo com gráficos comparativos, permitindo uma análise detalhada da eficiência de cada algoritmo em termos de taxa de acertos (hit rate) e tempo de resposta.

## ✨ Funcionalidades

- **Simulação de Disco Lento**: O carregamento de arquivos do disco simula a latência de um sistema de armazenamento lento.
- **Algoritmos de Cache**: Implementação e comparação dos algoritmos **FIFO** (First-In, First-Out), **LRU** (Least Recently Used) e **LFU** (Least Frequently Used).
- **Múltiplos Usuários e Padrões de Acesso**: Simula o acesso concorrente de vários usuários com três padrões distintos:
  - **Aleatório**: Acessos uniformemente distribuídos entre todos os textos.
  - **Poisson**: Acessos concentrados em uma região específica de textos, simulando "localidade de referência".
  - **Ponderado**: Acessos com maior probabilidade em uma "região quente" de textos pré-definida.
- **Geração de Relatórios**: Criação automática de gráficos e visualizações para análise de performance, incluindo:
  - Comparação de Taxa de Acertos (Hit Rate).
  - Comparação de Tempo Médio de Carregamento.
  - Distribuição de Cache Misses por texto.
  - Heatmap de Performance (Algoritmo vs. Padrão de Acesso).
  - Análise de textos mais acessados.

## 📂 Estrutura do Projeto

```
grupo10_RA2/
├── core/                # Módulos centrais (cache, text_loader, etc.)
├── docs/                # Diretório para os relatórios e gráficos gerados
├── simulation/          # Módulos de simulação e geração de relatórios
├── texts/               # Arquivos de texto utilizados na simulação
├── OsFilhosdoPadre.txt  # Texto original para ser processado
├── divide_textos.py     # Script para preparar os arquivos de texto
├── main.py              # Ponto de entrada principal da simulação (não fornecido no contexto)
└── README.md            # Este arquivo
```

## 🚀 Instalação e Uso

### 1. Pré-requisitos

- Python 3.8 ou superior

### 2. Instalação

Clone o repositório e instale as dependências:

```bash
# Clone este repositório
git clone <url-do-seu-repositorio>
cd grupo10_RA2

# Crie e ative um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Preparação dos Textos

O projeto utiliza um conjunto de 100 arquivos de texto. Para gerá-los a partir do arquivo `OsFilhosdoPadre.txt`, execute:

```bash
python divide_textos.py
```

Isso criará o diretório `texts/` com 100 arquivos numerados, cada um contendo aproximadamente 1000 palavras.

### 4. Executando a Simulação

Para iniciar a simulação e gerar os relatórios, execute o script principal do projeto:

```bash
python main.py
```

Ao final da execução, os gráficos comparativos serão salvos no diretório `docs/`.

## 📦 Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt` e podem ser instaladas com `pip`.

- `numpy>=1.21.0`
- `matplotlib>=3.4.0`
- `seaborn>=0.11.0`
- `requests>=2.26.0`
- `pandas>=1.3.0`

Para gerar o arquivo `requirements.txt` a partir da lista acima, você pode usar:

```bash
pip freeze > requirements.txt
```