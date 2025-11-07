import streamlit as st
import numpy as np
from datetime import datetime

# ================================================================
# Escala de Impulsividad Conductual (BIS-50 Adaptada)
# Inspirada en la lógica del BIS-11 (Atencional / Motora / No Planificada)
# Ítems originales (no son BIS-11 oficial, sin copyright)
# Autoavance + resultado profesional
# ================================================================

# ---------------------------------------------------------------
# Config general
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Escala de Impulsividad | BIS-50 Adaptada",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------
# Estilos (heredando la lógica visual del Big Five PRO)
# ---------------------------------------------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] { display:none !important; }

html, body, [data-testid="stAppViewContainer"]{
  background:#ffffff !important; color:#111 !important;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
}
.block-container{ max-width:1200px; padding-top:0.8rem; padding-bottom:2rem; }

.card{
  border:1px solid #eee; border-radius:14px; background:#fff;
  box-shadow:0 2px 0 rgba(0,0,0,0.03); padding:18px;
}
.kpi-grid{
  display:grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr));
  gap:12px; margin:10px 0 6px 0;
}
.kpi{
  border:1px solid #eee; border-radius:14px; background:#fff; padding:16px;
  position:relative; overflow:hidden;
}
.kpi .label{ font-size:.95rem; opacity:.85; }
.kpi .value{ font-size:2.2rem; font-weight:900; line-height:1; }

.dim-title{
  font-size:clamp(2.2rem, 5vw, 3.2rem);
  font-weight:900; letter-spacing:.2px; line-height:1.12;
  margin:.2rem 0 .6rem 0;
}
.dim-desc{ margin:.1rem 0 1rem 0; opacity:.9; }

.small{ font-size:0.95rem; opacity:.9; }

