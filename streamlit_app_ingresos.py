import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Ingresos - Grupo CISA",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .metric-label {
        font-size: 12px;
        opacity: 0.9;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .metric-change {
        font-size: 12px;
        opacity: 0.8;
    }
    .segment-card {
        background: #f9fafb;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 10px;
    }
    .segment-name {
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
        font-size: 14px;
    }
    .segment-value {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .segment-pct {
        color: #667eea;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("💰 Dashboard de Ingresos Operacionales")
st.markdown("**Grupo CISA - Análisis de Drivers de Ingresos 2026 vs 2025**")

# Sidebar
st.sidebar.header("⚙️ Filtros")
mes_seleccionado = st.sidebar.selectbox(
    "Mes:",
    ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"],
    index=4
)

empresa_seleccionada = st.sidebar.selectbox(
    "Empresa:",
    ["Todas", "CISA", "COAVEO", "COTOBUSA", "CODIVERSA"]
)

st.sidebar.markdown("---")

# Datos de ingresos y drivers
ingresos_data = {
    "2026": 456.465,
    "2025": 423.277,
    "variacion": 33.188,
    "variacion_pct": 7.84
}

drivers_ingresos = {
    "Km recorrido": {"valor": 9.876, "pct": 2.97},
    "Pago x KM": {"valor": 3.764, "pct": 1.13},
    "Otros": {"valor": 19.548, "pct": 5.87},
}

segmentos_data = {
    "Convencionales": {"monto_26": 98.805, "monto_25": 91.478, "variacion": 7.327, "pct_ingreso": 21.6},
    "Metrobús": {"monto_26": 163.343, "monto_25": 156.027, "variacion": 7.316, "pct_ingreso": 35.8},
    "Trolebús": {"monto_26": 16.140, "monto_25": 3.755, "variacion": 12.385, "pct_ingreso": 3.5},
    "Foráneas": {"monto_26": 178.177, "monto_25": 172.016, "variacion": 6.161, "pct_ingreso": 39.0},
}

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["📊 Métricas Principales", "🎯 Drivers de Ingresos", "📈 Análisis por Segmento", "📉 Waterfall Ingresos"])

# TAB 1: MÉTRICAS PRINCIPALES
with tab1:
    st.subheader("Resumen Ejecutivo - Ingresos 2026 vs 2025")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Ingresos 2026</div>
            <div class="metric-value">$456.5M</div>
            <div class="metric-change">Actual</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-label">Ingresos 2025</div>
            <div class="metric-value">$423.3M</div>
            <div class="metric-change">Año Anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #10b981 0%, #34d399 100%);">
            <div class="metric-label">Variación Absoluta</div>
            <div class="metric-value">+$33.2M</div>
            <div class="metric-change">Crecimiento</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);">
            <div class="metric-label">Variación %</div>
            <div class="metric-value">+7.84%</div>
            <div class="metric-change">Crecimiento YoY</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabla comparativa
    st.subheader("Ingresos Detallados por Concepto")
    
    conceptos_data = {
        "Concepto": [
            "Ingresos Totales",
            "├─ Convencionales",
            "├─ Metrobús",
            "├─ Trolebús",
            "└─ Foráneas",
            "",
            "Drivers Operacionales",
            "├─ KM Conciliado",
            "├─ KM Recorrido",
            "├─ Cumplimiento",
            "├─ Pago x KM",
            "└─ Pago por Pasajero"
        ],
        "2026": [
            "456.465", "98.805", "163.343", "16.140", "178.177",
            "",
            "",
            "6,668.5", "6,715.9", "95.88%", "64.61", "17.49"
        ],
        "2025": [
            "423.277", "91.478", "156.027", "3.755", "172.016",
            "",
            "",
            "6,455.8", "6,555.8", "94.37%", "61.70", "14.03"
        ],
        "Variación": [
            "+33.188", "+7.327", "+7.316", "+12.385", "+6.161",
            "",
            "",
            "+212.7", "+160.1", "+1.51pp", "+2.91", "+3.45"
        ],
        "% Cambio": [
            "+7.84%", "+8.0%", "+4.7%", "+329.9%", "+3.6%",
            "",
            "",
            "+3.3%", "+2.4%", "+1.6%", "+4.72%", "+24.62%"
        ]
    }
    
    df_conceptos = pd.DataFrame(conceptos_data)
    st.dataframe(df_conceptos, use_container_width=True, hide_index=True)

