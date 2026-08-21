import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

from password_strength_model import assess_password


# ============================================================
# LIVE PASSWORD COMPONENT
# ============================================================

FRONTEND_DIR = Path(__file__).parent / "live_password_frontend"

password_input_component = components.declare_component(
    "live_password",
    path=str(FRONTEND_DIR)
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Instant Password Strength & Security Assessment",
    page_icon="🔐",
    layout="centered"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "🔐 Instant Password Strength & Security Assessment"
)

st.write(
    "Evaluate your password in real time and discover its "
    "strength, predictability risk, and crack difficulty."
)


# ============================================================
# ONE PASSWORD INPUT
# ============================================================

st.markdown("**Password**")

password = password_input_component(
    label="Password",
    key="main_password"
)


# ============================================================
# ONLY RUN ASSESSMENT WHEN PASSWORD EXISTS
# ============================================================

if password:

    result = assess_password(password)


    # ========================================================
    # NORMALIZE TRADITIONAL STRENGTH
    # ========================================================

    model_strength = str(
        result["traditional_strength"]
    ).strip().lower()


    if model_strength == "strong":

        strength = "Strong"

    elif model_strength in ["medium", "moderate"]:

        strength = "Moderate"

    else:

        strength = "Weak"


    # ========================================================
    # TRADITIONAL PASSWORD STRENGTH
    # ========================================================

    st.markdown(
        "**Traditional Password Strength**"
    )


    if strength == "Weak":

        st.progress(33)

        st.markdown(
            "<span style='color:#d32f2f;"
            "font-size:18px;"
            "font-weight:bold;'>"
            "WEAK"
            "</span>",
            unsafe_allow_html=True
        )


    elif strength == "Moderate":

        st.progress(66)

        st.markdown(
            "<span style='color:#f39c12;"
            "font-size:18px;"
            "font-weight:bold;'>"
            "MODERATE"
            "</span>",
            unsafe_allow_html=True
        )


    else:

        st.progress(100)

        st.markdown(
            "<span style='color:#188038;"
            "font-size:18px;"
            "font-weight:bold;'>"
            "STRONG"
            "</span>",
            unsafe_allow_html=True
        )


    # ========================================================
    # CRACK DIFFICULTY
    # ========================================================

    crack_class = str(
        result["crack_class"]
    ).strip()


    if crack_class.lower() == "easy":

        crack_icon = "🟢"

    elif crack_class.lower() == "difficult":

        crack_icon = "🔴"

    else:

        crack_icon = "🟡"


    st.markdown(
        f"**{crack_icon} Crack Difficulty:** "
        f"{crack_class.upper()}"
    )


    # ========================================================
    # FALSE CONFIDENCE
    #
    # Strong traditionally + Easy to crack
    # = False-confidence case
    # ========================================================

    false_confidence = (
        strength == "Strong"
        and crack_class.lower() in ["easy", "moderate"]
    )


    if false_confidence:

        false_icon = "⚠️"
        false_result = "YES"

    else:

        false_icon = "🟢"
        false_result = "NO"


    st.markdown(
        f"**{false_icon} False Confidence:** "
        f"{false_result}"
    )


    # ========================================================
    # PASSWORD ANALYSIS DETAILS
    # ========================================================

    with st.expander(
        "🔍 Password Analysis Details"
    ):

        # ----------------------------------------------------
        # PASSWORD CHARACTERISTICS
        # ----------------------------------------------------

        st.subheader(
            "Password Characteristics"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Length",
                result["length"]
            )

            st.metric(
                "Character Diversity",
                result["character_diversity"]
            )

            st.metric(
                "Character Pool Size",
                result["character_pool_size"]
            )


        with col2:

            st.metric(
                "Entropy",
                f'{result["entropy"]:.4f} bits'
            )

            # IMPORTANT:
            # This MUST be the exact same strength
            # displayed above.

            st.metric(
                "Traditional Strength",
                strength
            )


        # ----------------------------------------------------
        # PREDICTABILITY INDICATORS
        # ----------------------------------------------------

        st.subheader(
            "Predictability Indicators"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                "**Dictionary Word:**",
                "Detected"
                if result["dictionary_word"]
                else "Not Detected"
            )

            st.write(
                "**Common Year:**",
                "Detected"
                if result["common_year"]
                else "Not Detected"
            )

            st.write(
                "**Sequential Pattern:**",
                "Detected"
                if result["sequential_pattern"]
                else "Not Detected"
            )


        with col2:

            st.write(
                "**Repeated Character:**",
                "Detected"
                if result["repeated_character"]
                else "Not Detected"
            )

            st.write(
                "**Predictable Structure:**",
                "Detected"
                if result["predictable_structure"]
                else "Not Detected"
            )


        # ----------------------------------------------------
        # CDR ASSESSMENT
        # ----------------------------------------------------

        st.subheader(
            "CDR Assessment"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "CDR Score",
                f'{result["cdr_score"]:.6f}'
            )


        with col2:

            st.metric(
                "Predictability Risk",
                result["cdr_class"]
            )


        # ----------------------------------------------------
        # CRACK DIFFICULTY ASSESSMENT
        # ----------------------------------------------------

        st.subheader(
            "Crack-Difficulty Assessment"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Crack-Difficulty Score",
                result["crack_score"]
            )


        with col2:

            st.metric(
                "Crack-Difficulty Class",
                result["crack_class"]
            )


        # ----------------------------------------------------
        # FALSE-CONFIDENCE ASSESSMENT
        # ----------------------------------------------------

        st.subheader(
            "False-Confidence Assessment"
        )


        if false_confidence:

            st.success(
                "False-Confidence Case Detected"
            )

        else:

            st.write(
                "No False-Confidence Case Detected"
            )