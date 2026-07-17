import pandas as pd

class AnalisadorConcorrencia:
    def __init__(self, caminho_csv: str):
        self.df = pd.read_csv(caminho_csv)
        self._limpar_dados()

    def _limpar_dados(self):
        # Garante que os tipos de dados estão corretos
        self.df['Preco'] = pd.to_numeric(self.df['Preco'])
        self.df['Promocao'] = self.df['Promocao'].astype(str).str.strip().str.lower()

    def obter_metricas_mercado(self) -> dict:
        """Calcula as métricas básicas do mercado concorrente."""
        preco_medio = self.df['Preco'].mean()
        
        idx_menor = self.df['Preco'].idxmin()
        idx_maior = self.df['Preco'].idxmax()
        
        empresa_menor = self.df.loc[idx_menor, 'Empresa']
        menor_preco = self.df.loc[idx_menor, 'Preco']
        
        empresa_maior = self.df.loc[idx_maior, 'Empresa']
        maior_preco = self.df.loc[idx_maior, 'Preco']
        
        # Conta quantas empresas estão em promoção (aceita 'sim' ou 's')
        empresas_em_promocao = self.df[self.df['Promocao'].isin(['sim', 's'])].shape[0]
        
        return {
            "preco_medio": preco_medio,
            "empresa_menor": empresa_menor,
            "menor_preco": menor_preco,
            "empresa_maior": empresa_maior,
            "maior_preco": maior_preco,
            "empresas_em_promocao": empresas_em_promocao
        }

    def gerar_insights(self, preco_meu_produto: float) -> list:
        """Aplica as regras de negócio baseadas no preço do meu produto."""
        metricas = self.obter_metricas_mercado()
        insights = []
        
        preco_medio = metricas["preco_medio"]
        menor_preco = metricas["menor_preco"]
        total_concorrentes = self.df.shape[0]
        promocoes = metricas["empresas_em_promocao"]

        # Regra 1: Preço acima da média
        if preco_meu_produto > preco_medio:
            percentual_acima = ((preco_meu_produto - preco_medio) / preco_medio) * 100
            insights.append(f"Seu produto está {percentual_acima:.1f}% acima do preço médio do mercado.")

        # Regra 2: Tendência promocional (> 50% dos concorrentes)
        if total_concorrentes > 0 and (promocoes / total_concorrentes) > 0.5:
            insights.append("Existe uma tendência promocional no mercado.")

        # Regra 3: Meu produto possui o menor preço
        if preco_meu_produto <= menor_preco:
            insights.append("Sua empresa possui um posicionamento competitivo.")

        # Regra 4: Diferença para o menor preço superior a 20%
        if preco_meu_produto > menor_preco:
            diferenca_percentual = ((preco_meu_produto - menor_preco) / menor_preco) * 100
            if diferenca_percentual > 20:
                insights.append("Existe risco de perda de competitividade (seu preço está mais de 20% acima do menor concorrente).")

        # Insight padrão caso nenhuma regra crítica seja ativada
        if not insights:
            insights.append("Seu preço está estável em relação aos parâmetros críticos do mercado.")

        return insights
