import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# --- CONFIGURACIÓN DE PÁGINA Y ESTILOS (CSS INYECTADO) ---
st.set_page_config(layout="wide", page_title="Reporte de Optimización de Activos", page_icon="📈")

# Inyección de CSS según el Prompt Maestro (Tipografía Serif, Cajas Académicas)
st.markdown("""
<style>
    /* Tipografía General - Forzando Serif elegante */
    body, .stMarkdown, .stText, h1, h2, h3, p {
        font-family: 'Georgia', 'Garamond', serif !important;
        color: #1a1a1a;
    }
    
    /* Cajas de Observación (Discusión de Resultados) */
    .observation-box {
        background-color: #ffffff;
        border-left: 4px solid #4a4a4a;
        padding: 15px;
        margin-top: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        font-style: italic;
        font-size: 16px;
    }

    /* Cajas Prescriptivas (Estrategia) */
    .prescription-box {
        background-color: #f4fcf4;
        border-left: 4px solid #2e7d32;
        padding: 15px;
        margin-top: 15px;
        font-size: 16px;
    }

    /* Títulos */
    h1 { color: #000000; border-bottom: 2px solid #d3d3d3; padding-bottom: 10px; }
    h2 { color: #333333; margin-top: 30px; }
    
    /* Matriz Lógica */
    .logic-matrix {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-family: 'Georgia', serif;
    }
    .logic-matrix th {
        background-color: #f0f0f0;
        border: 1px solid #ddd;
        padding: 10px;
        text-align: left;
    }
    .logic-matrix td {
        border: 1px solid #ddd;
        padding: 10px;
        vertical-align: top;
    }
</style>
""", unsafe_allow_html=True)

# --- IMPORTACIÓN DE LÓGICA PROPIA ---
sys.path.append(os.path.abspath('src')) # Asegura que encuentre tus módulos
try:
    from src.data_loader import get_financial_metrics
    from src.optimizer import optimize_portfolio
except ImportError:
    st.error("Error crítico: No se encuentran los módulos 'src'. Ejecuta este script desde la raíz del proyecto.")
    st.stop()

# --- I. PLANTEAMIENTO DEL PROBLEMA ---
st.title("Optimización de Portafolios: Enfoque de Varianza Mínima")
st.markdown("""
<div class="report-text">
Este reporte técnico aborda el problema de la asignación eficiente de capital bajo incertidumbre. 
El objetivo es determinar la combinación convexa de activos que minimice la volatilidad esperada 
sujeto a una restricción de retorno objetivo, siguiendo los postulados de la Teoría Moderna de Portafolios (Markowitz, 1952).
</div>
""", unsafe_allow_html=True)

# --- II. METODOLOGÍA ---
# Carga de datos (Simulada o Real)
@st.cache_data
def load_data():
    try:
        # Intentamos cargar los datos procesados en la fase anterior
        df = pd.read_csv("data/returns.csv", index_col=0, parse_dates=True)
        return df
    except:
        st.error("No se encontró 'data/returns.csv'. Por favor ejecuta 'data_loader.py' primero.")
        return None

returns_df = load_data()

