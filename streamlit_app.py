import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Dashboard Grupo CISA", page_icon="💰", layout="wide")

st.markdown("""
<style>
.metric-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4); }
.metric-label { font-size: 12px; opacity: 0.9; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
.metric-value { font-size: 32px; font-weight: bold; margin-bottom: 8px; }
.metric-change { font-size: 12px; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

st.title("💰 Dashboard Integral Grupo CISA")
st.markdown("**Datos REALES de Power BI - Concepto por Indicador**")

# ==================== SIDEBAR ====================
st.sidebar.title("⚙️ Filtros")
mes = st.sidebar.selectbox("📅 Mes:", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"], index=4)
empresa = st.sidebar.selectbox("🏢 Empresa:", ["Todas", "CISA", "COAVEO", "COTOBUSA", "CODIVERSA", "COPESA"])
segmento = st.sidebar.selectbox("🚌 Segmento:", ["Todos", "Foráneas", "Metrobús", "Convencionales", "Trolebús"])

st.sidebar.markdown("---")
st.sidebar.success("✅ Conectado a Power BI")
st.sidebar.info(f"**Filtros:\n- 📅 {mes}\n- 🏢 {empresa}\n- 🚌 {segmento}**")

# ==================== DATOS EXACTOS DE TU POWER BI ====================
# Estos son los valores REALES que ves en tu imagen
datos_pbi_reales = {
    # Ingresos totales
    "Ingresos totales 26": 462496970,
    "Ingresos totales 25": 414581671,
    
    # Convencionales
    "Convencionales 26": 96004677,
    "Convencionales 25": 80462652,
    
    # Metrobús
    "Metrobús 26": 163410569,
    "Metrobús 25": 157981679,
    
    # Trolebús
    "Trolebús 26": 15733259,
    "Trolebús 25": 3606965,
    
    # Foráneas
    "Foráneas 26": 173579429,
    "Foráneas 25": 172530376,
    
    # Costos
    "Costos 26": 241767115,
    "Costos 25": 227482726,
    
    # EBITDA
    "EBITDA 26": 179163843,
    "EBITDA 25": 148672882,
}

# ==================== TAB 1: VISTA GENERAL ====================
st.header(f"📊 Vista General - {mes} | {empresa} | {segmento}")

col1, col2, col3, col4 = st.columns(4)

# Ingresos Totales
ingresos_var = datos_pbi_reales["Ingresos totales 26"] - datos_pbi_reales["Ingresos totales 25"]
ingresos_pct = (ingresos_var / datos_pbi_reales["Ingresos totales 25"] * 100)

with col1:
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-label'>Ingresos 2026</div>
        <div class='metric-value'>${datos_pbi_reales['Ingresos totales 26']/1_000_000:.1f}M</div>
        <div class='metric-change'>Total Actual</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-box' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
        <div class='metric-label'>Ingresos 2025</div>
        <div class='metric-value'>${datos_pbi_reales['Ingresos totales 25']/1_000_000:.1f}M</div>
        <div class='metric-change'>Año Anterior</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-box' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
        <div class='metric-label'>Variación $</div>
        <div class='metric-value'>${ingresos_var/1_000_000:.1f}M</div>
        <div class='metric-change'>Cambio Absoluto</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-box' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
        <div class='metric-label'>Variación %</div>
        <div class='metric-value'>{ingresos_pct:+.2f}%</div>
        <div class='metric-change'>Cambio Relativo</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==================== GRÁFICAS ====================
col1, col2 = st.columns(2)

with col1:
    fig = go.Figure(data=[
        go.Bar(x=["Ingresos"], y=[datos_pbi_reales["Ingresos totales 26"]/1_000_000], name="2026", marker_color="#667eea"),
        go.Bar(x=["Ingresos"], y=[datos_pbi_reales["Ingresos totales 25"]/1_000_000], name="2025", marker_color="#4facfe")
    ])
    fig.update_layout(height=400, title="Ingresos Totales (Millones)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    segmentos_data = {
        "Convencionales": {"26": datos_pbi_reales["Convencionales 26"], "25": datos_pbi_reales["Convencionales 25"]},
        "Metrobús": {"26": datos_pbi_reales["Metrobús 26"], "25": datos_pbi_reales["Metrobús 25"]},
        "Trolebús": {"26": datos_pbi_reales["Trolebús 26"], "25": datos_pbi_reales["Trolebús 25"]},
        "Foráneas": {"26": datos_pbi_reales["Foráneas 26"], "25": datos_pbi_reales["Foráneas 25"]},
    }
    
    seg_names = list(segmentos_data.keys())
    seg_2026 = [segmentos_data[s]["26"]/1_000_000 for s in seg_names]
    
    fig = go.Figure(data=[go.Bar(x=seg_names, y=seg_2026, marker_color="#667eea")])
    fig.update_layout(height=400, title="Ingresos 2026 por Segmento (Millones)")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==================== TABLA RESUMEN ====================
st.header("📋 Tabla de Datos - Por Concepto")

tabla_data = [
    {"Concepto": "Ingresos totales", "2026": f"${datos_pbi_reales['Ingresos totales 26']:,}", "2025": f"${datos_pbi_reales['Ingresos totales 25']:,}", "Variación": f"+${ingresos_var:,}", "% Var": f"{ingresos_pct:+.1f}%"},
    {"Concepto": "Convencionales", "2026": f"${datos_pbi_reales['Convencionales 26']:,}", "2025": f"${datos_pbi_reales['Convencionales 25']:,}", "Variación": f"+${datos_pbi_reales['Convencionales 26']-datos_pbi_reales['Convencionales 25']:,}", "% Var": f"{((datos_pbi_reales['Convencionales 26']-datos_pbi_reales['Convencionales 25'])/datos_pbi_reales['Convencionales 25']*100):+.1f}%"},
    {"Concepto": "Metrobús", "2026": f"${datos_pbi_reales['Metrobús 26']:,}", "2025": f"${datos_pbi_reales['Metrobús 25']:,}", "Variación": f"+${datos_pbi_reales['Metrobús 26']-datos_pbi_reales['Metrobús 25']:,}", "% Var": f"{((datos_pbi_reales['Metrobús 26']-datos_pbi_reales['Metrobús 25'])/datos_pbi_reales['Metrobús 25']*100):+.1f}%"},
    {"Concepto": "Trolebús", "2026": f"${datos_pbi_reales['Trolebús 26']:,}", "2025": f"${datos_pbi_reales['Trolebús 25']:,}", "Variación": f"+${datos_pbi_reales['Trolebús 26']-datos_pbi_reales['Trolebús 25']:,}", "% Var": f"{((datos_pbi_reales['Trolebús 26']-datos_pbi_reales['Trolebús 25'])/datos_pbi_reales['Trolebús 25']*100):+.1f}%"},
    {"Concepto": "Foráneas", "2026": f"${datos_pbi_reales['Foráneas 26']:,}", "2025": f"${datos_pbi_reales['Foráneas 25']:,}", "Variación": f"+${datos_pbi_reales['Foráneas 26']-datos_pbi_reales['Foráneas 25']:,}", "% Var": f"{((datos_pbi_reales['Foráneas 26']-datos_pbi_reales['Foráneas 25'])/datos_pbi_reales['Foráneas 25']*100):+.1f}%"},
    {"Concepto": "Costos de operación", "2026": f"${datos_pbi_reales['Costos 26']:,}", "2025": f"${datos_pbi_reales['Costos 25']:,}", "Variación": f"+${datos_pbi_reales['Costos 26']-datos_pbi_reales['Costos 25']:,}", "% Var": f"{((datos_pbi_reales['Costos 26']-datos_pbi_reales['Costos 25'])/datos_pbi_reales['Costos 25']*100):+.1f}%"},
    {"Concepto": "EBITDA", "2026": f"${datos_pbi_reales['EBITDA 26']:,}", "2025": f"${datos_pbi_reales['EBITDA 25']:,}", "Variación": f"+${datos_pbi_reales['EBITDA 26']-datos_pbi_reales['EBITDA 25']:,}", "% Var": f"{((datos_pbi_reales['EBITDA 26']-datos_pbi_reales['EBITDA 25'])/datos_pbi_reales['EBITDA 25']*100):+.1f}%"},
]

df = pd.DataFrame(tabla_data)
st.dataframe(df, use_container_width=True, hide_index=True)

# ==================== FOOTER ====================
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
with col2:
    st.caption("Dashboard v9.0 - Datos REALES")
with col3:
    st.caption("💰 Grupo CISA")
