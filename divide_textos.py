# divide_textos.py
import os

def dividir_texto(arquivo_entrada, pasta_saida, palavras_por_texto=1000):
    # Cria a pasta de saída, se não existir
    os.makedirs(pasta_saida, exist_ok=True)

    # Lê todo o texto de entrada
    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        texto = f.read()

    # Divide o texto em palavras
    palavras = texto.split()

    # Cria os arquivos de saída
    for i in range (100):
        inicio = i * palavras_por_texto
        fim = inicio + palavras_por_texto
        trecho = " ".join(palavras[inicio:fim])
        
        with open(f"{pasta_saida}/texto_{i+1}.txt", "w", encoding="utf-8") as out:
            out.write(trecho)

    print(f"✅ Gerados 100 arquivos na pasta '{pasta_saida}'")


def main():
    dividir_texto("OsFilhosdoPadre.txt", "texts")

if __name__ == "__main__":
    main()