.badge{
  display:inline-flex; align-items:center; gap:6px; padding:.25rem .55rem; font-size:.82rem;
  border-radius:999px; border:1px solid #eaeaea; background:#fafafa;
}
hr{ border:none; border-top:1px solid #eee; margin:16px 0; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# Definición de subescalas e ítems (BIS-50 Adaptada)
# ---------------------------------------------------------------

SUBESCALAS = {
    "Atencional": "Dificultad para sostener la atención, distracción cognitiva.",
    "Motora": "Tendencia a actuar sin pensar, responder de forma impulsiva.",
    "No planificada": "Escasa planificación, priorizar el presente sobre el futuro."
}

# 50 ítems originales, agrupados según lógica BIS (no son BIS-11 oficial)
BIS_ITEMS = [
    # Atencional (1–18)
    {"id": 1, "texto": "Me cuesta mantener la atención cuando una actividad se vuelve monótona.", "subescala": "Atencional"},
    {"id": 2, "texto": "Cambio de tema en mi mente aun cuando la otra persona sigue hablando.", "subescala": "Atencional"},
    {"id": 3, "texto": "Me distraigo fácilmente con ruidos o movimientos a mi alrededor.", "subescala": "Atencional"},
    {"id": 4, "texto": "Me es difícil terminar una tarea sin revisar el celular u otras cosas.", "subescala": "Atencional"},
    {"id": 5, "texto": "Pierdo el hilo de lo que estoy haciendo con más frecuencia que otras personas.", "subescala": "Atencional"},
    {"id": 6, "texto": "Me resulta complicado concentrarme cuando tengo muchas ideas a la vez.", "subescala": "Atencional"},
    {"id": 7, "texto": "Cuando leo, avanzo páginas sin recordar bien lo que acabo de leer.", "subescala": "Atencional"},
    {"id": 8, "texto": "Me inquieta tener que escuchar explicaciones largas o muy detalladas.", "subescala": "Atencional"},
    {"id": 9, "texto": "Suelo desconectarme mentalmente en conversaciones extensas.", "subescala": "Atencional"},
    {"id": 10, "texto": "Me aburro con rapidez si la actividad requiere mucha paciencia.", "subescala": "Atencional"},
    {"id": 11, "texto": "Puedo mantener el enfoque en una tarea importante sin distraerme.", "subescala": "Atencional"},  # R
    {"id": 12, "texto": "Me organizo bien para no perder tiempo en cosas irrelevantes.", "subescala": "Atencional"},  # R
    {"id": 13, "texto": "Cuando decido concentrarme, lo logro sin mayores problemas.", "subescala": "Atencional"},  # R
    {"id": 14, "texto": "Me cuesta seguir instrucciones largas sin confundirme.", "subescala": "Atencional"},
    {"id": 15, "texto": "Paso de una idea a otra sin desarrollar ninguna por completo.", "subescala": "Atencional"},
    {"id": 16, "texto": "Me es difícil escuchar hasta el final antes de responder.", "subescala": "Atencional"},
    {"id": 17, "texto": "Cuando trabajo, mi mente se mantiene clara y ordenada.", "subescala": "Atencional"},  # R
    {"id": 18, "texto": "Me distraen mis propios pensamientos incluso en situaciones importantes.", "subescala": "Atencional"},

    # Motora (19–34)
    {"id": 19, "texto": "Actúo rápidamente sin pensar en las consecuencias.", "subescala": "Motora"},
    {"id": 20, "texto": "Digo lo primero que se me viene a la mente, incluso si puede molestar.", "subescala": "Motora"},
    {"id": 21, "texto": "A veces reacciono impulsivamente y luego me arrepiento.", "subescala": "Motora"},
    {"id": 22, "texto": "Me cuesta esperar mi turno sin intervenir.", "subescala": "Motora"},
    {"id": 23, "texto": "Tomo decisiones apresuradas en situaciones cotidianas.", "subescala": "Motora"},
    {"id": 24, "texto": "Hago compras o gastos sin haberlos planeado.", "subescala": "Motora"},
    {"id": 25, "texto": "Me resulta difícil quedarme quieto cuando algo me incomoda.", "subescala": "Motora"},
    {"id": 26, "texto": "Cambio de actividad sin terminar la anterior.", "subescala": "Motora"},
    {"id": 27, "texto": "Me involucro en situaciones solo por impulso del momento.", "subescala": "Motora"},
    {"id": 28, "texto": "Me dejo llevar por la emoción del momento al actuar.", "subescala": "Motora"},
    {"id": 29, "texto": "Antes de actuar en algo importante, siempre lo pienso con calma.", "subescala": "Motora"},  # R
    {"id": 30, "texto": "Prefiero analizar bien una situación antes de responder.", "subescala": "Motora"},  # R
    {"id": 31, "texto": "Suelo contenerme antes de decir algo cuando estoy enojado/a.", "subescala": "Motora"},  # R
    {"id": 32, "texto": "Rara vez hago algo solo por impulso.", "subescala": "Motora"},  # R
    {"id": 33, "texto": "Me cuesta controlar la urgencia de hacer algo de inmediato.", "subescala": "Motora"},
    {"id": 34, "texto": "Entro en proyectos o actividades sin evaluar si tengo tiempo o recursos.", "subescala": "Motora"},

    # No planificada (35–50)
    {"id": 35, "texto": "Prefiero disfrutar ahora y pensar después en las consecuencias.", "subescala": "No planificada"},
    {"id": 36, "texto": "Planeo con detalle mis metas a mediano y largo plazo.", "subescala": "No planificada"},  # R
    {"id": 37, "texto": "Me cuesta seguir un plan hasta el final.", "subescala": "No planificada"},
    {"id": 38, "texto": "Suelo dejar decisiones importantes para último minuto.", "subescala": "No planificada"},
    {"id": 39, "texto": "No acostumbro a evaluar bien los riesgos antes de comprometerme.", "subescala": "No planificada"},
    {"id": 40, "texto": "Me resulta difícil mantener un hábito constante de ahorro.", "subescala": "No planificada"},
    {"id": 41, "texto": "Siento que vivo más “al día” que con un plan claro.", "subescala": "No planificada"},
    {"id": 42, "texto": "Organizo mi tiempo y recursos de forma responsable.", "subescala": "No planificada"},  # R
    {"id": 43, "texto": "Cambio mis objetivos con frecuencia sin haber completado los anteriores.", "subescala": "No planificada"},
    {"id": 44, "texto": "Tomo decisiones relevantes sin recopilar suficiente información.", "subescala": "No planificada"},
    {"id": 45, "texto": "Prefiero la gratificación inmediata sobre los beneficios futuros.", "subescala": "No planificada"},
    {"id": 46, "texto": "Antes de iniciar algo importante, ya tengo una estrategia definida.", "subescala": "No planificada"},  # R
    {"id": 47, "texto": "Me cuesta mantener hábitos estables (estudio, ejercicio, proyectos personales).", "subescala": "No planificada"},
    {"id": 48, "texto": "Siento que muchas cosas importantes las hago sin una planificación real.", "subescala": "No planificada"},
    {"id": 49, "texto": "Me describiría como una persona ordenada y previsora.", "subescala": "No planificada"},  # R
    {"id": 50, "texto": "A menudo asumo compromisos sin estar seguro/a de poder cumplirlos.", "subescala": "No planificada"},
]

# Ítems con puntuación invertida (1-4 => 5 - respuesta)
INVERTIDOS = {11, 12, 13, 17, 29, 30, 31, 32, 36, 42, 46, 49}

# Escala Likert BIS-11 (adaptada): 1–4
OPCIONES = {
    "Rara vez / nunca": 1,
    "A veces": 2,
    "A menudo": 3,
    "Siempre o casi siempre": 4,
}
OPCIONES_LIST = list(OPCIONES.keys())

# Mapeo ID → índice para autoavance
ID2IDX = {item["id"]: idx for idx, item in enumerate(BIS_ITEMS)}

# ---------------------------------------------------------------
# Estado
# ---------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "inicio"  # inicio | test | resultados
if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {item["id"]: None for item in BIS_ITEMS}
if "fecha" not in st.session_state:
    st.session_state.fecha = None
if "_needs_rerun" not in st.session_state:
    st.session_state._needs_rerun = False

# ---------------------------------------------------------------
# Funciones de cálculo
# ---------------------------------------------------------------
def recodificar(item_id, valor):
    if item_id in INVERTIDOS:
        return 5 - valor
    return valor

def calcular_puntajes():
    total = 0
    sub_suma = {s: 0 for s in SUBESCALAS.keys()}
    sub_conteo = {s: 0 for s in SUBESCALAS.keys()}

    for item in BIS_ITEMS:
        item_id = item["id"]
        sub = item["subescala"]
        v = st.session_state.respuestas.get(item_id)
        if v is None:
            continue
        v_rec = recodificar(item_id, v)
        total += v_rec
        sub_suma[sub] += v_rec
        sub_conteo[sub] += 1

    sub_prom = {
        s: (sub_suma[s] / sub_conteo[s]) if sub_conteo[s] > 0 else 0
        for s in SUBESCALAS.keys()
    }

    return total, sub_suma, sub_prom

def interpretar_total(total):
    # Rango teórico BIS-50 adaptada: 50 (mínima impulsividad) a 200 (máxima)
    if total < 90:
        return "Perfil de impulsividad global **baja a moderada**. Indica buena autorregulación en la mayoría de los contextos."
    elif 90 <= total < 130:
        return "Perfil de impulsividad **moderada**. Puede manifestarse en ciertas situaciones; recomendable análisis profesional según contexto."
    else:
        return "Perfil de impulsividad **elevada**. Sugiere tendencia significativa a conductas impulsivas; se recomienda evaluación clínica especializada."

def interpretar_subescala(nombre, puntaje, promedio):
    # Interpretación simple basada en promedio 1–4:
    if promedio < 1.8:
        return f"En **{nombre}** se observa un nivel bajo de impulsividad; buena regulación en esta área."
    elif 1.8 <= promedio < 2.6:
        return f"En **{nombre}** se observa un nivel moderado de impulsividad; conviene monitorear según demandas del entorno."
    else:
        return f"En **{nombre}** se observa un nivel alto de impulsividad; puede requerir estrategias específicas de control y ajuste conductual."

# ---------------------------------------------------------------
# Callback autoavance
# ---------------------------------------------------------------
def on_answer_change(item_id: int):
    # Respuesta ya guardada por el radio; avanzamos
    idx = ID2IDX[item_id]
    if idx < len(BIS_ITEMS) - 1:
        st.session_state.q_idx = idx + 1
    else:
        st.session_state.stage = "resultados"
        st.session_state.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.session_state._needs_rerun = True

# ---------------------------------------------------------------
# Vistas
# ---------------------------------------------------------------
def view_inicio():
    st.markdown(
        """
        <div class="card">
          <h1 style="margin:0 0 6px 0; font-size:clamp(2.2rem,3.6vw,3rem); font-weight:900;">
            ⚡ Escala de Impulsividad Conductual (BIS-50 Adaptada)
          </h1>
          <p class="small" style="margin:4px 0 0 0;">
            Versión profesional inspirada en la lógica del BIS-11 (Barratt), con tres dimensiones:
            Atencional, Motora y No planificada. Uso orientativo para evaluación psicológica y laboral.
          </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([1.4, 1])
    with c1:
        st.markdown(
            """
            <div class="card">
              <h3 style="margin-top:0;">¿Qué mide esta escala?</h3>
              <ul style="line-height:1.6;">
                <li><b>Impulsividad Atencional:</b> Distracción, fuga de ideas, dificultad para sostener el foco.</li>
                <li><b>Impulsividad Motora:</b> Actuar sin pensar, respuestas rápidas, conductas impulsivas.</li>
                <li><b>Impulsividad No planificada:</b> Falta de planificación, decisiones apresuradas, vivir el presente.</li>
              </ul>
              <p class="small">
                50 ítems Likert (1–4) · Autoavance · Duración estimada: <b>8–10 minutos</b>.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="card">
              <h3 style="margin-top:0;">Instrucciones</h3>
              <ol style="line-height:1.6;">
                <li>Responda de manera honesta según su conducta habitual.</li>
                <li>No hay respuestas correctas o incorrectas.</li>
                <li>Las respuestas se avanzan automáticamente al seleccionar una opción.</li>
              </ol>
              <p class="small"><b>Importante:</b> El resultado es orientativo y debe ser interpretado por un profesional.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🚀 Iniciar evaluación", type="primary", use_container_width=True):
            st.session_state.stage = "test"
            st.session_state.q_idx = 0
            st.session_state.respuestas = {item["id"]: None for item in BIS_ITEMS}
            st.session_state.fecha = None
            st.experimental_rerun()

def view_test():
    i = st.session_state.q_idx
    item = BIS_ITEMS[i]
    total_items = len(BIS_ITEMS)
    progreso = (i + 1) / total_items

    st.progress(progreso, text=f"Progreso: {i+1}/{total_items}")

    st.markdown(
        f"""
        <div class="dim-title">
            Dimensión: {item['subescala']}
        </div>
        <p class="dim-desc">
            {SUBESCALAS[item['subescala']]}
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### {i+1}. {item['texto']}")

    prev_val = st.session_state.respuestas.get(item["id"])
    prev_idx = None
    if prev_val is not None:
        # Buscar índice de la etiqueta correspondiente
        for j, (label, val) in enumerate(OPCIONES.items()):
            if val == prev_val:
                prev_idx = j
                break

    seleccion = st.radio(
        "Selecciona una opción",
        OPCIONES_LIST,
        index=prev_idx,
        key=f"resp_{item['id']}",
        horizontal=True,
        label_visibility="collapsed",
    )

    # Guardar respuesta y auto-avanzar
    st.session_state.respuestas[item["id"]] = OPCIONES[seleccion]
    if seleccion is not None:
        on_answer_change(item["id"])

    st.markdown("</div>", unsafe_allow_html=True)

def view_resultados():
    if st.session_state.fecha is None:
        st.session_state.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    total, sub_suma, sub_prom = calcular_puntajes()

    st.markdown(
        f"""
        <div class="card">
          <h1 style="margin:0 0 4px 0; font-size:clamp(2.1rem,3.4vw,2.9rem); font-weight:900;">
            📊 Resultados — Escala de Impulsividad (BIS-50 Adaptada)
          </h1>
          <p class="small" style="margin:0;">Fecha de aplicación: <b>{st.session_state.fecha}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # KPIs básicos
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='kpi'><div class='label'>Puntaje total (50–200)</div><div class='value'>{total}</div></div>",
        unsafe_allow_html=True,
    )
    for nombre in SUBESCALAS.keys():
        st.markdown(
            f"<div class='kpi'><div class='label'>Impulsividad {nombre}</div>"
            f"<div class='value'>{sub_suma[nombre]} "
            f"<span class='small'>({sub_prom[nombre]:.2f} promedio)</span></div></div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Interpretación global (orientativa)")
    st.write(interpretar_total(total))

    st.markdown("---")
    st.subheader("Análisis por dimensiones")

    for nombre, desc in SUBESCALAS.items():
        st.markdown(f"### {nombre}")
        st.write(desc)
        st.write(
            f"- **Puntaje total**: {sub_suma[nombre]} "
            f" (promedio {sub_prom[nombre]:.2f} en escala 1–4)"
        )
        st.write(interpretar_subescala(nombre, sub_suma[nombre], sub_prom[nombre]))
        st.markdown("")

    st.markdown("---")
    st.markdown(
        """
        **Aviso importante:**  
        Esta escala es un instrumento **adaptado** basado en la lógica del BIS-11, pero no reemplaza la
        versión estandarizada oficial ni constituye diagnóstico clínico por sí sola.
        Se recomienda interpretación por psicólogo/a o psiquiatra, y uso ético en contextos laborales o clínicos.
        """
    )

    if st.button("🔄 Nueva evaluación", type="primary", use_container_width=True):
        st.session_state.stage = "inicio"
        st.session_state.q_idx = 0
        st.session_state.respuestas = {item["id"]: None for item in BIS_ITEMS}
        st.session_state.fecha = None
        st.experimental_rerun()

# ---------------------------------------------------------------
# Controlador principal
# ---------------------------------------------------------------
if st.session_state.stage == "inicio":
    view_inicio()
elif st.session_state.stage == "test":
    view_test()
elif st.session_state.stage == "resultados":
    view_resultados()

# Rerun si se marcó desde el callback
if st.session_state._needs_rerun:
    st.session_state._needs_rerun = False
    st.experimental_rerun()
