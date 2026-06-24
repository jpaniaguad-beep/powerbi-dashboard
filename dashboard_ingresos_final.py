import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Dashboard Ingresos - Grupo CISA",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
    <style>
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
    }
    .metric-label { font-size: 12px; opacity: 0.9; margin-bottom: 8px; text-transform: uppercase; }
    .metric-value { font-size: 32px; font-weight: bold; margin-bottom: 8px; }
    .metric-change { font-size: 12px; opacity: 0.8; }
    </style>
""", unsafe_allow_html=True)

st.title("💰 Dashboard de Ingresos Operacionales")
st.markdown("**Grupo CISA - Análisis Detallado 2026 vs 2025**")

# ==================== SECCIÓN 1: MÉTRICAS PRINCIPALES ====================
st.header("📊 1. Resumen Total de Ingresos")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-label">Ingresos 2026</div>
        <div class="metric-value">$456.5M</div>
        <div class="metric-change">Actual</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="metric-label">Ingresos 2025</div>
        <div class="metric-value">$423.3M</div>
        <div class="metric-change">Año Anterior</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-box" style="background: linear-gradient(135deg, #10b981 0%, #34d399 100%);">
        <div class="metric-label">Variación $</div>
        <div class="metric-value">+$33.2M</div>
        <div class="metric-change">Crecimiento</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-box" style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);">
        <div class="metric-label">Variación %</div>
        <div class="metric-value">+7.84%</div>
        <div class="metric-change">YoY Growth</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==================== SECCIÓN 2: APORTACIÓN POR SEGMENTO ====================
st.header("📈 2. Aportación por Segmento de Empresa")

segmentos = {
    "Foráneas": {"2026": 178.177, "2025": 172.016, "var": 6.161, "pct": 39.0},
    "Metrobús": {"2026": 163.343, "2025": 156.027, "var": 7.316, "pct": 35.8},
    "Convencionales": {"2026": 98.805, "2025": 91.478, "var": 7.327, "pct": 21.6},
    "Trolebús": {"2026": 16.140, "2025": 3.755, "var": 12.385, "pct": 3.5},
}

# Tabla de segmentos
tabla_segmentos = []
for seg, datos in segmentos.items():
    tabla_segmentos.append({
        "Segmento": seg,
        "2026": f"${datos['2026']:.1f}M",
        "2025": f"${datos['2025']:.1f}M",
        "Variación": f"+${datos['var']:.1f}M",
        "% Variación": f"+{((datos['var']/datos['2025'])*100):.1f}%",
        "% del Total": f"{datos['pct']:.1f}%"
    })

df_seg = pd.DataFrame(tabla_segmentos)
st.dataframe(df_seg, use_container_width=True, hide_index=True)

# Gráfico de barras por segmento
seg_names = list(segmentos.keys())
seg_2026 = [segmentos[s]["2026"] for s in seg_names]
seg_2025 = [segmentos[s]["2025"] for s in seg_names]

fig_seg = go.Figure(data=[
    go.Bar(x=seg_names, y=seg_2026, name="2026", marker_color="#667eea"),
    go.Bar(x=seg_names, y=seg_2025, name="2025", marker_color="#4facfe")
])
fig_seg.update_layout(barmode="group", height=400, title="Comparativa de Ingresos por Segmento")
st.plotly_chart(fig_seg, use_container_width=True)

st.divider()

# ==================== SECCIÓN 3: DRIVERS DE INGRESOS ====================
st.header("🎯 3. Drivers que Impulsan los Ingresos")

drivers = {
    "Cumplimiento": {
        "valor_26": "95.88%",
        "valor_25": "94.37%",
        "variacion": "+1.51pp",
        "aportacion": "0.52%",
        "impacto": "Mejora en cumplimiento genera más ingresos"
    },
    "KM Recorrido": {
        "valor_26": "6,715.9k",
        "valor_25": "6,555.8k",
        "variacion": "+160.1k",
        "aportacion": "2.40%",
        "impacto": "Aumento de KM recorridos impulsa ingresos directamente"
    },
    "Pago por KM": {
        "valor_26": "64.61",
        "valor_25": "61.70",
        "variacion": "+2.91",
        "aportacion": "4.72%",
        "impacto": "Incremento de tarifa por KM aumenta ingresos totales"
    },
    "Pago por Pasajero": {
        "valor_26": "17.49",
        "valor_25": "14.03",
        "variacion": "+3.45",
        "aportacion": "24.62%",
        "impacto": "Mayor tarifa por pasajero genera mayor impacto relativo"
    },
    "Demanda": {
        "valor_26": "456.5M",
        "valor_25": "423.3M",
        "variacion": "+33.2M",
        "aportacion": "100.00%",
        "impacto": "Demanda total de servicios de transporte"
    }
}

# Tabla de drivers
tabla_drivers = []
for driver, datos in drivers.items():
    tabla_drivers.append({
        "Driver": driver,
        "2026": datos["valor_26"],
        "2025": datos["valor_25"],
        "Variación": datos["variacion"],
        "% Aportación": datos["aportacion"]
    })

df_drivers = pd.DataFrame(tabla_drivers)
st.dataframe(df_drivers, use_container_width=True, hide_index=True)

# Cards detallados de cada driver
st.subheader("Análisis Detallado por Driver")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    **📍 Cumplimiento**
    - 2026: {drivers['Cumplimiento']['valor_26']}
    - 2025: {drivers['Cumplimiento']['valor_25']}
    - Variación: {drivers['Cumplimiento']['variacion']}
    - Aportación: {drivers['Cumplimiento']['aportacion']}
    - 💡 {drivers['Cumplimiento']['impacto']}
    """)
    
    st.markdown(f"""
    **📍 KM Recorrido**
    - 2026: {drivers['KM Recorrido']['valor_26']}
    - 2025: {drivers['KM Recorrido']['valor_25']}
    - Variación: {drivers['KM Recorrido']['variacion']}
    - Aportación: {drivers['KM Recorrido']['aportacion']}
    - 💡 {drivers['KM Recorrido']['impacto']}
    """)
    
    st.markdown(f"""
    **📍 Pago por KM**
    - 2026: {drivers['Pago por KM']['valor_26']}
    - 2025: {drivers['Pago por KM']['valor_25']}
    - Variación: {drivers['Pago por KM']['variacion']}
    - Aportación: {drivers['Pago por KM']['aportacion']}
    - 💡 {drivers['Pago por KM']['impacto']}
    """)

