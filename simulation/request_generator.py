"""
Gerador de requisições para simulação de usuários
Implementa três padrões de acesso: aleatório, Poisson e ponderado

Aluno D - Módulo de Simulação
"""

import random
import numpy as np


class RequestGenerator:
    """
    Classe para gerar requisições de textos seguindo diferentes padrões
    """
    
    def __init__(self, total_texts: int = 100, seed: int = None):
        """
        Inicializa o gerador de requisições
        
        Args:
            total_texts: número total de textos disponíveis (1-100)
            seed: semente para reprodutibilidade (opcional)
        """
        self.total_texts = total_texts
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
    
    def generate_random(self, num_requests: int) -> list:
        """
        Gera requisições completamente aleatórias (distribuição uniforme)
        
        Args:
            num_requests: número de requisições a gerar
            
        Returns:
            list: lista de números de textos (1 a total_texts)
        """
        return [random.randint(1, self.total_texts) for _ in range(num_requests)]
    
    def generate_poisson(self, num_requests: int, lambda_param: float = 30.0) -> list:
        """
        Gera requisições com distribuição de Poisson
        
        A distribuição de Poisson modela eventos que ocorrem em intervalos,
        gerando um padrão mais realista onde alguns valores são mais comuns.
        
        Args:
            num_requests: número de requisições a gerar
            lambda_param: parâmetro lambda (média) da distribuição
            
        Returns:
            list: lista de números de textos
        """
        requests = []
        for _ in range(num_requests):
            # Gera número usando Poisson e garante que está no range válido
            value = np.random.poisson(lambda_param)
            # Mantém no intervalo [1, total_texts]
            value = max(1, min(value, self.total_texts))
            requests.append(value)
        return requests
    
    def generate_weighted(self, num_requests: int, 
                         hot_range: tuple = (30, 40), 
                         hot_probability: float = 0.43) -> list:
        """
        Gera requisições com ponderação (alguns textos são mais prováveis)
        
        Simula um cenário onde textos específicos são mais acessados
        (textos "quentes" ou hot items), como documentos de referência.
        
        Args:
            num_requests: número de requisições a gerar
            hot_range: tupla (início, fim) do intervalo de textos quentes
            hot_probability: probabilidade de acessar textos quentes (0-1)
            
        Returns:
            list: lista de números de textos
        """
        requests = []
        hot_start, hot_end = hot_range
        hot_texts = list(range(hot_start, hot_end + 1))
        cold_texts = [i for i in range(1, self.total_texts + 1) 
                     if i not in hot_texts]
        
        for _ in range(num_requests):
            if random.random() < hot_probability:
                # Acessa um texto "quente" (no intervalo especificado)
                requests.append(random.choice(hot_texts))
            else:
                # Acessa um texto "frio" (fora do intervalo)
                requests.append(random.choice(cold_texts))
        
        return requests
    
    def generate_user_requests(self, num_requests: int = 200, 
                              pattern: str = 'random') -> list:
        """
        Gera requisições para um único usuário seguindo um padrão específico
        
        Args:
            num_requests: número de requisições (padrão: 200)
            pattern: tipo de padrão ('random', 'poisson', 'weighted')
            
        Returns:
            list: lista de números de textos
            
        Raises:
            ValueError: se o padrão for inválido
        """
        if pattern == 'random':
            return self.generate_random(num_requests)
        elif pattern == 'poisson':
            return self.generate_poisson(num_requests)
        elif pattern == 'weighted':
            return self.generate_weighted(num_requests)
        else:
            raise ValueError(f"Padrão inválido: {pattern}. "
                           f"Use 'random', 'poisson' ou 'weighted'")
    
    def analyze_distribution(self, requests: list) -> dict:
        """
        Analisa a distribuição de uma lista de requisições
        
        Args:
            requests: lista de números de textos
            
        Returns:
            dict: estatísticas da distribuição
        """
        from collections import Counter
        
        counter = Counter(requests)
        
        return {
            'total_requests': len(requests),
            'unique_texts': len(counter),
            'most_common': counter.most_common(10),
            'min_accesses': min(counter.values()) if counter else 0,
            'max_accesses': max(counter.values()) if counter else 0,
            'avg_accesses': sum(counter.values()) / len(counter) if counter else 0
        }


# Teste e demonstração
if __name__ == "__main__":
    print("="*70)
    print("TESTE DO GERADOR DE REQUISIÇÕES")
    print("="*70)
    
    generator = RequestGenerator(total_texts=100, seed=42)
    
    patterns = ['random', 'poisson', 'weighted']
    num_requests = 200
    
    for pattern in patterns:
        print(f"\n{'='*70}")
        print(f"Padrão: {pattern.upper()}")
        print(f"{'='*70}")
        
        requests = generator.generate_user_requests(num_requests, pattern)
        analysis = generator.analyze_distribution(requests)
        
        print(f"Total de requisições: {analysis['total_requests']}")
        print(f"Textos únicos acessados: {analysis['unique_texts']}")
        print(f"Média de acessos por texto: {analysis['avg_accesses']:.2f}")
        print(f"Máximo de acessos: {analysis['max_accesses']}")
        print(f"Mínimo de acessos: {analysis['min_accesses']}")
        
        print(f"\n10 textos mais acessados:")
        for text_num, count in analysis['most_common']:
            print(f"  Texto {text_num:3d}: {count:3d} acessos "
                  f"({'*' * (count // 2)})")
        
        if pattern == 'weighted':
            # Verifica se a ponderação funcionou (textos 30-40 devem ter ~43%)
            hot_range = range(30, 41)
            hot_accesses = sum(1 for r in requests if r in hot_range)
            hot_percentage = (hot_accesses / len(requests)) * 100
            print(f"\n📊 Verificação da ponderação:")
            print(f"  Textos 30-40: {hot_accesses} acessos ({hot_percentage:.1f}%)")
            print(f"  Esperado: ~43%")
            print(f"  Status: {'✓ OK' if 40 <= hot_percentage <= 46 else '✗ Fora do esperado'}")
    
    print("\n" + "="*70)
    print("Teste concluído! ✅")
    print("="*70)