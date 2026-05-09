import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="ASO Master - Auditoría de Salud Organizacional", layout="wide")

# Estilos personalizados
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .dimension-header { color: #1e3a8a; font-size: 24px; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Inicialización de estado
if 'paso' not in st.session_state:
    st.session_state.paso = 'landing'
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}

# BANCO DE DATOS Y LÓGICA
# Se definen las dimensiones y si requieren inversión (6 - X)
dimensiones = {
    "Exigencias Psicológicas": {"rango": range(1, 9), "inv": []},
    "Control y Autonomía": {"rango": range(9, 17), "inv": range(9, 17)},
    "Apoyo Social y Liderazgo": {"rango": range(17, 25), "inv": range(17, 25)},
    "Recompensa y Sentido": {"rango": range(25, 33), "inv": range(25, 33)},
    "Vida Personal": {"rango": range(33, 41), "inv": [33, 36, 37, 39, 40]},
    "Loops Neuropsicológicos": {"rango": range(41, 51), "inv": []}
}

# Texto de las 50 preguntas
preguntas_texto = {
    1: "Siento que la velocidad exigida en mis tareas supera habitualmente mi capacidad de respuesta.",
    2: "La distribución de mis labores suele ser irregular, generando 'cuellos de botella'.",
    3: "El volumen de actividades pendientes me obliga a sacrificar la calidad por la rapidez.",
    4: "Mi atención se siente fragmentada por saltar constantemente de un tema a otro.",
    5: "Al finalizar el día, experimento un agotamiento mental que me impide mi vida personal.",
    6: "Percibo que las metas de mi área son poco realistas para el tiempo disponible.",
    7: "Es habitual que deba resolver urgencias externas que interrumpen mi planificación.",
    8: "La complejidad de mis funciones requiere un nivel de alerta desgastador.",
    9: "Siento que tengo un margen de decisión real sobre la organización de mi agenda.",
    10: "La institución valora e incorpora mis sugerencias para optimizar los procesos.",
    11: "Mi jefatura me otorga la confianza para resolver problemas según mi criterio.",
    12: "Tengo la oportunidad de aplicar mis habilidades de forma creativa.",
    13: "Siento que puedo influir en las decisiones que afectan mi flujo de trabajo.",
    14: "El diseño de mis tareas me permite aprender nuevas competencias.",
    15: "Percibo que los métodos de trabajo son flexibles y se adaptan a la realidad.",
    16: "Siento que mis acciones tienen un impacto visible en el éxito del departamento.",
    17: "En mi entorno de trabajo prima la colaboración sobre la competencia individual.",
    18: "Mi líder directo comunica los objetivos con claridad y sin ambigúedades.",
    19: "Siento que puedo contar con el apoyo técnico de mis superiores ante imprevistos.",
    20: "El clima de mi unidad permite expresar desacuerdos de forma segura.",
    21: "Mi jefatura equilibra las metas con el bienestar del equipo.",
    22: "Recibo información oportuna sobre los cambios que ocurren en la organización.",
    23: "Existe disposición entre compañeros para ayudarnos en momentos de alta carga.",
    24: "Las situaciones de conflicto son gestionadas de forma justa y equitativa.",
    25: "Siento que el esfuerzo que invierto en mi labor es reconocido de forma genuina.",
    26: "Las perspectivas de desarrollo o crecimiento son claras para mí.",
    27: "Percibo que mi salario y beneficios son coherentes con mi responsabilidad.",
    28: "Mi trabajo me entrega una satisfacción personal más allá de lo económico.",
    29: "La organización es justa en la forma en que distribuye premios y méritos.",
    30: "El propósito de mi cargo está alineado con mis valores personales.",
    31: "Me siento valorado como profesional por parte de mi jefatura y pares.",
    32: "Siento que la institución se preocupa por mi estabilidad laboral.",
    33: "Me resulta sencillo desconectarme del trabajo en mis periodos de descanso.",
    34: "Siento que mi entorno personal se ve afectado por la tensión del trabajo.",
    35: "Percibo que deba estar disponible para la organización fuera de mi jornada.",
    36: "Mi vida familiar tiene un espacio respetado por la empresa.",
    37: "Siento que el sistema de trabajo protege mi salud física y mental.",
    38: "He tenido que postergar necesidades personales básicas para cumplir mi labor.",
    39: "La organización fomenta una cultura de desconexión efectiva.",
    40: "Siento que mi nivel de vitalidad es suficiente para los desafíos diarios.",
    41: "¿Sientes que el trabajo te 'persigue' mentalmente después de la salida?",
    42: "¿Has llegado a sentir que nada de lo que hagas cambiará realmente las cosas?",
    43: "¿Prefieres callar tus dificultades para no parecer un eslabón débil?",
    44: "¿Sientes que tu compromiso con la organización se ha enfriado?",
    45: "¿Te sientes tan saturado que te cuesta procesar información nueva?",
    46: "¿Vives con la sensación de que siempre está a punto de ocurrir una emergencia?",
    47: "¿Sientes que el líder de tu área es una fuente de incertidumbre?",
    48: "¿Percibes que la carga administrativa te quita tiempo para lo importante?",
    49: "¿Sientes que el esfuerzo que das es mucho mayor a lo que recibes?",
    50: "¿Te sientes emocionalmente agotado antes de interactuar con colegas?"
}