with col2:
    st.markdown(f"""
    **📍 Pago por Pasajero**
    - 2026: {drivers['Pago por Pasajero']['valor_26']}
    - 2025: {drivers['Pago por Pasajero']['valor_25']}
    - Variación: {drivers['Pago por Pasajero']['variacion']}
    - Aportación: {drivers['Pago por Pasajero']['aportacion']}
    - 💡 {drivers['Pago por Pasajero']['impacto']}
    """)
    
    st.markdown(f"""
    **📍 Demanda Total**
    - 2026: {drivers['Demanda']['valor_26']}
    - 2025: {drivers['Demanda']['valor_25']}
    - Variación: {drivers['Demanda']['variacion']}
    - Aportación: {drivers['Demanda']['aportacion']}
    - 💡 {drivers['Demanda']['impacto']}
    """)

st.divider()

# ==================== SECCIÓN 4: GRÁFICA WATERFALL ====================
st.header("📊 4. Evolución de Ingresos: Waterfall 2025 → 2026")

st.markdown("**¿Cómo pasamos de $423.3M a $456.5M? Aquí está el desglose:**")

# Waterfall por segmento
fig_waterfall = go.Figure(go.Waterfall(
    name="Ingresos",
    orientation="v",
    x=[
        "Ingresos 2025",
        "Convencionales (+8.0%)",
        "Metrobús (+4.7%)",
        "Trolebús (+329.9%)",
        "Foráneas (+3.6%)",
        "Ingresos 2026"
    ],
    textposition="outside",
    y=[423.277, 7.327, 7.316, 12.385, 6.161, 0],
    base=0,
    connector={"line": {"color": "rgba(63, 63, 63, 0.35)"}},
    increasing={"marker": {"color": "#10b981"}},
    decreasing={"marker": {"color": "#ef4444"}},
    totals={"marker": {"color": "#667eea"}},
    measures=["relative", "relative", "relative", "relative", "relative", "total"],
))

fig_waterfall.update_layout(
    height=500,
    title="WF Valor Ingresos - Evolución por Segmento",
    yaxis_title="Ingresos (Millones)"
)

st.plotly_chart(fig_waterfall, use_container_width=True)

# Análisis del waterfall
st.subheader("Análisis de la Evolución")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **🔍 Principales Impulsores:**
    
    1. **Trolebús**: +$12.4M (+329.9%)
       - Mayor expansión del servicio
    
    2. **Convencionales**: +$7.3M (+8.0%)
       - Crecimiento estable en base
    
    3. **Metrobús**: +$7.3M (+4.7%)
       - Mantenimiento de posición fuerte
    
    4. **Foráneas**: +$6.2M (+3.6%)
       - Segmento más grande, crece moderado
    
    **Total: +$33.2M (+7.84%)**
    """)

with col2:
    st.warning("""
    **⚡ Insights Clave:**
    
    ✅ **Crecimiento distribuido** entre todos segmentos
    
    ✅ **Trolebús lidera** en crecimiento porcentual
    
    ✅ **Foráneas permanece grande** (39% del total)
    
    ✅ **Metrobús estable** (35.8% del total)
    
    ✅ **Drivers positivos**: KM, tarifa, cumplimiento
    
    📊 **Pronóstico**: Tendencia alcista sostenible
    """)

st.divider()

# ==================== SECCIÓN 5: SUMMARY ====================
st.header("📋 Resumen Ejecutivo")

summary_data = {
    "Métrica": [
        "Total Ingresos 2026",
        "Total Ingresos 2025",
        "Crecimiento Absoluto",
        "Crecimiento Porcentual",
        "Segmento Dominante",
        "Segmento Mayor Crecimiento %",
        "Driver Principal",
        "Eficiencia Operativa"
    ],
    "Valor": [
        "$456.5M",
        "$423.3M",
        "+$33.2M",
        "+7.84%",
        "Foráneas (39.0%)",
        "Trolebús (+329.9%)",
        "Pago por Pasajero (+24.62%)",
        "95.88% Cumplimiento"
    ]
}

df_summary = pd.DataFrame(summary_data)
st.dataframe(df_summary, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
with col2:
    st.caption("Dashboard v1.0 - Ingresos Operacionales")
with col3:
    st.caption("💰 Grupo CISA")
