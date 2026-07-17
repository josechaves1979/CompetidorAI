import streamlit as strl
import pandas as pd
from analise_concorrencia import AnalisadorConcorrencia

# Configuração da página do Streamlit
strl.set_page_config(page_title="CompetitorAI - MVP", layout="centered")

strl.title("📊 CompetitorAI")
strl.subheader("Inteligência de Mercado Aplicada")
strl.markdown("---")

# Seção de Entrada de Dados
strl.sidebar.header("Parâmetros de Entrada")

# Upload do arquivo CSV
arquivo_upload = strl.sidebar.file_uploader("Suba a base de dados dos concorrentes (.CSV)", type=["csv"])

# Entrada do preço do meu produto
preco_meu_produto = strl.sidebar.number_input(
    "Digite o preço do seu produto (R$):", 
    min_value=0.0, 
    value=990.0, 
    step=10.0
)

if arquivo_upload is not None:
    try:
        # Inicializa o analisador com o arquivo enviado
        analisador = AnalisadorConcorrencia(arquivo_upload)
        metricas = analisador.obter_metricas_mercado()
        
        # Exibição da base de dados carregada
        strl.markdown("### 📋 Dados dos Concorrentes Carregados")
        strl.dataframe(analisador.df)
        
        strl.markdown("---")
        strl.markdown("### 🏛️ Análise da Concorrência")
        
        # Exibição de métricas em formato de cards visuais
        col1, col2 = strl.columns(2)
        with col1:
            strl.metric(label="Preço Médio do Mercado", value=f"R$ {metricas['preco_medio']:.2f}")
            strl.metric(label="Menor Preço Encontrado", value=f"R$ {metricas['menor_preco']:.2f}", delta=f"Empresa: {metricas['empresa_menor']}")
        with col2:
            strl.metric(label="Empresas em Promoção", value=f"{metricas['empresas_em_promocao']}")
            strl.metric(label="Maior Preço Encontrado", value=f"R$ {metricas['maior_preco']:.2f}", delta=f"Empresa: {metricas['empresa_maior']}", delta_color="inverse")

        # --- LOGO ABAIXO DOS CARDS DE MÉTRICAS NO SEU APP.PY ---

strl.markdown("---")
strl.markdown("### 📈 Análise Visual de Posicionamento")

# Inicializa o construtor de dashboards
from dashboard import DashboardConcorrencia
dash = DashboardConcorrencia(analisador.df)

# Renderiza o gráfico de comparação de preços
grafico_precos = dash.gerar_grafico_precos(preco_meu_produto)
strl.plotly_chart(grafico_precos, use_container_width=True)

# Renderiza o gráfico de rosca para promoções
grafico_promocao = dash.gerar_grafico_proporcao_promocao()
strl.plotly_chart(grafico_promocao, use_container_width=True)

strl.markdown("---")
# (Daqui para baixo continua o bloco existente dos Insights da IA...)
