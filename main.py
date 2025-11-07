# ================================================================
# Escala de Impulsividad - Estilo BIS-11 (Versión Adaptada, 30 ítems)
# Estructura tipo Test Big Five (autoavance + vista resultados)
# ================================================================

import streamlit as st
import numpy as np
from datetime import datetime

# ---------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Escala de Impulsividad | BIS-11 Adaptada",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------
# Estilos base (inspirados en tu app Big Five)
# ---------------------------------------------------------------
st.markdown(
    """
<style>
[data-testid="stSidebar"] { display: none !important; }

html, body, [data-testid="stAppViewContainer"] {
  background: #ffffff !important;
  color: #111111 !important;
  font-family: -apple-system, system-ui, BlinkMacSystemFont, "SF Pro Text",
               -system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Helvetica, Arial, sans-serif;
}

.block-container {
  max-width: 1100px;
  padding-top: 0.8rem;
  padding-bottom: 2rem;
}

/* Tarjetas */
.card {
  border: 1px solid #eee;
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 2px 4px rgba(15,23,42,0.04);
  padding: 18px 18px 16px 18px;
  margin-bottom: 12px;
}

.dim-title {
  font-size: clamp(2.0rem, 3.2vw, 2.6rem);
  font-weight: 900;
  margin: 0.2rem 0 0.2rem 0;
}

.dim-subtitle {
  font-size: 0.98rem;
  opacity: 0.9;
  margin-bottom: 0.6rem;
}

.small {
  font-size: 0.9rem;
  opacity: 0.9;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 10px;
  margin: 12px 0;
}

.kpi {
  border-radius: 14px;
  border: 1px solid #eee;
  padding: 12px 14px;
  background: #fafafa;
}

.kpi-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  opacity: 0.75;
}

.kpi-value {
  font-size: 1.6rem;
  font-weight: 800;
  margin-top: 2px;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0.18rem 0.55rem;
  font-size: 0.78rem;
  border-radius: 999px;
  border: 1px solid #e5e5e5;
  background: #f9f9f9;
}

.result-section {
  border-radius: 12px;
  border: 1px solid #eee;
  padding: 12px 14px;
  margin-bottom: 8px;
  background: #ffffff;
}
</style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# Definición de dimensiones y preguntas (30 ítems)
# Lógica BIS-11: Atencional, Motora, No planificada
# Ítems originales, NO BIS-11 oficial.
# ---------------------------------------------------------------

DIMENSIONES = {
    "Atencional": "Dificultad para mantener foco, distracción cognitiva, salto de ideas.",
    "Motora": "Actuar sin pensar, respuestas impulsivas, dificultad para frenar conductas.",
    "No planificada": "Baja planificación, decisiones apresuradas, foco en el corto plazo."
}

# Cada pregunta:
# - text: enunciado
# - dim: subescala
# - key: identificador
# - rev: True si es ítem invertido (se recodifica 5 - respuesta)
QUESTIONS = [
    # Atencional (10)
    {"text": "Me cuesta mantener mi atención cuando una actividad se vuelve monótona.", "dim": "Atencional", "key": "A1", "rev": False},
    {"text": "Me distraigo con facilidad por ruidos o estímulos externos.", "dim": "Atencional", "key": "A2", "rev": False},
    {"text": "Pierdo el hilo de lo que hago con más frecuencia que otras personas.", "dim": "Atencional", "key": "A3", "rev": False},
    {"text": "Cuando leo o escucho, mi mente se va a otros temas.", "dim": "Atencional", "key": "A4", "rev": False},
    {"text": "Puedo concentrarme bien cuando la tarea es importante para mí.", "dim": "Atencional", "key": "A5", "rev": True},
    {"text": "Me organizo para minimizar distracciones cuando necesito enfocarme.", "dim": "Atencional", "key": "A6", "rev": True},
    {"text": "Las instrucciones largas me confunden o las olvido con facilidad.", "dim": "Atencional", "key": "A7", "rev": False},
    {"text": "Cambio de una idea a otra sin terminar de desarrollar ninguna.", "dim": "Atencional", "key": "A8", "rev": False},
    {"text": "Suelo interrumpir mentalmente una explicación porque me aburro.", "dim": "Atencional", "key": "A9", "rev": False},
    {"text": "Mantengo mi mente clara y ordenada al trabajar.", "dim": "Atencional", "key": "A10", "rev": True},

    # Motora (10)
    {"text": "Actúo rápidamente sin pensar en las consecuencias.", "dim": "Motora", "key": "M1", "rev": False},
    {"text": "Digo lo primero que pienso aunque pueda generar conflicto.", "dim": "Motora", "key": "M2", "rev": False},
    {"text": "Me cuesta esperar mi turno sin intervenir.", "dim": "Motora", "key": "M3", "rev": False},
    {"text": "Hago compras o decisiones impulsivas sin planearlas.", "dim": "Motora", "key": "M4", "rev": False},
    {"text": "Antes de actuar en algo relevante, me detengo a analizarlo.", "dim": "Motora", "key": "M5", "rev": True},
    {"text": "Puedo contenerme cuando siento la necesidad de reaccionar de inmediato.", "dim": "Motora", "key": "M6", "rev": True},
    {"text": "Cambio de actividad sin haber terminado la anterior.", "dim": "Motora", "key": "M7", "rev": False},
    {"text": "Me involucro en situaciones solo por la emoción del momento.", "dim": "Motora", "key": "M8", "rev": False},
    {"text": "Rara vez hago algo solo por impulso.", "dim": "Motora", "key": "M9", "rev": True},
    {"text": "Suelo reaccionar primero y pensar después.", "dim": "Motora", "key": "M10", "rev": False},

    # No planificada (10)
    {"text": "Prefiero disfrutar ahora y pensar después en las consecuencias.", "dim": "No planificada", "key": "N1", "rev": False},
    {"text": "Planifico mis metas a mediano y largo plazo.", "dim": "No planificada", "key": "N2", "rev": True},
    {"text": "Me cuesta seguir un plan hasta el final.", "dim": "No planificada", "key": "N3", "rev": False},
    {"text": "Tomo decisiones importantes sin evaluar suficiente información.", "dim": "No planificada", "key": "N4", "rev": False},
    {"text": "Mantengo hábitos estables (ahorro, estudio, autocuidado).", "dim": "No planificada", "key": "N5", "rev": True},
    {"text": "Suelo dejar asuntos importantes para último minuto.", "dim": "No planificada", "key": "N6", "rev": False},
    {"text": "Cambio mis objetivos con frecuencia sin completarlos.", "dim": "No planificada", "key": "N7", "rev": False},
    {"text": "Me describiría como ordenado/a y previsor/a.", "dim": "No planificada", "key": "N8", "rev": True},
    {"text": "Asumo compromisos sin estar seguro/a de poder cumplirlos.", "dim": "No planificada", "key": "N9", "rev": False},
    {"text": "Evalúo los riesgos antes de tomar decisiones importantes.", "dim": "No planificada", "key": "N10", "rev": True},
]

DIM_LIST = list(DIMENSIONES.keys())
KEY2IDX = {q["key"]: i for i, q in enumerate(QUESTIONS)}

# Escala Likert 1–4
LIK_LABELS = [
    "1 - Rara vez / nunca",
    "2 - A veces",
    "3 - A menudo",
    "4 - Casi siempre / siempre",
]
LIK_MAP = {
    LIK_LABELS[0]: 1,
    LIK_LABELS[1]: 2,
    LIK_LABELS[2]: 3,
    LIK_LABELS[3]: 4,
}

# ---------------------------------------------------------------
# Estado global
# ---------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "inicio"           # inicio | test | resultados
if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = {q["key"]: None for q in QUESTIONS}
if "fecha" not in st.session_state:
    st.session_state.fecha = None
if "_needs_rerun" not in st.session_state:
    st.session_state._needs_rerun = False

# ---------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------
def recode(value: int, rev: bool) -> int:
    if value is None:
        return None
    return (5 - value) if rev else value

def compute_scores(answers: dict):
    """
    Devuelve:
      - total_raw: suma total (30–120)
      - dim_raw: dict dimensión -> suma cruda
      - dim_norm: dict dimensión -> 0-100 normalizado
    """
    dim_values = {d: [] for d in DIM_LIST}
    total_raw = 0

    for q in QUESTIONS:
        v = answers.get(q["key"])
        if v is None:
            continue
        v_rec = recode(v, q["rev"])
        total_raw += v_rec
        dim_values[q["dim"]].append(v_rec)

    dim_raw = {d: (sum(vals) if vals else 0) for d, vals in dim_values.items()}
    dim_norm = {}
    for d, vals in dim_values.items():
        if not vals:
            dim_norm[d] = 0.0
            continue
        # Normalización 0–100: mínimo = 1 * n, máximo = 4 * n
        n = len(vals)
        raw = sum(vals)
        min_s = 1 * n
        max_s = 4 * n
        dim_norm[d] = (raw - min_s) / (max_s - min_s) * 100 if max_s > min_s else 0.0

    return total_raw, dim_raw, dim_norm

def interpret_total(total_raw: int):
    # Rango: 30 (mínima impulsividad) a 120 (máxima)
    if total_raw < 60:
        return "Impulsividad global **baja a moderada**. Indica buena autorregulación en la mayoría de los contextos."
    elif 60 <= total_raw < 85:
        return "Impulsividad global **moderada**. Puede impactar algunas decisiones; recomendable monitoreo según contexto personal o laboral."
    else:
        return "Impulsividad global **elevada**. Sugiere tendencia marcada a responder impulsivamente; se recomienda evaluación profesional detallada."

def interpret_dim(dim: str, raw: int, norm: float):
    if norm < 35:
        lvl = "baja"
        txt = f"En {dim.lower()} se observa impulsividad baja; buena regulación en esta área."
    elif 35 <= norm < 65:
        lvl = "moderada"
        txt = f"En {dim.lower()} se observa impulsividad moderada; conviene observar cómo influye en decisiones clave."
    else:
        lvl = "alta"
        txt = f"En {dim.lower()} se observa impulsividad alta; puede requerir estrategias específicas de control y planificación."
    return lvl, txt

# ---------------------------------------------------------------
# Callback: autoavance al responder
# ---------------------------------------------------------------
def on_answer_change(qkey: str):
    # La radio ya guardó el valor en session_state; lo leemos
    val_label = st.session_state.get(f"resp_{qkey}")
    if val_label is None:
        return
    st.session_state.answers[qkey] = LIK_MAP[val_label]

    # Calcular siguiente pregunta
    idx = KEY2IDX[qkey]
    if idx < len(QUESTIONS) - 1:
        st.session_state.q_idx = idx + 1
        st.session_state.stage = "test"
    else:
        # Última pregunta: ir a resultados
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
          <h1 class="dim-title">⚡ Escala de Impulsividad — Modelo BIS-11 Adaptado</h1>
          <p class="small">
            Versión profesional de 30 ítems, con tres dimensiones: Impulsividad Atencional, Motora y No Planificada.
            Basada en la lógica del BIS-11, con enunciados originales para uso ético y libre.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown(
            f"""
            <div class="card">
              <h3>¿Qué mide?</h3>
              <ul class="small">
                <li><b>Atencional:</b> Distracción, dificultad para mantener el foco.</li>
                <li><b>Motora:</b> Actuar sin pensar, reacciones rápidas.</li>
                <li><b>No planificada:</b> Falta de planificación, decisiones apresuradas.</li>
              </ul>
              <p class="small">
                Número de ítems: <b>{len(QUESTIONS)}</b><br>
                Respuesta: escala Likert 1–4.<br>
                Duración estimada: <b>5–7 minutos</b>.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="card">
              <h3>Instrucciones</h3>
              <ol class="small">
                <li>Responda según su conducta habitual, no como le gustaría ser.</li>
                <li>No hay respuestas correctas o incorrectas.</li>
                <li>Al seleccionar una opción, la prueba avanza automáticamente.</li>
              </ol>
              <p class="small">
                <b>Uso orientativo:</b> La interpretación debe ser realizada por un profesional competente.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("🚀 Iniciar evaluación", type="primary", use_container_width=True):
        st.session_state.stage = "test"
        st.session_state.q_idx = 0
        st.session_state.answers = {q["key"]: None for q in QUESTIONS}
        st.session_state.fecha = None
        st.rerun()

def view_test():
    i = st.session_state.q_idx
    q = QUESTIONS[i]
    dim = q["dim"]
    progreso = (i + 1) / len(QUESTIONS)

    st.progress(progreso, text=f"Progreso: {i+1}/{len(QUESTIONS)}")

    st.markdown(
        f"""
        <div class="card">
          <div class="dim-title">📋 Pregunta {i+1} de {len(QUESTIONS)}</div>
          <div class="dim-subtitle">
            Dimensión: <b>{dim}</b> — {DIMENSIONES[dim]}
          </div>
          <p style="font-size:1.05rem; margin-top:0.4rem;"><b>{q['text']}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    prev_val = st.session_state.answers.get(q["key"])
    if prev_val is None:
        prev_index = 0
    else:
        # Buscar índice según valor previo
        prev_index = [v for v in LIK_MAP.values()].index(prev_val)

    st.radio(
        "Selecciona una opción",
        options=LIK_LABELS,
        index=prev_index,
        key=f"resp_{q['key']}",
        horizontal=True,
        label_visibility="collapsed",
        on_change=on_answer_change,
        args=(q["key"],),
    )

def view_resultados():
    if st.session_state.fecha is None:
        st.session_state.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    total_raw, dim_raw, dim_norm = compute_scores(st.session_state.answers)

    st.markdown(
        f"""
        <div class="card">
          <h1 class="dim-title">📊 Resultados — Escala de Impulsividad Adaptada</h1>
          <p class="small">Fecha de aplicación: <b>{st.session_state.fecha}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # KPIs
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='kpi'>
          <div class='kpi-label'>Puntaje total (30–120)</div>
          <div class='kpi-value'>{total_raw}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for d in DIM_LIST:
        st.markdown(
            f"""
            <div class='kpi'>
              <div class='kpi-label'>Impulsividad {d} (normalizada 0–100)</div>
              <div class='kpi-value'>{dim_norm[d]:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Interpretación global
    st.markdown("### Interpretación global (orientativa)")
    st.write(interpret_total(total_raw))

    # Detalle por dimensión
    st.markdown("### Análisis por dimensiones")
    for d in DIM_LIST:
        lvl, txt = interpret_dim(d, dim_raw[d], dim_norm[d])
        st.markdown(
            f"""
            <div class="result-section">
              <div class="badge">Impulsividad {d} · {lvl.upper()}</div>
              <p class="small" style="margin-top:4px;">
                Puntaje bruto: <b>{dim_raw[d]}</b> · Índice normalizado: <b>{dim_norm[d]:.1f}/100</b>
              </p>
              <p class="small">{txt}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        **Aviso importante:**  
        Esta escala es una adaptación basada en la lógica del BIS-11, con ítems originales.
        No sustituye la versión estandarizada oficial ni constituye diagnóstico clínico por sí sola.
        Su uso e interpretación deben ser realizados por profesionales de la salud mental o expertos en evaluación psicológica.
        """
    )

    if st.button("🔄 Realizar nueva evaluación", type="primary", use_container_width=True):
        st.session_state.stage = "inicio"
        st.session_state.q_idx = 0
        st.session_state.answers = {q["key"]: None for q in QUESTIONS}
        st.session_state.fecha = None
        st.rerun()

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
    st.rerun()
