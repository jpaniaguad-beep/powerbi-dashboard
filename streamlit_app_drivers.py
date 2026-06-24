import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Drivers Costos - Grupo CISA",
    page_icon="📊",
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
    .driver-card {
        background: #f9fafb;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 10px;
    }
    .driver-name {
        font-weight: 600;
        color: #333;
        margin-bottom: 5px;
    }
    .driver-value {
        font-size: 18px;
        color: #667eea;
        font-weight: bold;
    }
    .driver-impact {
        font-size: 12px;
        color: #666;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Dashboard de Drivers de Costos Operacionales")
st.markdown("**Grupo CISA - Análisis de Componentes que Afectan Cada Rubro**")

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

# Datos de drivers por rubro (basados en tu modelo)
drivers_data = {
    "Combustible": {
        "monto_26": 104.6,
        "monto_25": 100.8,
        "drivers": [
            {"nombre": "Litros Consumidos", "valor_26": "3.3M", "valor_25": "3.6M", "variacion": "-312k (-8.6%)"},
            {"nombre": "Precio Promedio", "valor_26": "27.11", "valor_25": "24.66", "variacion": "+2.45 (+9.9%)"},
        ],
        "impacto": "El aumento de 9.9% en el precio compensa la reducción de 8.6% en litros"
    },
    "Mantenimiento": {
        "monto_26": 48.7,
        "monto_25": 57.7,
        "drivers": [
            {"nombre": "Factor Promedio Mtto", "valor_26": "7.26", "valor_25": "8.80", "variacion": "-0.31 (-3.38%)"},
            {"nombre": "KM Recorrido", "valor_26": "6.7M", "valor_25": "6.6M", "variacion": "+53.9k (+1%)"},
            {"nombre": "Costo por Unidad", "valor_26": "14.8k", "valor_25": "17.5k", "variacion": "-2.7k (-15.4%)"},
        ],
        "impacto": "Reducción de 15.5% en costos por mejora en factor de mantenimiento"
    },
    "Nómina Operadores": {
        "monto_26": 81.5,
        "monto_25": 76.9,
        "drivers": [
            {"nombre": "Número de Operadores", "valor_26": "3,366", "valor_25": "3,419", "variacion": "-53 (-1.6%)"},
            {"nombre": "Costo Promedio", "valor_26": "24.2k", "valor_25": "22.5k", "variacion": "+1.7k (+7.6%)"},
            {"nombre": "Total Horas", "valor_26": "8.2M", "valor_25": "7.8M", "variacion": "+400k (+5.1%)"},
        ],
        "impacto": "Aumento por mayor costo promedio y horas trabajadas (+6.1%)"
    },
    "Nómina Mecánicos": {
        "monto_26": 23.8,
        "monto_25": 19.2,
        "drivers": [
            {"nombre": "Número de Mecánicos", "valor_26": "1,018", "valor_25": "952", "variacion": "+66 (+6.9%)"},
            {"nombre": "Costo Promedio", "valor_26": "23.4k", "valor_25": "20.2k", "variacion": "+3.2k (+15.8%)"},
        ],
        "impacto": "Aumento por más mecánicos y mayor costo por persona (+23.9%)"
    },
    "Limpieza": {
        "monto_26": 6.4,
        "monto_25": 5.7,
        "drivers": [
            {"nombre": "Servicios por Unidad", "valor_26": "12.4", "valor_25": "11.2", "variacion": "+1.2 (+10.7%)"},
            {"nombre": "Costo por Servicio", "valor_26": "520", "valor_25": "508", "variacion": "+12 (+2.4%)"},
            {"nombre": "Unidades Base", "valor_26": "1,991", "valor_25": "1,991", "variacion": "0 (0%)"},
        ],
        "impacto": "Aumento por más servicios y mayor costo unitario (+12.3%)"
    },
    "Seguro": {
        "monto_26": 9.1,
        "monto_25": 9.1,
        "drivers": [
            {"nombre": "Prima Promedio", "valor_26": "4,574", "valor_25": "4,561", "variacion": "+13 (+0.3%)"},
            {"nombre": "Unidades Aseguradas", "valor_26": "1,991", "valor_25": "1,991", "variacion": "0 (0%)"},
        ],
        "impacto": "Sin variación significativa (prima estable año a año)"
    },
    "Otros Costos": {
        "monto_26": 2.8,
        "monto_25": 1.9,
        "drivers": [
            {"nombre": "Repuestos Varios", "valor_26": "0.8M", "valor_25": "0.5M", "variacion": "+0.3M (+60%)"},
            {"nombre": "Servicios Externos", "valor_26": "1.2M", "valor_25": "0.9M", "variacion": "+0.3M (+33%)"},
            {"nombre": "Gastos Diversos", "valor_26": "0.8M", "valor_25": "0.5M", "variacion": "+0.3M (+60%)"},
        ],
        "impacto": "Aumento significativo en todos los componentes (+40.5%)"
    }
}

# TAB 1: ANÁLISIS POR RUBRO
tab1, tab2, tab3 = st.tabs(["📈 Drivers por Rubro", "📊 Comparativa 2026 vs 2025", "🔍 Impacto Total"])

with tab1:
    st.subheader("Análisis Detallado de Drivers - ¿Qué impulsa cada costo?")
    
    # Selector de rubro
    selected_rubro = st.selectbox(
        "Selecciona un rubro para ver sus drivers:",
        list(drivers_data.keys())
    )
    
    rubro = drivers_data[selected_rubro]
    
    # Métricas principales del rubro
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">{selected_rubro}</div>
            <div class="metric-value">{rubro['monto_26']}M</div>
            <div class="metric-change">2026</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-label">2025</div>
            <div class="metric-value">{rubro['monto_25']}M</div>
            <div class="metric-change">Año Anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        variacion = rubro['monto_26'] - rubro['monto_25']
        pct = (variacion / rubro['monto_25']) * 100
        color = "#10b981" if pct > 0 else "#ef4444"
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, {color} 0%, {color}aa 100%);">
            <div class="metric-label">Variación</div>
            <div class="metric-value">{variacion:+.1f}M</div>
            <div class="metric-change">{pct:+.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Drivers detallados
    st.subheader(f"🎯 Componentes que Afectan a {selected_rubro}")
    
    for driver in rubro['drivers']:
        st.markdown(f"""
        <div class="driver-card">
            <div class="driver-name">📍 {driver['nombre']}</div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: #667eea; font-weight: bold;">2026: </span>{driver['valor_26']}
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    <span style="color: #4facfe; font-weight: bold;">2025: </span>{driver['valor_25']}
                </div>
            </div>
            <div class="driver-impact">📊 Variación: {driver['variacion']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Impacto explicativo
    st.info(f"**💡 Análisis:** {rubro['impacto']}")

with tab2:
    st.subheader("Comparativa de Montos por Rubro")
    
    # Preparar datos para gráfico
    rubros = list(drivers_data.keys())
    montos_26 = [drivers_data[r]["monto_26"] for r in rubros]
    montos_25 = [drivers_data[r]["monto_25"] for r in rubros]
    
    # Gráfico de barras
    fig = go.Figure(data=[
        go.Bar(x=rubros, y=montos_26, name="2026", marker_color="#667eea"),
        go.Bar(x=rubros, y=montos_25, name="2025", marker_color="#4facfe")
    ])
    fig.update_layout(
        barmode="group",
        height=400,
        hovermode="x unified",
        xaxis_title="Rubro de Costo",
        yaxis_title="Monto (Millones)",
        title="Comparativa de Costos 2026 vs 2025"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla comparativa
    st.markdown("---")
    st.subheader("Tabla Detallada")
    
    df_comparativa = pd.DataFrame({
        "Rubro": rubros,
        "Monto 2026 (M)": montos_26,
        "Monto 2025 (M)": montos_25,
        "Variación (M)": [montos_26[i] - montos_25[i] for i in range(len(rubros))],
        "% Variación": [((montos_26[i] - montos_25[i]) / montos_25[i]) * 100 for i in range(len(rubros))]
    })
    
    st.dataframe(df_comparativa, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("🔍 Impacto Total de Drivers")
    
    # Resumen ejecutivo
    total_26 = sum([drivers_data[r]["monto_26"] for r in rubros])
    total_25 = sum([drivers_data[r]["monto_25"] for r in rubros])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Costos Totales 2026", f"{total_26:.1f}M", delta=None)
    
    with col2:
        st.metric("Costos Totales 2025", f"{total_25:.1f}M", delta=None)
    
    with col3:
        st.metric("Variación Total", f"{total_26-total_25:+.1f}M", f"{((total_26-total_25)/total_25)*100:+.1f}%")
    
    st.markdown("---")
    
    # Análisis por categoría
    st.subheader("¿Cuál es el driver principal de cada variación?")
    
    top_drivers = []
    
    for rubro in rubros:
        data = drivers_data[rubro]
        variacion = data["monto_26"] - data["monto_25"]
        
        # Obtener el driver más importante
        if data["drivers"]:
            main_driver = data["drivers"][0]
            top_drivers.append({
                "Rubro": rubro,
                "Variación M": variacion,
                "Driver Principal": main_driver["nombre"],
                "Impacto": main_driver["variacion"]
            })
    
    df_drivers = pd.DataFrame(top_drivers)
    st.dataframe(df_drivers, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Gráfico de impacto
    st.subheader("Contribución a la Variación Total")
    
    fig_impact = go.Figure(data=[
        go.Pie(
            labels=df_drivers["Rubro"],
            values=df_drivers["Variación M"].abs(),
            hole=0.3,
            marker=dict(colors=["#667eea", "#764ba2", "#f5576c", "#4facfe", "#43e97b", "#fa709a", "#fee140"])
        )
    ])
    fig_impact.update_layout(height=400, title="Distribución de Variaciones Absolutas")
    st.plotly_chart(fig_impact, use_container_width=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
with col2:
    st.caption("Dashboard v2.0 - Análisis de Drivers")
with col3:
    st.caption("📊 Grupo CISA")
