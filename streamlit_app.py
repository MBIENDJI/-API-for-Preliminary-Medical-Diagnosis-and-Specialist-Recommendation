import streamlit as st
import requests
import base64

# ===========================================================================
# CONFIG
# ===========================================================================

API_BASE = "http://127.0.0.1:8000/api"

st.set_page_config(
    page_title="MediAssist — Health Diagnosis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ===========================================================================
# SYMPTOM GLOSSARY
# ===========================================================================

ALL_SYMPTOMS = sorted([
    "abdominal_pain", "abnormal_menstruation", "acidity", "acute_liver_failure",
    "altered_sensorium", "anxiety", "back_pain", "belly_pain", "blackheads",
    "bladder_discomfort", "blister", "blood_in_sputum", "bloody_stool",
    "blurred_and_distorted_vision", "breathlessness", "brittle_nails", "bruising",
    "burning_micturition", "chest_pain", "chills", "cold_hands_and_feets", "coma",
    "congestion", "constipation", "continuous_feel_of_urine", "continuous_sneezing",
    "cough", "cramps", "dark_urine", "dehydration", "depression", "diarrhoea",
    "dizziness", "drying_and_tingling_lips", "enlarged_thyroid", "excessive_hunger",
    "extra_marital_contacts", "family_history", "fast_heart_rate", "fatigue",
    "fluid_overload", "headache", "high_fever", "hip_joint_pain",
    "history_of_alcohol_consumption", "increased_appetite", "indigestion",
    "inflammatory_nails", "internal_itching", "irregular_sugar_level",
    "irritability", "irritation_in_anus", "joint_pain", "knee_pain",
    "lack_of_concentration", "lethargy", "loss_of_appetite", "loss_of_balance",
    "loss_of_smell", "malaise", "mild_fever", "mood_swings", "movement_stiffness",
    "mucoid_sputum", "muscle_pain", "muscle_wasting", "muscle_weakness", "nausea",
    "neck_pain", "nodal_skin_eruptions", "obesity", "pain_behind_the_eyes",
    "pain_during_bowel_movements", "pain_in_anal_region", "painful_walking",
    "palpitations", "passage_of_gases", "patches_in_throat", "phlegm", "polyuria",
    "prominent_veins_on_calf", "puffy_face_and_eyes", "pus_filled_pimples",
    "receiving_blood_transfusion", "receiving_unsterile_injections",
    "red_sore_around_nose", "red_spots_over_body", "redness_of_eyes", "restlessness",
    "runny_nose", "rusty_sputum", "scurring", "shivering", "silver_like_dusting",
    "sinus_pressure", "skin_peeling", "skin_rash", "slurred_speech",
    "small_dents_in_nails", "spinning_movements", "stiff_neck", "stomach_bleeding",
    "stomach_pain", "sunken_eyes", "sweating", "swelled_lymph_nodes",
    "swelling_joints", "swelling_of_stomach", "swollen_blood_vessels",
    "swollen_extremeties", "swollen_legs", "throat_irritation", "ulcers_on_tongue",
    "unsteadiness", "visual_disturbances", "vomiting", "watering_from_eyes",
    "weakness_in_limbs", "weakness_of_one_body_side", "weight_gain", "weight_loss",
    "yellow_crust_ooze", "yellow_urine", "yellowing_of_eyes", "yellowish_skin", "itching",
])

# ===========================================================================
# SESSION STATE
# ===========================================================================

defaults = {
    "token": None,
    "patient_id": None,
    "diagnosis_id": None,
    "step": "welcome",
    "selected_symptoms": [],
    "diagnosis_result": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ===========================================================================
# HELPERS
# ===========================================================================

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

def api_post(endpoint, payload):
    try:
        r = requests.post(f"{API_BASE}{endpoint}", json=payload, headers=auth_headers(), timeout=10)
        return r.status_code, r.json()
    except Exception as e:
        return 500, {"error": str(e)}

def search_symptoms(query):
    if not query:
        return []
    return [s for s in ALL_SYMPTOMS if query.lower().strip() in s]

def load_image_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

# ===========================================================================
# STYLES
# ===========================================================================

def apply_welcome_style(logo_html=""):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;600&display=swap');
    .stApp {{
        background-color: #c8c8c8;
        font-family: 'Lato', sans-serif;
    }}
    .welcome-wrap {{
        max-width: 440px;
        margin: 40px auto 0;
        background: white;
        border-radius: 22px;
        padding: 36px 44px 28px;
        box-shadow: 0 10px 50px rgba(0,0,0,0.14);
        text-align: center;
    }}
    .welcome-title {{
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #1a1a2e;
        margin-bottom: 4px;
    }}
    .welcome-sub {{
        color: #999;
        font-size: 0.9rem;
        margin-bottom: 8px;
        font-weight: 300;
    }}
    .stTextInput > div > input {{
        border-radius: 8px !important;
        border: 1.5px solid #e0e0e0 !important;
        padding: 10px 14px !important;
    }}
    .stButton > button {{
        background: #c0392b !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 10px !important;
        margin-top: 6px !important;
    }}
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    <div class="welcome-wrap">
        {logo_html}
        <div class="welcome-title">MediAssist</div>
        <div class="welcome-sub">Preliminary Health Diagnosis System</div>
    </div>
    """, unsafe_allow_html=True)


def apply_inner_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;600&display=swap');
    .stApp {
        background-color: #FFB6C1;
        font-family: 'Lato', sans-serif;
    }
    .page-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.7rem;
        color: #1a1a2e;
        margin-bottom: 2px;
    }
    .card {
        background: rgba(255,255,255,0.65);
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 16px;
        backdrop-filter: blur(6px);
    }
    .stButton > button {
        background: #c0392b !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background: #a93226 !important;
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# ===========================================================================
# STEP 1 — WELCOME / LOGIN
# ===========================================================================

if st.session_state.step == "welcome":

    img_b64 = load_image_b64(r"C:\test_latex\zzz\v7.png")
    logo_html = ""
    if img_b64:
        logo_html = f'<img src="data:image/png;base64,{img_b64}" style="width:80px;margin-bottom:16px;border-radius:50%;box-shadow:0 4px 20px rgba(0,0,0,0.15);">'

    apply_welcome_style(logo_html)

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="your username")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        if st.button("Sign In →"):
            if not username or not password:
                st.error("Please fill in both fields.")
            else:
                try:
                    r = requests.post(
                        f"{API_BASE}/auth/token/",
                        json={"username": username, "password": password},
                        timeout=8,
                    )
                    if r.status_code == 200:
                        st.session_state.token = r.json()["access"]
                        st.session_state.step = "register"
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials.")
                except Exception as e:
                    st.error(f"Cannot reach API: {e}")

        st.markdown(
            "<p style='text-align:center;color:#aaa;font-size:0.8rem;margin-top:14px;'>"
            "Not a substitute for professional medical advice.</p>",
            unsafe_allow_html=True,
        )


# ===========================================================================
# STEP 2 — PATIENT REGISTRATION
# ===========================================================================

elif st.session_state.step == "register":
    apply_inner_style()

    st.markdown('<div class="page-title">👤 Patient Registration</div>', unsafe_allow_html=True)
    st.caption("All personal data is encrypted with Fernet before storage.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Personal Information**")
        name  = st.text_input("Full Name *")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        age   = st.number_input("Age", 0, 120, 30)
        sex   = st.selectbox("Sex", ["Male", "Female", "Other"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Medical History**")
        medical_history = st.text_area(
            "Previous conditions, allergies, medications...",
            height=180,
            placeholder="e.g. Hypertension since 2018, penicillin allergy",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Register & Continue →", type="primary"):
        if not name:
            st.error("Full name is required.")
        else:
            payload = {
                "name": name, "email": email or None, "phone": phone or None,
                "age": age, "sex": sex, "medical_history": medical_history or None,
                "symptom_names": [],
            }
            code, resp = api_post("/patients/", payload)
            if code == 201:
                st.session_state.patient_id = resp["patient_id"]
                st.session_state.step = "symptom_search"
                st.rerun()
            else:
                st.error(f"Registration failed: {resp}")


# ===========================================================================
# STEP 3 — SYMPTOM GLOSSARY SEARCH (unlimited)
# ===========================================================================

elif st.session_state.step == "symptom_search":
    apply_inner_style()

    st.markdown('<div class="page-title">🔍 Hospital Symptom Glossary</div>', unsafe_allow_html=True)
    st.caption("Type the beginning of a symptom — the system completes it for you. Add as many as you need.")
    st.markdown("---")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Search Symptom**")
        query = st.text_input("Start typing a symptom", placeholder="e.g.  cou  →  cough")
        results = search_symptoms(query)

        if query:
            if results:
                st.caption(f"📋 {len(results)} result(s) — click to add:")
                for s in results[:12]:
                    if st.button(f"➕  {s}", key=f"btn_{s}"):
                        if s not in st.session_state.selected_symptoms:
                            st.session_state.selected_symptoms.append(s)
                        st.rerun()
            else:
                st.caption("No match. Try another spelling.")
        else:
            st.caption("Glossary contains 131 medical symptoms.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"**Selected Symptoms ({len(st.session_state.selected_symptoms)})**")

        if st.session_state.selected_symptoms:
            for s in list(st.session_state.selected_symptoms):
                c1, c2 = st.columns([6, 1])
                with c1:
                    st.markdown(f"✅ `{s}`")
                with c2:
                    if st.button("✕", key=f"del_{s}"):
                        st.session_state.selected_symptoms.remove(s)
                        st.rerun()
            st.markdown("---")
            if st.button("🗑️ Clear all"):
                st.session_state.selected_symptoms = []
                st.rerun()
        else:
            st.info("No symptoms added yet. Search and click ➕ to add.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        if st.session_state.selected_symptoms:
            st.success(f"**{len(st.session_state.selected_symptoms)} symptom(s) selected.** Ready to confirm.")
    with col_b:
        if st.button("Confirm & Continue →", type="primary",
                     disabled=len(st.session_state.selected_symptoms) == 0):
            st.session_state.step = "symptom_count"
            st.rerun()


# ===========================================================================
# STEP 4 — HOW MANY SYMPTOMS + FINAL PICK
# ===========================================================================

elif st.session_state.step == "symptom_count":
    apply_inner_style()

    st.markdown('<div class="page-title">📋 Confirm Symptoms for Analysis</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    total = len(st.session_state.selected_symptoms)
    n = st.number_input(
        f"How many symptoms do you want to submit? (you selected {total})",
        min_value=1,
        max_value=total,
        value=total,
    )

    st.markdown(f"**Select exactly {int(n)} symptom(s):**")
    final_symptoms = st.multiselect(
        "Choose from your list",
        options=st.session_state.selected_symptoms,
        default=st.session_state.selected_symptoms[:int(n)],
        max_selections=int(n),
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to search"):
            st.session_state.step = "symptom_search"
            st.rerun()
    with col2:
        if st.button("🔬 Analyse Symptoms", type="primary",
                     disabled=len(final_symptoms) == 0):
            payload = {"patient_id": st.session_state.patient_id, "symptoms": final_symptoms}
            code, resp = api_post("/diagnoses/preliminary/", payload)
            if code == 201:
                st.session_state.diagnosis_id = resp["diagnosis_id"]
                st.session_state.diagnosis_result = resp
                st.session_state.step = "results"
                st.rerun()
            else:
                st.error(f"Error: {resp}")


# ===========================================================================
# STEP 5 — RESULTS
# ===========================================================================

elif st.session_state.step == "results":
    apply_inner_style()

    resp = st.session_state.diagnosis_result
    st.markdown('<div class="page-title">🩺 Diagnosis Results</div>', unsafe_allow_html=True)
    st.caption(f"Diagnosis ID: {st.session_state.diagnosis_id} | Patient ID: {st.session_state.patient_id}")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🦠 Possible Conditions")
        for d in resp.get("preliminary_diagnoses", []):
            pct = round(d["confidence"] * 100, 1)
            st.metric(label=d["disease"], value=f"{pct}%", delta="confidence score")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 👨‍⚕️ Recommended Specialists")
        icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        for s in resp.get("specialists", []):
            icon = icons.get(s["priority"], "⚪")
            confidence = round((s.get("confidence") or 0) * 100, 1)
            st.markdown(f"{icon} **{s['detail']}**")
            st.caption(f"Priority: {s['priority']}  |  Confidence: {confidence}%")
        st.markdown('</div>', unsafe_allow_html=True)

    st.warning(f"⚠️ {resp.get('disclaimer', '')}")
    st.markdown("---")

    if st.button("📊 Continue to Risk Assessment →", type="primary"):
        st.session_state.step = "risk"
        st.rerun()


# ===========================================================================
# STEP 6 — RISK ASSESSMENT
# ===========================================================================

elif st.session_state.step == "risk":
    apply_inner_style()

    st.markdown('<div class="page-title">📊 Risk Assessment</div>', unsafe_allow_html=True)
    st.caption("Biometric data is encrypted before storage.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Enter Biometric Data**")
        bmi            = st.number_input("BMI", 10.0, 80.0, 25.0, step=0.1)
        age            = st.number_input("Age", 0, 120, 35)
        blood_pressure = st.selectbox("Blood Pressure", ["normal", "low", "elevated", "high"])
        family_history = st.checkbox("Family history of diabetes / hypertension")
        sex            = st.selectbox("Sex", ["Male", "Female", "Other"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**BMI Reference**")
        st.markdown("""
| BMI | Category |
|-----|----------|
| < 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25 – 29.9 | Overweight |
| ≥ 30 | Obese |
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Evaluate Risk 📊", type="primary"):
        payload = {
            "bmi": bmi, "age": age,
            "blood_pressure": blood_pressure,
            "family_history": family_history,
            "sex": sex,
        }
        code, resp = api_post(f"/patients/{st.session_state.patient_id}/risk-assessment/", payload)
        if code == 200:
            st.success("✅ Assessment complete!")
            st.markdown("---")
            col1, col2 = st.columns(2)
            risk_icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("**Risk Levels**")
                for condition, level in resp["risk_factors"].items():
                    icon = risk_icons.get(level, "⚪")
                    st.metric(condition.capitalize(), f"{icon} {level}")
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("**Recommendations**")
                st.info(resp["recommendations"])
                st.markdown('</div>', unsafe_allow_html=True)
            st.warning(f"⚠️ {resp['disclaimer']}")
        else:
            st.error(f"Error: {resp}")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Patient"):
            for k in ["patient_id", "diagnosis_id", "diagnosis_result"]:
                st.session_state[k] = None
            st.session_state.selected_symptoms = []
            st.session_state.step = "register"
            st.rerun()
    with col2:
        if st.button("🚪 Logout"):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()
