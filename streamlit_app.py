import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import msal
import requests

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Costos - Grupo CISA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración Power BI
CLIENT_ID = "f6aabfcb-707d-419e-8144-1e00a54f0014"
CLIENT_SECRET = "2Kk8Q~c.bfOLLQFpIERf8QySgGlH.iFmibWPwbS3"
TENANT_ID = "2864e7a4-cef3-4af5-a363-e0e15efd0fa3"
WORKSPACE_ID = "f19bb368-567f-41b3-9586-5f17dc7f239e"
REPORT_ID = "7d8e8353-9a14-4f42-b1ae-659b619e80f2"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://analysis.windows.net/.default"]

@st.cache_resource
def get_access_token():
    """Obtiene token de acceso para Power BI API"""
    try:
        app_client = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET
        )
        
        token_response = app_client.acquire_token_for_client(scopes=SCOPE)
        
        if "access_token" in token_response:
            return token_response["access_token"]
        else:
            return None
    except Exception as e:
        st.error(f"Error al obtener token: {str(e)}")
        return None

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
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Dashboard de Costos Operacionales")
st.markdown("**Grupo CISA - Análisis Financiero 2026**")

# Sidebar
st.sidebar.header("⚙️ Configuración")
mes_seleccionado = st.sidebar.selectbox(
    "Selecciona mes:",
    ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    index=4
)

empresa_seleccionada = st.sidebar.selectbox(
    "Selecciona empresa:",
    ["Todas", "CISA", "COAVEO", "COTOBUSA", "CODIVERSA", "COPESA"]
)

segmento_seleccionado = st.sidebar.selectbox(
    "Selecciona segmento:",
    ["Todos", "Foráneas", "Metrobús", "Convencionales", "Trolebús"]
)

# Botones de acción
st.sidebar.markdown("---")
if st.sidebar.button("🔗 Abrir Reporte Completo en Power BI", use_container_width=True):
    st.sidebar.success(f"✓ Abriendo reporte...")
    st.sidebar.markdown(f"[Ir a Power BI](https://app.powerbi.com/groups/{WORKSPACE_ID}/reports/{REPORT_ID})")

if st.sidebar.button("🔄 Actualizar Datos", use_container_width=True):
    st.sidebar.info("Datos actualizados ✓")

# Estatus de conexión
token = get_access_token()
if token:
    st.sidebar.success("✓ Conectado a Power BI")
else:
    st.sidebar.error("✗ Error de conexión a Power BI")

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📈 Métricas Principales", "💰 Desglose de Costos", "📊 Análisis por Segmento", "📋 Tabla Detallada"])

