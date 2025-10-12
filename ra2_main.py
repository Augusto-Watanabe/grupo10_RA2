from core.text_loader import TextLoader

def menu():
    # Instancia o loader
    loader = TextLoader("texts")
    
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
                
                # Carrega o texto
                content, load_time = loader.load_text(text_num)
                
                # Exibe informações
                print(f"\n{'='*60}")
                print(f"✓ Texto {text_num} carregado com sucesso!")
                print(f"  Tempo de carregamento: {load_time:.4f}s")
                print(f"  Tamanho: {len(content)} caracteres")
                print(f"  Palavras: {len(content.split())}")
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