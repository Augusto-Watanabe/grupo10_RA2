from core.text_loader import TextLoader
from algorithms.fifo_cache import FIFOCache
from algorithms.lru_cache import LRUCache
from algorithms.lfu_cache import LFUCache

def menu():
    # Instancia o loader
    loader = TextLoader("texts")
    
    # Inicializa o cache FIFO
    FIFOcache = FIFOCache(capacity=10)
    # Inicializa o cache LRU
    LRUcache = LRUCache(capacity=10)
    # Inicializa o cache LRU
    LFUcache = LFUCache(capacity=10)
    
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
                
                # Obtém o texto através do cache FIFO
                FIFOcontent, FIFOload_time, FIFOwas_hit = FIFOcache.get(text_num, load_from_disk)

                # Obtém o texto através do cache LRU
                LRUcontent, LRUload_time, LRUwas_hit = LRUcache.get(text_num, load_from_disk)

                # Obtém o texto através do cache LFU
                LFUcontent, LFUload_time, LFUwas_hit = LFUcache.get(text_num, load_from_disk)
                
                # Exibe informações FIFO
                FIFOstatus = "CACHE HIT ✓" if FIFOwas_hit else "CACHE MISS ✗ (carregado do disco)"

                # Exibe informações LRU
                LRUstatus = "CACHE HIT ✓" if LRUwas_hit else "CACHE MISS ✗ (carregado do disco)"

                # Exibe informações LFU
                LFUstatus = "CACHE HIT ✓" if LFUwas_hit else "CACHE MISS ✗ (carregado do disco)"
                
                # Exibição
                print(f"\n{'='*60}")

                # Exibe informações FIFO
                print(f"{'='*20}FIFO{'='*20}")
                print(f"✓ Texto {text_num} carregado com sucesso - {FIFOstatus}!")
                print(f"  Tempo de carregamento: {FIFOload_time:.6f}s")
                print(f"  Tamanho: {len(FIFOcontent)} caracteres")
                print(f"  Palavras: {len(FIFOcontent.split())}")
                print(f"Itens no cache: {FIFOcache.size()}/{FIFOcache.capacity}")
                print(f"{'='*60}\n")

                # Exibe informações LRU
                print(f"{'='*20}LRU{'='*20}")
                print(f"✓ Texto {text_num} carregado com sucesso - {LRUstatus}!")
                print(f"  Tempo de carregamento: {LRUload_time:.6f}s")
                print(f"  Tamanho: {len(LRUcontent)} caracteres")
                print(f"  Palavras: {len(LRUcontent.split())}")
                print(f"Itens no cache: {LRUcache.size()}/{LRUcache.capacity}")
                print(f"{'='*60}\n")

                # Exibe informações LFU
                print(f"{'='*20}LFU{'='*20}")
                print(f"✓ Texto {text_num} carregado com sucesso - {LFUstatus}!")
                print(f"  Tempo de carregamento: {LFUload_time:.6f}s")
                print(f"  Tamanho: {len(LFUcontent)} caracteres")
                print(f"  Palavras: {len(LFUcontent.split())}")
                print(f"Itens no cache: {LFUcache.size()}/{LFUcache.capacity}")
                print(f"{'='*60}\n")

                #Imprime o conteudo, que é igual para todos os caches
                print(LFUcontent)


                # Fim da exibição
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