# --- NAVEGACIÓN ---
if st.session_state.paso == 'landing':
    st.title("🚀 Proyecto ASO Master")
    st.subheader("Auditoría de Salud Organizacional y Liderazgo Neuro-Sistémico")
    st.write("Bienvenido, Claudio. Esta herramienta permite diagnosticar con precisión científica los riesgos de tu organización.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Items", "50")
    col2.metric("Dimensiones", "6")
    col3.metric("Versión", "2026")

    if st.button("Iniciar Auditoría Digital"):
        st.session_state.paso = 'cuestionario'
        st.rerun()

elif st.session_state.paso == 'cuestionario':
    idx = len(st.session_state.respuestas) + 1
    
    if idx <= 50:
        # Identificar dimensión actual
        dim_actual = ""
        for nombre, info in dimensiones.items():
            if idx in info["rango"]:
                dim_actual = nombre
                break
        
        st.markdown(f"<div class='dimension-header'>{dim_actual}</div>", unsafe_allow_html=True)
        st.progress(idx / 50)
        st.write(f"Pregunta {idx} de 50")
        st.subheader(preguntas_texto[idx])
        
        opciones = {
            "Totalmente de acuerdo": 5,
            "De acuerdo": 4,
            "Ni de acuerdo ni en desacuerdo": 3,
            "En desacuerdo": 2,
            "Totalmente en desacuerdo": 1
        }
        
        seleccion = st.radio("Selecciona tu respuesta:", list(opciones.keys()), key=f"q_{idx}")
        
        if st.button("Siguiente"):
            st.session_state.respuestas[idx] = opciones[seleccion]
            st.rerun()
    else:
        st.session_state.paso = 'resultados'
        st.rerun()

elif st.session_state.paso == 'resultados':
    st.title("📊 Dashboard de Resultados ASO")
    
    # Procesamiento de datos
    datos_finales = []
    for nombre, info in dimensiones.items():
        valores = []
        for i in info["rango"]:
            val = st.session_state.respuestas[i]
            # Lógica inversa: 6 - X
            if i in info["inv"]:
                val = 6 - val
            valores.append(val)
        
        promedio = sum(valores) / len(valores)
        # Punto de corte 3.5[cite: 1]
        estado = "Riesgo Presente 🔴" if promedio >= 3.5 else "Riesgo Ausente 🟢"
        datos_finales.append({"Dimensión": nombre, "Promedio": round(promedio, 2), "Estado": estado})

    df = pd.DataFrame(datos_finales)
    
    # Visualización
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.dataframe(df, use_container_width=True)
    
    with col_b:
        fig = px.polar_bar(df, r="Promedio", theta="Dimensión", color="Estado", 
                           color_discrete_map={"Riesgo Presente 🔴": "red", "Riesgo Ausente 🟢": "green"},
                           range_r=[0, 5], title="Mapa de Riesgos Neuro-Sistémicos")
        st.plotly_chart(fig)

    st.divider()
    st.write("**Conclusión Técnica:**")
    peor_dim = df.loc[df['Promedio'].idxmax()]
    st.info(f"La dimensión con mayor impacto es **{peor_dim['Dimensión']}**. Se sugiere aplicar el módulo focalizado (40%) de la metodología de Claudio Chamond.")

    if st.button("Reiniciar Aplicación"):
        st.session_state.paso = 'landing'
        st.session_state.respuestas = {}
        st.rerun()