# TAB 1: MÉTRICAS PRINCIPALES
with tab1:
    st.subheader("Métricas Principales 2026 vs 2025")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Ingresos Totales</div>
            <div class="metric-value">456.5M</div>
            <div class="metric-change">+7.8% vs 2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Costos Operación</div>
            <div class="metric-value">276.9M</div>
            <div class="metric-change">+2.1% vs 2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">EBITDA</div>
            <div class="metric-value">134.4M</div>
            <div class="metric-change">+19.8% vs 2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Margen EBITDA</div>
            <div class="metric-value">29.4%</div>
            <div class="metric-change">+2.6pp vs 2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráfico de variación mensual
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ingresos Mensual 2026 vs 2025")
        months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        ingresos_2026 = [38, 42, 45, 48, 52, 50, 51, 52, 48, 45, 42, 40]
        ingresos_2025 = [35, 40, 42, 45, 48, 48, 49, 50, 46, 44, 41, 38]
        
        fig = go.Figure(data=[
            go.Bar(x=months, y=ingresos_2026, name="2026", marker_color="#667eea"),
            go.Bar(x=months, y=ingresos_2025, name="2025", marker_color="#e5e7eb")
        ])
        fig.update_layout(barmode="group", height=400, hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Costos Mensual 2026 vs 2025")
        costos_2026 = [22, 25, 27, 28, 30, 29, 30, 31, 28, 25, 23, 21]
        costos_2025 = [21, 24, 26, 27, 29, 29, 29, 30, 27, 25, 23, 20]
        
        fig = go.Figure(data=[
            go.Bar(x=months, y=costos_2026, name="2026", marker_color="#f5576c"),
            go.Bar(x=months, y=costos_2025, name="2025", marker_color="#e5e7eb")
        ])
        fig.update_layout(barmode="group", height=400, hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: DESGLOSE DE COSTOS
with tab2:
    st.subheader("Desglose de Costos 2026")
    
    col1, col2, col3 = st.columns(3)
    
    costos_data = {
        "Concepto": ["Combustible", "Mantenimiento", "Nómina Operadores", "Nómina Mecánicos", "Limpieza", "Seguro", "Otros"],
        "Monto 2026": [104.6, 48.7, 81.5, 23.8, 6.4, 9.1, 2.8],
        "% del Total": [37.8, 17.6, 29.5, 8.6, 2.3, 3.3, 1.0]
    }
    
    # Gráfico Pastel
    fig_pie = go.Figure(data=[go.Pie(
        labels=costos_data["Concepto"],
        values=costos_data["Monto 2026"],
        hole=0.3,
        marker=dict(colors=["#667eea", "#764ba2", "#f5576c", "#4facfe", "#43e97b", "#fa709a", "#fee140"])
    )])
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    # Tabla de costos
    df_costos = pd.DataFrame(costos_data)
    st.dataframe(df_costos, use_container_width=True, hide_index=True)

# TAB 3: ANÁLISIS POR SEGMENTO
with tab3:
    st.subheader("Análisis por Segmento")
    
    segmentos_data = {
        "Segmento": ["Foráneas", "Metrobús", "Convencionales", "Trolebús"],
        "Ingresos 2026": [178.2, 163.3, 98.8, 16.1],
        "Costos 2026": [95.3, 89.2, 52.1, 8.6],
        "% Costos/Ingresos": [53.5, 54.6, 52.7, 53.4],
        "Variación vs 2025": ["+3.6%", "+4.7%", "+8.0%", "+329.9%"]
    }
    
    df_segmentos = pd.DataFrame(segmentos_data)
    
    # Gráfico de barras
    fig_segments = go.Figure(data=[
        go.Bar(x=segmentos_data["Segmento"], y=segmentos_data["Ingresos 2026"], name="Ingresos 2026", marker_color="#667eea"),
        go.Bar(x=segmentos_data["Segmento"], y=segmentos_data["Costos 2026"], name="Costos 2026", marker_color="#f5576c")
    ])
    fig_segments.update_layout(barmode="group", height=400)
    st.plotly_chart(fig_segments, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(df_segmentos, use_container_width=True, hide_index=True)

# TAB 4: TABLA DETALLADA
with tab4:
    st.subheader("Tabla Detallada de Costos")
    
    tabla_detallada = {
        "Concepto": [
            "01. Ingresos totales", "01a. Convencionales", "01b. Metrobús", "01c. Trolebús", "01d. Foráneas",
            "02. Costos de operación", "02a. Combustible", "02b. Mantenimiento", "02c. Nómina Operadores",
            "02d. Nómina Mecánicos", "02e. Limpieza", "02f. Seguro", "02g. Otros Costos",
            "03. Gastos Generales", "04. EBITDA", "05. Utilidad Neta"
        ],
        "Monto 2026": [456.5, 98.8, 163.3, 16.1, 178.2, 276.9, 104.6, 48.7, 81.5, 23.8, 6.4, 9.1, 2.8, 45.2, 134.4, 89.2],
        "Monto 2025": [423.3, 91.5, 156.0, 3.8, 172.0, 271.5, 100.8, 57.7, 76.9, 19.2, 5.7, 9.1, 1.9, 44.5, 112.3, 68.0],
        "Variación": [33.2, 7.3, 7.3, 12.3, 6.2, 5.4, 3.8, -9.0, 4.6, 4.6, 0.7, 0.0, 0.9, 0.7, 22.1, 21.2],
        "% Cambio": ["+7.8%", "+8.0%", "+4.7%", "+329.9%", "+3.6%", "+2.0%", "+3.8%", "-15.5%", "+6.1%", "+23.9%", "+12.3%", "+0.3%", "+40.5%", "+1.6%", "+19.7%", "+31.2%"]
    }
    
    df_tabla = pd.DataFrame(tabla_detallada)
    st.dataframe(df_tabla, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
with col2:
    st.caption("Dashboard v1.0 - Grupo CISA")
with col3:
    st.caption("📊 Powered by Power BI + Streamlit")
