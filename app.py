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

        strl.markdown("---")
        
        # Seção de Insights da IA (Regras de Negócio)
        strl.markdown("### 💡 Insights Gerados pela IA")
        insights = analisador.gerar_insights(preco_meu_produto)
        
        for insight in insights:
            if "risco" in insight.lower() or "acima" in insight.lower():
                strl.warning(insight)
            elif "competitivo" in insight.lower():
                strl.success(insight)
            else:
                strl.info(insight)
                
    except Exception as e:
        strl.error(f"Erro ao processar o arquivo CSV. Verifique o formato. Detalhes: {e}")
else:
    strl.info("💡 Por favor, faça o upload do arquivo `.csv` na barra lateral para iniciar a análise.")
    
    # Exemplo de formato esperado para ajudar o usuário do portfólio
    strl.markdown("#### Formato esperado do arquivo CSV:")
    df_exemplo = pd.DataFrame({
        "Empresa": ["Gran Cursos", "Estratégia", "Direção Concursos", "AlfaCon"],
        "Produto": ["Assinatura Premium", "Assinatura Premium", "Assinatura Premium", "Assinatura Premium"],
        "Preco": [997, 797, 897, 847],
        "Promocao": ["Não", "Sim", "Sim", "Não"]
    })
    strl.dataframe(df_exemplo)
