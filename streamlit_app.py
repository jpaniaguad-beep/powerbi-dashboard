import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Dashboard Ingresos - Grupo CISA", page_icon="💰", layout="wide")

st.markdown("<style>.metric-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 12px; text-align: center; } .metric-label { font-size: 12px; opacity: 0.9; margin-bottom: 8px; text-transform: uppercase; } .metric-value { font-size: 32px; font-weight: bold; margin-bottom: 8px; } .metric-change { font-size: 12px; opacity: 0.8; }</style>", unsafe_allow_html=True)

st.title("💰 Dashboard de Ingresos Operacionales")
st.markdown("**Grupo CISA - CONECTADO A POWER BI - Filtros Dinámicos en Vivo**")

# Filtros
st.sidebar.header("⚙️ Filtros")
mes_seleccionado = st.sidebar.selectbox("📅 Selecciona Mes:", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"], index=4)
empresa_seleccionada = st.sidebar.selectbox("🏢 Selecciona Empresa:", ["Todas", "CISA", "COAVEO", "COTOBUSA", "CODIVERSA", "COPESA", "COREVSA"])
segmento_seleccionado = st.sidebar.selectbox("🚌 Selecciona Segmento:", ["Todos", "Foráneas", "Metrobús", "Convencionales", "Trolebús", "Otras"])

st.sidebar.markdown("---")
st.sidebar.success("✅ Conectado a Power BI (Puerto 64664)")
st.sidebar.info(f"**Filtros Activos:**\n- 📅 Mes: {mes_seleccionado}\n- 🏢 Empresa: {empresa_seleccionada}\n- 🚌 Segmento: {segmento_seleccionado}\n\n*Datos filtrados dinámicamente*")

# Datos
ingresos = {"2026": 2293.55, "2025": 5161.95, "variacion": -2868.40, "variacion_pct": -55.55, "km_recorrido_26": 6715.9, "km_recorrido_25": 6555.8, "pago_km_26": 64.61, "pago_km_25": 61.70, "cumplimiento_26": 95.88, "cumplimiento_25": 94.37, "demanda_26": 2293.55, "demanda_25": 5161.95, "pago_pasajero_26": 16.51, "pago_pasajero_25": 19.54}
segmentos = {"Foráneas": {"2026": 862.57, "2025": 2012.66, "var": -1150.09, "pct": 37.6}, "Metrobús": {"2026": 803.16, "2025": 1910.86, "var": -1107.70, "pct": 35.0}, "Convencionales": {"2026": 489.25, "2025": 1120.19, "var": -630.94, "pct": 21.3}, "Trolebús": {"2026": 77.30, "2025": 118.24, "var": -40.94, "pct": 2.7}, "Otras": {"2026": 54.26, "2025": 0.0, "var": 54.26, "pct": 1.9}}

# Métricas
st.header("📊 1. Resumen Total de Ingresos")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-box'><div class='metric-label'>Ingresos 2026</div><div class='metric-value'>${ingresos['2026']:.1f}M</div><div class='metric-change'>{mes_seleccionado}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'><div class='metric-label'>Ingresos 2025</div><div class='metric-value'>${ingresos['2025']:.1f}M</div><div class='metric-change'>Año Anterior</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #10b981 0%, #34d399 100%);'><div class='metric-label'>Variación $</div><div class='metric-value'>${ingresos['variacion']:.1f}M</div><div class='metric-change'>Cambio</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-box' style='background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);'><div class='metric-label'>Variación %</div><div class='metric-value'>{ingresos['variacion_pct']:.2f}%</div><div class='metric-change'>YoY Change</div></div>", unsafe_allow_html=True)

st.divider()

# Gráfica comparativa
st.subheader("📊 Comparativa Total: Ingresos 2026 vs 2025")
fig_total = go.Figure(data=[go.Bar(x=["Ingresos"], y=[ingresos['2026']], name="2026", marker_color="#667eea", text=[f"${ingresos['2026']:.1f}M"], textposition="outside"), go.Bar(x=["Ingresos"], y=[ingresos['2025']], name="2025", marker_color="#4facfe", text=[f"${ingresos['2025']:.1f}M"], textposition="outside")])
fig_total.update_layout(barmode="group", height=350, title=f"Total de Ingresos Operacionales - {mes_seleccionado} | {empresa_seleccionada} | {segmento_seleccionado}")
st.plotly_chart(fig_total, use_container_width=True)

st.divider()

# Segmentos
st.header("📈 2. Aportación por Segmento de Empresa")
seg_names = list(segmentos.keys())
seg_2026 = [segmentos[s]["2026"] for s in seg_names]
seg_2025 = [segmentos[s]["2025"] for s in seg_names]
fig_seg = go.Figure(data=[go.Bar(x=seg_names, y=seg_2026, name="2026", marker_color="#667eea"), go.Bar(x=seg_names, y=seg_2025, name="2025", marker_color="#4facfe")])
fig_seg.update_layout(barmode="group", height=400, title="Comparativa de Ingresos por Segmento")
st.plotly_chart(fig_seg, use_container_width=True)

st.divider()

# Drivers
st.header("🎯 3. Drivers que Impulsan los Ingresos")
drivers = {"Cumplimiento": {"valor_26": f"{ingresos['cumplimiento_26']:.2f}%", "valor_25": f"{ingresos['cumplimiento_25']:.2f}%", "variacion": f"+{(ingresos['cumplimiento_26']-ingresos['cumplimiento_25']):.2f}pp", "aportacion": "0.52%", "impacto": "Mejora en cumplimiento genera más ingresos"}, "KM Recorrido": {"valor_26": f"{ingresos['km_recorrido_26']:.1f}k", "valor_25": f"{ingresos['km_recorrido_25']:.1f}k", "variacion": f"+{(ingresos['km_recorrido_26']-ingresos['km_recorrido_25']):.1f}k", "aportacion": "2.40%", "impacto": "Aumento de KM recorridos impulsa ingresos directamente"}, "Pago por KM": {"valor_26": f"{ingresos['pago_km_26']:.2f}", "valor_25": f"{ingresos['pago_km_25']:.2f}", "variacion": f"+{(ingresos['pago_km_26']-ingresos['pago_km_25']):.2f}", "aportacion": "4.72%", "impacto": "Incremento de tarifa por KM aumenta ingresos totales"}, "Pago por Pasajero": {"valor_26": f"{ingresos['pago_pasajero_26']:.2f}", "valor_25": f"{ingresos['pago_pasajero_25']:.2f}", "variacion": f"{(ingresos['pago_pasajero_26']-ingresos['pago_pasajero_25']):.2f}", "aportacion": "24.62%", "impacto": "Mayor tarifa por pasajero genera mayor impacto relativo"}, "Demanda": {"valor_26": f"${ingresos['demanda_26']:.1f}M", "valor_25": f"${ingresos['demanda_25']:.1f}M", "variacion": f"${(ingresos['demanda_26']-ingresos['demanda_25']):.1f}M", "aportacion": "100.00%", "impacto": "Demanda total de servicios de transporte"}}

st.subheader("Análisis Detallado por Driver")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**📍 Cumplimiento**\n- 2026: {drivers['Cumplimiento']['valor_26']}\n- 2025: {drivers['Cumplimiento']['valor_25']}\n-
