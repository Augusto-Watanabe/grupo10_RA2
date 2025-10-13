from core.text_loader import TextLoader
from algorithms.fifo_cache import FIFOCache

def menu():
    # Instancia o loader
    loader = TextLoader("texts")
    
    # Inicializa o cache (por enquanto usa BaseCache, depois será substituído)
    FIFOcache = FIFOCache(capacity=10)
    
    while True:
        entrada = input("\nDigite o número do texto desejado (1-100), 0 para sair, ou -1 para simulação: ")
        
        # Sair
        if entrada == "0":
            print("Encerrando programa...")
            break
        
        # Modo simulação
        elif entrada == "-1":
            print("Iniciando modo simulação...")
            # TODO: adicionar função do modo simulação
            # simulation_mode()
        
        # Carregar texto
        else:
            try:
                # Converte para inteiro
                text_num = int(entrada)

                # Função wrapper para o loader
                def load_from_disk(num):
                    return loader.load_text(num)
                
                # Obtém o texto através do cache
                content, load_time, was_hit = FIFOcache.get(text_num, load_from_disk)
                
                # Exibe informações
                status = "CACHE HIT ✓" if was_hit else "CACHE MISS ✗ (carregado do disco)"
                
                # Exibe informações
                print(f"\n{'='*60}")
                print(f"✓ Texto {text_num} carregado com sucesso - {status}!")
                print(f"  Tempo de carregamento: {load_time:.6f}s")
                print(f"  Tamanho: {len(content)} caracteres")
                print(f"  Palavras: {len(content.split())}")
                print(f"Itens no cache: {FIFOcache.size()}/{FIFOcache.capacity}")
                print(f"{'='*60}\n")
                print(content)
                print(f"\n{'='*60}")
                
            except ValueError as e:
                if "invalid literal" in str(e):
                    print("❌ Erro: Digite apenas números!")
                else:
                    print(f"❌ Erro: {e}")
            
            except FileNotFoundError as e:
                print(f"❌ Arquivo não encontrado: {e}")
            
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    menu()  