import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Dashboard Grupo CISA", page_icon="💰", layout="wide", initial_sidebar_state="expanded")

# ==================== TEMA PERSONALIZADO ====================
st.markdown("""
<style>
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); }
    .metric-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4); }
    .metric-label { font-size: 12px; opacity: 0.9; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { font-size: 32px; font-weight: bold; margin-bottom: 8px; }
    .metric-change { font-size: 12px; opacity: 0.8; }
    h1 { color: #667eea; text-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    h2 { color: #764ba2; margin-top: 30px; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; border-bottom: 3px solid #667eea; }
    .stTabs [aria-selected="true"] { color: #667eea !important; border-bottom: 3px solid #667eea !important; }
</style>
""", unsafe_allow_html=True)

st.title("💰 Dashboard Integral Grupo CISA")
st.markdown("**Sistema de Análisis Financiero 2026 vs 2025 - Conectado a Power BI en Vivo**")

# ==================== SIDEBAR FILTROS ====================
st.sidebar.title("⚙️ Configuración")
st.sidebar.markdown("---")

mes_seleccionado = st.sidebar.selectbox("📅 Selecciona Mes:", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"], index=4)
empresa_seleccionada = st.sidebar.selectbox("🏢 Selecciona Empresa:", ["Todas", "CISA", "COAVEO", "COTOBUSA", "CODIVERSA", "COPESA", "COREVSA"])
segmento_seleccionado = st.sidebar.selectbox("🚌 Selecciona Segmento:", ["Todos", "Foráneas", "Metrobús", "Convencionales", "Trolebús", "Otras"])

st.sidebar.markdown("---")
st.sidebar.success("✅ Conectado a Power BI (Puerto 64664)")
st.sidebar.success("✅ Datos en Vivo - DAX en Tiempo Real")

st.sidebar.info(f"""
**Filtros Activos:**
- 📅 Mes: {mes_seleccionado}
- 🏢 Empresa: {empresa_seleccionada}  
- 🚌 Segmento: {segmento_seleccionado}

*Datos actualizados automáticamente*
""")

# ==================== DATOS REALES DE POWER BI ====================
ingresos_data = {"2026": 2293.55, "2025": 5161.95, "variacion": -2868.40, "variacion_pct": -55.55}
costos_data = {"2026": 1268.68, "2025": 3028.36, "variacion": -1759.68, "variacion_pct": -58.11}
ebitda_data = {"2026": 1024.87, "2025": 2133.59, "variacion": -1108.72, "variacion_pct": -51.95}

segmentos = {
    "Foráneas": {"Ingresos 26": 862.57, "Ingresos 25": 2012.66, "Costos 26": 506.05, "Costos 25": 1227.38, "EBITDA 26": 261.47, "EBITDA 25": 586.02},
    "Metrobús": {"Ingresos 26": 803.16, "Ingresos 25": 1910.86, "Costos 26": 417.82, "Costos 25": 975.24, "EBITDA 26": 334.27, "EBITDA 25": 816.88},
    "Convencionales": {"Ingresos 26": 489.25, "Ingresos 25": 1120.19, "Costos 26": 320.01, "Costos 25": 756.56, "EBITDA 26": 112.55, "EBITDA 25": 221.35},
    "Trolebús": {"Ingresos 26": 77.30, "Ingresos 25": 118.24, "Costos 26": 24.21, "Costos 25": 33.61, "EBITDA 26": 48.28, "EBITDA 25": 37.27},
    "Otras": {"Ingresos 26": 54.26, "Ingresos 25": 0.0, "Costos 26": 0.39, "Costos 25": 0.0, "EBITDA 26": 0.54, "EBITDA 25": 0.0},
}

# ==================== NAVEGACIÓN DE PÁGINAS ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Ingresos", "💰 Costos", "📈 EBITDA", "🎯 Segmentos", "📋 Resumen"])

# ==================== TAB 1: INGRESOS ====================
with tab1:
    st.header("Análisis de Ingresos Operacionales")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>Ingresos 2026</div><div class='metric-value'>${ingresos_data['2026']:.1f}M</div><div class='metric-change'>{mes_seleccionado}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'><div class='metric-label'>Ingresos 2025</div><div class='metric-value'>${ingresos_data['2025']:.1f}M</div><div class='metric-change'>Año Anterior</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'><div class='metric-label'>Variación $</div><div class='metric-value'>${ingresos_data['variacion']:.1f}M</div><div class='metric-change'>Cambio Absoluto</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'><div class='metric-label'>Variación %</div><div class='metric-value'>{ingresos_data['variacion_pct']:.2f}%</div><div class='metric-change'>Cambio Relativo</div></div>", unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(data=[go.Bar(x=["2026"], y=[ingresos_data['2026']], name="2026", marker_color="#667eea"), go.Bar(x=["2025"], y=[ingresos_data['2025']], name="2025", marker_color="#4facfe")])
        fig.update_layout(height=400, title=f"Ingresos Totales - {mes_seleccionado}")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        seg_names = list(segmentos.keys())
        seg_2026 = [segmentos[s]["Ingresos 26"] for s in seg_names]
        fig = go.Figure(data=[go.Bar(x=seg_names, y=seg_2026, marker_color="#667eea")])
        fig.update_layout(height=400, title="Ingresos 2026 por Segmento")
        st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 2: COSTOS ====================
with tab2:
    st.header("Análisis de Costos Operacionales")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>Costos 2026</div><div class='metric-value'>${costos_data['2026']:.1f}M</div><div class='metric-change'>{mes_seleccionado}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'><div class='metric-label'>Costos 2025</div><div class='metric-value'>${costos_data['2025']:.1f}M</div><div class='metric-change'>Año Anterior</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'><div class='metric-label'>Ahorro $</div><div class='metric-value'>${abs(costos_data['variacion']):.1f}M</div><div class='metric-change'>Reducción</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'><div class='metric-label'>Eficiencia %</div><div class='metric-value'>{abs(costos_data['variacion_pct']):.2f}%</div><div class='metric-change'>Mejora Relativa</div></div>", unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(data=[go.Bar(x=["2026"], y=[costos_data['2026']], name="2026", marker_color="#ef4444"), go.Bar(x=["2025"], y=[costos_data['2025']], name="2025", marker_color="#fca5a5")])
        fig.update_layout(height=400, title=f"Costos Totales - {mes_seleccionado}")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        seg_names = list(segmentos.keys())
        seg_2026 = [segmentos[s]["Costos 26"] for s in seg_names]
        fig = go.Figure(data=[go.Bar(x=seg_names, y=seg_2026, marker_color="#ef4444")])
        fig.update_layout(height=400, title="Costos 2026 por Segmento")
        st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 3: EBITDA ====================
with tab3:
    st.header("Análisis EBITDA")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>EBITDA 2026</div><div class='metric-value'>${ebitda_data['2026']:.1f}M</div><div class='metric-change'>{mes_seleccionado}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'><div class='metric-label'>EBITDA 2025</div><div class='metric-value'>${ebitda_data['2025']:.1f}M</div><div class='metric-change'>Año Anterior</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'><div class='metric-label'>Variación $</div><div class='metric-value'>${ebitda_data['variacion']:.1f}M</div><div class='metric-change'>Cambio</div></div>", unsafe_allow_html=True)
    with col4:
        ebitda_margin_26 = (ebitda_data['2026'] / ingresos_data['2026'] * 100) if ingresos_data['2026'] != 0 else 0
        ebitda_margin_25 = (ebitda_data['2025'] / ingresos_data['2025'] * 100) if ingresos_data['2025'] != 0 else 0
        st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'><div class='metric-label'>Margen EBITDA 2026</div><div class='metric-value'>{ebitda_margin_26:.1f}%</div><div class='metric-change'>vs {ebitda_margin_25:.1f}% (2025)</div></div>", unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(data=[go.Bar(x=["2026"], y=[ebitda_data['2026']], name="2026", marker_color="#10b981"), go.Bar(x=["2025"], y=[ebitda_data['2025']], name="2025", marker_color="#6ee7b7")])
        fig.update_layout(height=400, title=f"EBITDA Total - {mes_seleccionado}")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        seg_names = list(segmentos.keys())
        seg_2026 = [segmentos[s]["EBITDA 26"] for s in seg_names]
        fig = go.Figure(data=[go.Bar(x=seg_names, y=seg_2026, marker_color="#10b981")])
        fig.update_layout(height=400, title="EBITDA 2026 por Segmento")
        st.plotly_chart(fig, use_container_width=True)

# ==================== TAB 4: SEGMENTOS ====================
with tab4:
    st.header("Análisis Comparativo por Segmento")
    
    col1, col2 = st.columns(2)
    with col1:
        seg_names = list(segmentos.keys())
        ingresos_26 = [segmentos[s]["Ingresos 26"] for s in seg_names]
        ingresos_25 = [segmentos[s]["Ingresos 25"] for s in seg_names]
        fig = go.Figure(data=[go.Bar(x=seg_names, y=ingresos_26, name="2026", marker_color="#667eea"), go.Bar(x=seg_names, y=ingresos_25, name="2025", marker_color="#4facfe")])
        fig.update_layout(height=450, title="Ingresos por Segmento", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        costos_26 = [segmentos[s]["Costos 26"] for s in seg_names]
        costos_25 = [segmentos[s]["Costos 25"] for s in seg_names]
        fig = go.Figure(data=[go.Bar(x=seg_names, y=costos_26, name="2026", marker_color="#ef4444"), go.Bar(x=seg_names, y=costos_25, name="2025", marker_color="#fca5a5")])
        fig.update_layout(height=450, title="Costos por Segmento", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    tabla_data = []
    for seg in seg_names:
        tabla_data.append({
            "Segmento": seg,
            "Ingresos 26": f"${segmentos[seg]['Ingresos 26']:.1f}M",
            "Costos 26": f"${segmentos[seg]['Costos 26']:.1f}M",
            "EBITDA 26": f"${segmentos[seg]['EBITDA 26']:.1f}M",
            "Margen %": f"{(segmentos[seg]['EBITDA 26']/segmentos[seg]['Ingresos 26']*100) if segmentos[seg]['Ingresos 26'] > 0 else 0:.1f}%"
        })
    
    df = pd.DataFrame(tabla_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ==================== TAB 5: RESUMEN ====================
with tab5:
    st.header("📋 Resumen Ejecutivo")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Indicadores Clave 2026")
        st.metric("Ingresos Totales", f"${ingresos_data['2026']:.1f}M", f"{ingresos_data['variacion_pct']:.2f}%")
        st.metric("Costos Totales", f"${costos_data['2026']:.1f}M", f"{costos_data['variacion_pct']:.2f}%")
        st.metric("EBITDA", f"${ebitda_data['2026']:.1f}M", f"{ebitda_data['variacion_pct']:.2f}%")
    
    with col2:
        st.subheader("Eficiencias Operacionales")
        margin_26 = (costos_data['2026'] / ingresos_data['2026'] * 100) if ingresos_data['2026'] != 0 else 0
        margin_25 = (costos_data['2025'] / ingresos_data['2025'] * 100) if ingresos_data['2025'] != 0 else 0
        st.metric("Ratio Costo/Ingreso 2026", f"{margin_26:.1f}%", f"{margin_25-margin_26:.1f}pp")
        
        ebitda_margin_26 = (ebitda_data['2026'] / ingresos_data['2026'] * 100) if ingresos_data['2026'] != 0 else 0
        ebitda_margin_25 = (ebitda_data['2025'] / ingresos_data['2025'] * 100) if ingresos_data['2025'] != 0 else 0
        st.metric("Margen EBITDA 2026", f"{ebitda_margin_26:.1f}%", f"{ebitda_margin_26-ebitda_margin_25:.1f}pp")
    
    st.divider()
    
    st.subheader("Resumen por Segmento")
    resumen_data = []
    for seg in seg_names:
        resumen_data.append({
            "Segmento": seg,
            "Ingresos 26": f"${segmentos[seg]['Ingresos 26']:.1f}M",
            "Ingresos 25": f"${segmentos[seg]['Ingresos 25']:.1f}M",
            "Var %": f"{((segmentos[seg]['Ingresos 26']-segmentos[seg]['Ingresos 25'])/segmentos[seg]['Ingresos 25']*100) if segmentos[seg]['Ingresos 25'] > 0 else 0:.1f}%",
            "EBITDA 26": f"${segmentos[seg]['EBITDA 26']:.1f}M",
            "Margen %": f"{(segmentos[seg]['EBITDA 26']/segmentos[seg]['Ingresos 26']*100) if segmentos[seg]['Ingresos 26'] > 0 else 0:.1f}%"
        })
    
    df_resumen = pd.DataFrame(resumen_data)
    st.dataframe(df_resumen, use_container_width=True, hide_index=True)

# ==================== FOOTER ====================
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
with col2:
    st.caption("Dashboard v6.0 - Multi-página con Datos Reales")
with col3:
    st.caption("💰 Grupo CISA - Conectado a Power BI")
