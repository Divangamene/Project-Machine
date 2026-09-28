import streamlit as st
import pandas as pd
import joblib


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Machine Condition Assessment",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .stApp {
        background: #F7F8FA;
        color: #172033;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }


    /* ========================================================
       TYPOGRAPHY
       ======================================================== */

    html, body, [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }


    /* ========================================================
       TOP BAR
       ======================================================== */

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding-bottom: 1.5rem;
        margin-bottom: 2rem;

        border-bottom: 1px solid #E5E7EB;
    }

    .brand {
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #172033;
    }

    .system-status {
        display: flex;
        align-items: center;
        gap: 8px;

        font-size: 0.75rem;
        font-weight: 600;
        color: #667085;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #18A36B;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        margin-bottom: 2.5rem;
    }

    .hero-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #667085;

        letter-spacing: 0.12em;
        text-transform: uppercase;

        margin-bottom: 0.6rem;
    }

    .hero-title {
        font-size: 2.5rem;
        line-height: 1.1;
        font-weight: 650;

        color: #101828;

        margin: 0;
    }

    .hero-description {
        max-width: 680px;

        margin-top: 0.8rem;

        color: #667085;
        font-size: 1rem;
        line-height: 1.6;
    }


    /* ========================================================
       SECTION
       ======================================================== */

    .section-header {
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 0.78rem;
        font-weight: 700;

        letter-spacing: 0.1em;
        text-transform: uppercase;

        color: #475467;
    }


    /* ========================================================
       CARDS
       ======================================================== */

    .card {
        background: #FFFFFF;

        border: 1px solid #E4E7EC;
        border-radius: 12px;

        padding: 1.5rem;

        margin-bottom: 1rem;
    }

    .card-title {
        font-size: 1rem;
        font-weight: 650;

        color: #101828;

        margin-bottom: 0.25rem;
    }

    .card-description {
        font-size: 0.84rem;
        color: #667085;

        margin-bottom: 1.2rem;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    .metric-card {
        background: #FFFFFF;

        border: 1px solid #E4E7EC;
        border-radius: 12px;

        padding: 1.3rem 1.4rem;
    }

    .metric-label {
        color: #667085;

        font-size: 0.72rem;
        font-weight: 650;

        text-transform: uppercase;
        letter-spacing: 0.07em;
    }

    .metric-value {
        color: #101828;

        font-size: 1.55rem;
        font-weight: 650;

        margin-top: 0.35rem;
    }


    /* ========================================================
       RESULT
       ======================================================== */

    .assessment {
        background: #FFFFFF;

        border: 1px solid #D0D5DD;
        border-radius: 14px;

        padding: 2rem;

        margin-top: 1.5rem;
    }

    .assessment-label {
        color: #667085;

        font-size: 0.72rem;
        font-weight: 700;

        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .assessment-status {
        font-size: 2rem;
        font-weight: 700;

        margin-top: 0.5rem;
        margin-bottom: 0.25rem;
    }

    .assessment-description {
        color: #667085;
        font-size: 0.92rem;
    }

    .normal {
        color: #087443;
    }

    .warning {
        color: #B54708;
    }

    .critical {
        color: #B42318;
    }


    /* ========================================================
       PROBABILITY
       ======================================================== */

    .probability-wrapper {
        margin-top: 1.7rem;
    }

    .probability-header {
        display: flex;
        justify-content: space-between;

        margin-bottom: 0.55rem;

        font-size: 0.82rem;
        color: #475467;
    }

    .probability-value {
        font-weight: 700;
        color: #101828;
    }

    .progress-background {
        width: 100%;
        height: 7px;

        background: #EAECF0;

        border-radius: 10px;

        overflow: hidden;
    }

    .progress-fill {
        height: 100%;

        border-radius: 10px;

        background: #344054;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    .stButton > button {
        width: 100%;

        height: 3rem;

        border-radius: 8px;

        border: 1px solid #172033;

        background: #172033;
        color: #FFFFFF;

        font-size: 0.86rem;
        font-weight: 650;

        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        background: #273449;
        border-color: #273449;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    div[data-baseweb="input"] {
        border-radius: 7px;
    }

    label {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        color: #344054 !important;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        border-color: #E4E7EC;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        border-top: 1px solid #E4E7EC;

        margin-top: 3rem;
        padding-top: 1.5rem;

        display: flex;
        justify-content: space-between;

        color: #98A2B3;

        font-size: 0.72rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load("modelo.pkl")


try:
    model = load_model()
    model_loaded = True

except Exception:
    model = None
    model_loaded = False


# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    """
    <div class="topbar">

        <div class="brand">
            Machine Condition Assessment
        </div>

        <div class="system-status">
            <span class="status-dot"></span>
            System operational
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-label">
            Predictive Maintenance
        </div>

        <div class="hero-title">
            Machine condition assessment
        </div>

        <div class="hero-description">
            Evaluate the current operating conditions of a machine
            and estimate the likelihood of a failure based on
            operational parameters.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MAIN LAYOUT
# ============================================================

left, right = st.columns(
    [1.35, 0.85],
    gap="large"
)


# ============================================================
# LEFT — INPUT PARAMETERS
# ============================================================

with left:

    st.markdown(
        """
        <div class="section-header">
            <div class="section-title">
                Operational parameters
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">

            <div class="card-title">
                Machine operating conditions
            </div>

            <div class="card-description">
                Enter the measurements recorded during operation.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        udi = st.number_input(
            "Machine identifier",
            min_value=1,
            max_value=10000,
            value=1,
            step=1
        )

        air_temperature = st.number_input(
            "Air temperature [K]",
            min_value=250.0,
            max_value=350.0,
            value=298.0,
            step=0.1
        )

        process_temperature = st.number_input(
            "Process temperature [K]",
            min_value=250.0,
            max_value=400.0,
            value=308.0,
            step=0.1
        )

    with col2:

        rotational_speed = st.number_input(
            "Rotational speed [rpm]",
            min_value=0.0,
            max_value=5000.0,
            value=1500.0,
            step=10.0
        )

        torque = st.number_input(
            "Torque [Nm]",
            min_value=0.0,
            max_value=150.0,
            value=40.0,
            step=0.5
        )

        tool_wear = st.number_input(
            "Tool wear [min]",
            min_value=0.0,
            max_value=300.0,
            value=100.0,
            step=1.0
        )

    st.markdown("<br>", unsafe_allow_html=True)

    analyse = st.button(
        "Assess machine condition"
    )


# ============================================================
# RIGHT — CONTEXT
# ============================================================

with right:

    st.markdown(
        """
        <div class="section-header">
            <div class="section-title">
                Assessment scope
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">

            <div class="card-title">
                Parameters considered
            </div>

            <div class="card-description">
                The assessment is based on the operational
                characteristics supplied by the user.
            </div>

            <div style="
                border-top:1px solid #EAECF0;
                padding-top:1rem;
            ">

                <div style="
                    padding:0.55rem 0;
                    color:#475467;
                    font-size:0.84rem;
                ">
                    Air temperature
                </div>

                <div style="
                    padding:0.55rem 0;
                    color:#475467;
                    font-size:0.84rem;
                ">
                    Process temperature
                </div>

                <div style="
                    padding:0.55rem 0;
                    color:#475467;
                    font-size:0.84rem;
                ">
                    Rotational speed
                </div>

                <div style="
                    padding:0.55rem 0;
                    color:#475467;
                    font-size:0.84rem;
                ">
                    Torque
                </div>

                <div style="
                    padding:0.55rem 0;
                    color:#475467;
                    font-size:0.84rem;
                ">
                    Tool wear
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PREDICTION
# ============================================================

if analyse:

    if not model_loaded:

        st.error(
            "The predictive model could not be loaded. "
            "Please verify that 'modelo.pkl' is available."
        )

    else:

        # ----------------------------------------------------
        # INPUT DATA
        # ----------------------------------------------------

        data = pd.DataFrame(
            [{
                "UDI": udi,
                "Air temperature [K]": air_temperature,
                "Process temperature [K]": process_temperature,
                "Rotational speed [rpm]": rotational_speed,
                "Torque [Nm]": torque,
                "Tool wear [min]": tool_wear
            }]
        )


        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(data)[0]


        probability = None

        if hasattr(model, "predict_proba"):

            probability = model.predict_proba(data)[0][1]


        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-header">
                <div class="section-title">
                    Assessment result
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        if prediction == 1:

            if probability is not None and probability >= 0.70:

                status_class = "critical"
                status = "HIGH RISK"
                description = (
                    "The current operating conditions indicate "
                    "a high likelihood of machine failure."
                )

            else:

                status_class = "warning"
                status = "ATTENTION"
                description = (
                    "The current operating conditions indicate "
                    "an increased likelihood of machine failure."
                )

        else:

            status_class = "normal"
            status = "NORMAL"
            description = (
                "The current operating conditions do not indicate "
                "a machine failure."
            )


        st.markdown(
            f"""
            <div class="assessment">

                <div class="assessment-label">
                    Current assessment
                </div>

                <div class="assessment-status {status_class}">
                    {status}
                </div>

                <div class="assessment-description">
                    {description}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # PROBABILITY
        # ----------------------------------------------------

        if probability is not None:

            percentage = probability * 100

            st.markdown(
                f"""
                <div class="assessment">

                    <div class="assessment-label">
                        Estimated failure probability
                    </div>

                    <div class="probability-wrapper">

                        <div class="probability-header">

                            <span>
                                Model assessment
                            </span>

                            <span class="probability-value">
                                {percentage:.1f}%
                            </span>

                        </div>

                        <div class="progress-background">

                            <div
                                class="progress-fill"
                                style="width:{percentage}%"
                            ></div>

                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # OPERATING VALUES
        # ----------------------------------------------------

        st.markdown(
            """
            <br>

            <div class="section-header">
                <div class="section-title">
                    Operating values
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        metric1, metric2, metric3 = st.columns(3)

        with metric1:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Air temperature
                    </div>

                    <div class="metric-value">
                        {air_temperature:.1f} K
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with metric2:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Rotational speed
                    </div>

                    <div class="metric-value">
                        {rotational_speed:,.0f} rpm
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with metric3:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Tool wear
                    </div>

                    <div class="metric-value">
                        {tool_wear:.0f} min
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # DATA DETAILS
        # ----------------------------------------------------

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("View assessment data"):

            st.dataframe(
                data,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <div>
            Machine Condition Assessment
        </div>

        <div>
            Predictive Maintenance · Operational Analytics
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