if returns_df is not None:
    mu, sigma = get_financial_metrics(returns_df)
    
    with st.expander("Ver Detalles Metodológicos (Diseño Experimental)", expanded=False):
        st.markdown(f"""
        * **Universo de Activos:** {list(returns_df.columns)}
        * **Muestra:** {len(returns_df)} observaciones diarias.
        * **Estimadores:** Retornos esperados (Media aritmética anualizada) y Matriz de Covarianza (Shrinkage empírico).
        * **Algoritmo:** Programación Cuadrática Secuencial (SLSQP).
        """)

    # --- III. ANÁLISIS EMPÍRICO (DESCRIPTIVO/DIAGNÓSTICO) ---
    st.header("III. Análisis Empírico de Activos")
    
    tab1, tab2 = st.tabs(["Matriz de Correlación", "Perfil de Riesgo-Retorno"])
    
    with tab1:
        # Heatmap con Plotly (Minimalista)
        corr_matrix = returns_df.corr()
        fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto")
        fig_corr.update_layout(template="plotly_white", title_text="Interdependencia de Activos (Correlación de Pearson)")
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.markdown("""
        <div class="observation-box">
        <b>Discusión:</b> Se observa una correlación negativa o baja entre la Renta Variable (SPY) y los Bonos del Tesoro (TLT), 
        lo cual valida teóricamente el beneficio de la diversificación. Los activos de refugio (GLD) muestran independencia 
        relativa respecto al ciclo económico tradicional.
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        # Scatter simple Riesgo vs Retorno de activos individuales
        risk_v_return = pd.DataFrame({'Retorno': mu, 'Riesgo': np.sqrt(np.diag(sigma))})
        fig_scatter = px.scatter(risk_v_return, x='Riesgo', y='Retorno', text=risk_v_return.index, size_max=60)
        fig_scatter.update_traces(textposition='top center', marker=dict(size=15, color='#4a4a4a'))
        fig_scatter.update_layout(template="plotly_white", xaxis_title="Volatilidad Anualizada", yaxis_title="Retorno Esperado")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- IV. ANALÍTICA PRESCRIPTIVA (ESTRATEGIA) ---
    st.header("IV. Estrategia de Asignación Óptima")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Parámetros de Decisión")
        target_return = st.slider("Objetivo de Retorno Anual", min_value=0.0, max_value=float(mu.max()), value=0.08, step=0.005, format="%.2f")
        
        # Ejecutar Optimización en tiempo real
        result = optimize_portfolio(mu, sigma, target_return)
        
        if result['success']:
            st.success("✅ Convergencia Exitosa")
            st.metric("Riesgo Mínimo (Volatilidad)", f"{result['risk']:.2%}")
        else:
            st.error("❌ Solución Infactible")

    with col2:
        if result['success']:
            # Gráfico de Torta Minimalista
            weights = pd.Series(result['weights'], index=mu.index)
            weights = weights[weights > 0.001] # Filtrar residuos
            
            fig_pie = go.Figure(data=[go.Pie(labels=weights.index, values=weights.values, hole=.4, 
                                             marker=dict(colors=px.colors.qualitative.Pastel))])
            fig_pie.update_layout(template="plotly_white", title_text=f"Asignación de Capital (Target: {target_return:.1%})")
            st.plotly_chart(fig_pie, use_container_width=True)

    # MATRIZ LÓGICA (Requisito del Prompt)
    if result['success']:
        top_asset = weights.idxmax()
        top_weight = weights.max()
        
        st.markdown(f"""
        <table class="logic-matrix">
          <tr>
            <th>Nivel de Análisis</th>
            <th>Hallazgo Técnico</th>
          </tr>
          <tr>
            <td><b>Descriptivo</b><br><i>(¿Qué sucede?)</i></td>
            <td>Para alcanzar un retorno del {target_return:.1%}, el modelo sugiere una concentración del {top_weight:.1%} en {top_asset}.</td>
          </tr>
          <tr>
            <td><b>Diagnóstico</b><br><i>(¿Por qué?)</i></td>
            <td>La optimización convexa penaliza la alta covarianza. {top_asset} ofrece la mejor eficiencia marginal de riesgo en este nivel de retorno objetivo.</td>
          </tr>
          <tr>
            <td><b>Prescriptivo</b><br><i>(Acción)</i></td>
            <td>Reestructurar el portafolio actual comprando {top_asset} y reduciendo exposición en activos con beta alto si el objetivo es preservación de capital.</td>
          </tr>
        </table>
        
        <div class="prescription-box">
        <b>📋 Recomendación Estratégica:</b><br>
        Se recomienda ejecutar las órdenes de compra/venta según los pesos calculados. 
        Mantener monitoreo mensual de la matriz de covarianza para rebalanceo dinámico.
        </div>
        """, unsafe_allow_html=True)

# --- V. CONCLUSIONES ---
st.markdown("---")
st.markdown("""
<div class="report-text" style="font-size: 14px; color: #666;">
<b>Nota Final:</b> Este dashboard ha sido generado automáticamente utilizando un motor de cálculo en Python. 
Los resultados constituyen una aproximación teórica y no representan una asesoría financiera vinculante.
</div>
""", unsafe_allow_html=True)