# TAB 2: DRIVERS DE INGRESOS
with tab2:
    st.subheader("🎯 ¿Qué impulsa el crecimiento de ingresos?")
    
    # Waterfall de drivers (Waterfall Visual como en Power BI)
    fig_waterfall = go.Figure(go.Waterfall(
        name="WF Valor Ingresos",
        orientation="v",
        x=["Ingresos 2025", "Km recorrido", "Pago x KM", "Otros", "Ingresos 2026"],
        textposition="outside",
        y=[423.277, 9.876, 3.764, 19.548, 0],
        base=0,
        connector={"line": {"color": "rgba(63, 63, 63, 0.35)"}},
        increasing={"marker": {"color": "#10b981"}},
        decreasing={"marker": {"color": "#ef4444"}},
        totals={"marker": {"color": "#667eea"}},
        measures=["relative", "relative", "relative", "relative", "total"],
        text=[
            "423.277 mil",
            "9.876 mil",
            "3.764 mil",
            "19.548 mil",
            "456.465 mil"
        ]
    ))
    
    fig_waterfall.update_layout(
        height=500,
        title="WF Valor Ingresos por Driver (2025 → 2026)",
        yaxis_title="Ingresos (Millones)",
        showlegend=True
    )
    
    st.plotly_chart(fig_waterfall, use_container_width=True)
    
    st.markdown("---")
    
    # Desglose de drivers
    st.subheader("Contribución Detallada de Drivers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="segment-card">
            <div class="segment-name">📍 KM Recorrido</div>
            <div class="segment-value">
                <span>Aumento:</span>
                <span class="segment-pct">+9.876M</span>
            </div>
            <div class="segment-value">
                <span>% del Total:</span>
                <span class="segment-pct">2.97%</span>
            </div>
            <div style="font-size: 11px; color: #666; margin-top: 8px;">
                Aumento de KM recorridos contribuye al crecimiento de ingresos
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="segment-card">
            <div class="segment-name">📍 Pago x KM</div>
            <div class="segment-value">
                <span>Aumento:</span>
                <span class="segment-pct">+3.764M</span>
            </div>
            <div class="segment-value">
                <span>% del Total:</span>
                <span class="segment-pct">1.13%</span>
            </div>
            <div style="font-size: 11px; color: #666; margin-top: 8px;">
                Incremento en tarifa por KM afecta ingresos
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="segment-card">
            <div class="segment-name">📍 Otros Drivers</div>
            <div class="segment-value">
                <span>Aumento:</span>
                <span class="segment-pct">+19.548M</span>
            </div>
            <div class="segment-value">
                <span>% del Total:</span>
                <span class="segment-pct">5.87%</span>
            </div>
            <div style="font-size: 11px; color: #666; margin-top: 8px;">
                Otros factores (demanda, cumplimiento, etc)
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: ANÁLISIS POR SEGMENTO
with tab3:
    st.subheader("Ingresos por Segmento de Empresa")
    
    # Gráfico de barras
    segmentos = list(segmentos_data.keys())
    montos_26 = [segmentos_data[s]["monto_26"] for s in segmentos]
    montos_25 = [segmentos_data[s]["monto_25"] for s in segmentos]
    
    fig_segments = go.Figure(data=[
        go.Bar(x=segmentos, y=montos_26, name="2026", marker_color="#667eea"),
        go.Bar(x=segmentos, y=montos_25, name="2025", marker_color="#4facfe")
    ])
    
    fig_segments.update_layout(
        barmode="group",
        height=400,
        hovermode="x unified",
        title="Comparativa de Ingresos por Segmento",
        xaxis_title="Segmento",
        yaxis_title="Ingresos (Millones)"
    )
    
    st.plotly_chart(fig_segments, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Desglose por Segmento y Aportación al Total")
    
    for segmento, data in segmentos_data.items():
        st.markdown(f"""
        <div class="segment-card">
            <div class="segment-name">🎯 {segmento}</div>
            <div class="segment-value">
                <span>Ingresos 2026:</span>
                <span class="segment-pct">${data['monto_26']:.1f}M</span>
            </div>
            <div class="segment-value">
                <span>Ingresos 2025:</span>
                <span>${data['monto_25']:.1f}M</span>
            </div>
            <div class="segment-value">
                <span>Variación:</span>
                <span class="segment-pct">+${data['variacion']:.2f}M ({((data['variacion']/data['monto_25'])*100):.1f}%)</span>
            </div>
            <div class="segment-value">
                <span>% del Total:</span>
                <span class="segment-pct">{data['pct_ingreso']:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# TAB 4: WATERFALL EVOLUCIÓN
with tab4:
    st.subheader("Evolución de Ingresos: Del 2025 al 2026")
    
    # Waterfall por segmento
    fig_wf_segmentos = go.Figure(go.Waterfall(
        name="Variación por Segmento",
        orientation="v",
        x=[
            "Ingresos 2025",
            "Convencionales +8.0%",
            "Metrobús +4.7%",
            "Trolebús +329.9%",
            "Foráneas +3.6%",
            "Ingresos 2026"
        ],
        textposition="outside",
        y=[
            423.277,
            7.327,
            7.316,
            12.385,
            6.161,
            0
        ],
        base=0,
        connector={"line": {"color": "rgba(63, 63, 63, 0.35)"}},
        increasing={"marker": {"color": "#10b981"}},
        decreasing={"marker": {"color": "#ef4444"}},
        totals={"marker": {"color": "#667eea"}},
        measures=["relative", "relative", "relative", "relative", "relative", "total"],
        text=[
            "423.3M",
            "+7.3M",
            "+7.3M",
            "+12.4M",
            "+6.2M",
            "456.5M"
        ]
    ))
    
    fig_wf_segmentos.update_layout(
        height=600,
        title="Evolución de Ingresos por Segmento (2025 → 2026)",
        yaxis_title="Ingresos (Millones)",
        showlegend=True
    )
    
    st.plotly_chart(fig_wf_segmentos, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📊 Análisis de la Evolución")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🔍 Principales Impulsores:**
        - **Trolebús**: Crecimiento espectacular de +329.9% (de 3.8M a 16.1M)
        - **Convencionales**: +8.0% (7.3M adicionales)
        - **Metrobús**: +4.7% (7.3M adicionales)
        - **Foráneas**: +3.6% (6.2M adicionales)
        
        **Total**: +$33.2M (+7.84%)
        """)
    
    with col2:
        st.warning("""
        **⚠️ Observaciones:**
        - Trolebús lidera el crecimiento porcentual
        - Foráneas es el segmento más grande (39% del total)
        - Metrobús mantiene posición fuerte (35.8%)
        - Crecimiento distribuido entre todos los segmentos
        """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
with col2:
    st.caption("Dashboard v1.0 - Análisis de Ingresos")
with col3:
    st.caption("💰 Grupo CISA")
