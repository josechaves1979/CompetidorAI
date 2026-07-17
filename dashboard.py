import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class DashboardConcorrencia:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def gerar_grafico_precos(self, preco_meu_produto: float) -> go.Figure:
        """
        Gera um gráfico de barras comparando os preços dos concorrentes
        e adiciona uma linha de referência com o preço do meu produto.
        """
        # Ordena os preços para facilitar a leitura visual
        df_ordenado = self.df.sort_values(by="Preco", ascending=True)
        
        # Cria o gráfico de barras
        fig = px.bar(
            df_ordenado,
            x="Empresa",
            y="Preco",
            text="Preco",
            title="Comparativo de Preços no Mercado (R$)",
            labels={"Preco": "Preço (R$)", "Empresa": "Concorrente"},
            color="Promocao",
            color_discrete_map={"Sim": "#2ecc71", "Não": "#3498db"}
        )
        
        # Ajusta a exibição do texto em cima das barras
        fig.update_traces(texttemplate='R$ %{text:.2f}', textposition='outside')
        
        # Adiciona a linha horizontal com o preço do meu produto
        fig.add_hline(
            y=preco_meu_produto,
            line_dash="dash",
            line_color="#e74c3c",
            line_width=2,
            annotation_text=f"Meu Produto: R$ {preco_meu_produto:.2f}",
            annotation_position="top right"
        )
        
        # Melhora o layout estético
        fig.update_layout(
            yaxis=dict(range=[0, df_ordenado["Preco"].max() * 1.2]),
            template="plotly_white",
            legend_title_text="Em Promoção?"
        )
        
        return fig

    def gerar_grafico_proporcao_promocao(self) -> go.Figure:
        """
        Gera um gráfico de pizza para mostrar a proporção de concorrentes
        que estão ou não realizando promoções.
        """
        contagem_promocao = self.df["Promocao"].value_counts().reset_index()
        contagem_promocao.columns = ["Status", "Quantidade"]
        
        fig = px.pie(
            contagem_promocao,
            values="Quantidade",
            names="Status",
            title="Proporção de Concorrentes em Promoção",
            color="Status",
            color_discrete_map={"Sim": "#2ecc71", "Não": "#3498db"},
            hole=0.4 # Transforma em um gráfico de rosca (mais moderno)
        )
        
        fig.update_traces(textinfo='percent+value')
        fig.update_layout(template="plotly_white")
        
        return fig
