
import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import requests

# --- CONFIGURATION ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# --- GOOGLE FORM CONFIGURATION ---
# Correct URL ending in /formResponse
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScAXrlLHuNrSsReWAcp9Qn6eP__NYyecswY9evWyY4HT_EqRw/formResponse"

# 🚨 CORRECTED IDs FROM YOUR LINK
ENTRY_MAPPING = {
    "Name": "entry.2050712578",
    "Email": "entry.1060699408",      # ✅ FIXED (Was missing '08')
    "Whatsapp": "entry.753036163",
    "College": "entry.1025328017",
    "Branch": "entry.393812671",
    "Current_Role": "entry.301448048",
    "Target_Role": "entry.522155613",
    "Role_Others": "entry.90157928",
    "Confidence": "entry.1985230001",
    "Internship": "entry.950348418",
    "Pain_Point": "entry.1499744374",
    "Pain_Explain": "entry.289520657"
}

def save_to_google_sheet(data_dict):
    try:
        form_data = {ENTRY_MAPPING[key]: value for key, value in data_dict.items()}
        requests.post(FORM_URL, data=form_data)
        return True
    except:
        return False

# --- UI SETUP ---
st.set_page_config(page_title="ForeTeach Career Scorer", layout="centered")

# 🔴 FINAL CSS FIX
st.markdown("""
    <style>
    /* 1. FORCE APP BACKGROUND TO WHITE */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }

    /* 2. TARGET ALL INPUT TEXT */
    input, textarea {
        background-color: white !important;
        color: #000000 !important;
        caret-color: #FF4B4B !important;
        border: 1px solid #d3d3d3 !important;
        padding: 10px !important;
        border-radius: 8px !important;
    }

    /* 3. TARGET DROPDOWN DISPLAY */
    div[data-baseweb="select"] > div {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
        border: 1px solid #d3d3d3 !important;
        border-radius: 8px !important;
    }
    
    /* 4. TARGET DROPDOWN MENU ITEMS */
    div[role="listbox"] li, div[role="option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* 5. FOCUS STATE */
    input:focus, textarea:focus, div[data-baseweb="select"] > div:focus-within {
        border: 2px solid #FF4B4B !important;
        box-shadow: 0px 4px 10px rgba(255, 75, 75, 0.1) !important;
    }

    /* 6. LABELS */
    label, p, h1, h2, h3 {
        color: #000000 !important;
    }
    
    /* 7. BUTTON STYLING */
    div.stButton > button {
        background-color: #FF4B4B;
        color: white !important;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("ForeTeach Career Scorer")
st.write("Complete your profile to unlock your AI Resume Analysis.")

# --- THE FORM ---
with st.container():
    st.subheader("👤 Personal Details")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Rahul Kumar")
        whatsapp = st.text_input("WhatsApp Number", placeholder="e.g. 9876543210")
        college = st.text_input("Graduation College", placeholder="e.g. IIT Roorkee")
    with col2:
        email = st.text_input("Email Address (Required)", placeholder="email@example.com")
        branch = st.text_input("Graduation Branch", placeholder="e.g. ME")
        # UPDATED: Added "Not Graduate Yet" to match your form data
        current_role = st.selectbox("Current Role (Dropdown)", ["SDE", "Data Scientist", "Product Manager", "Analyst", "Consultancy", "Core Engineering", "Others", "Not Graduate Yet"])

    st.markdown("---")
    st.subheader("🎯 Career Goals")
    
    target_role = st.selectbox("Target Role (Dropdown)", ["SDE", "Data Scientist", "Product Manager", "Analyst", "Core Engineering", "Other"])
    
    role_others = "NA"
    if target_role == "Other":
        role_others = st.text_input("Please specify your Target Role")

    st.markdown("---")
    st.subheader("🧠 Skills & Struggles")
    
    col3, col4 = st.columns(2)
    with col3:
        confidence = st.slider("How confident are you? (1-5)", 1, 5, 4)
    with col4:
        internship = st.radio("Have you done an internship? (Select One)", ["Yes", "No"], horizontal=True)
    
    # UPDATED: Matches your Form's "Online Assessments (OA)" exactly
    pain_point = st.selectbox(
        "Primary Pain Point (Dropdown)",
        ["Resume Shortlisting", "Online Assessments (OA)", "Interviews", "Guidance / Roadmap", "Others"]
    )
    
    pain_explain = st.text_area("Please Explain your pain point (Optional)")

st.markdown("---")

# --- RESUME UPLOAD ---
st.subheader("📄 Upload Resume")
uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])

# --- ANALYZE LOGIC ---
if st.button("Analyze My Strategy"):
    if not email or not uploaded_file:
        st.warning("⚠️ Please provide at least your Email and Resume.")
    else:
        # 1. PREPARE DATA PACKAGE
        user_data = {
            "Name": name, "Email": email, "Whatsapp": whatsapp,
            "College": college, "Branch": branch, "Current_Role": current_role,
            "Target_Role": target_role, "Role_Others": role_others,
            "Confidence": confidence, "Internship": internship,
            "Pain_Point": pain_point, "Pain_Explain": pain_explain
        }
        
        # 2. SAVE TO GOOGLE SHEET
        with st.spinner("Saving profile..."):
            success = save_to_google_sheet(user_data)
            if success:
                st.success("✅ Profile Saved!")
            else:
                st.error("⚠️ Could not save data, but proceeding with AI analysis.")
        
        # 3. RUN AI ANALYSIS
        with st.spinner("AI is analyzing your profile..."):
            try:
                reader = PdfReader(uploaded_file)
                resume_text = ""
                for page in reader.pages:
                    resume_text += page.extract_text()
                
                system_prompt = f"""
                You are a Senior Career Auditor at ForeTeach. Your job is to strictly evaluate this student's resume for the role of {target_role}.
                
                **USER PROFILE:**
                - College: {college}
                - Confidence Level: {confidence}/5 (If low, they need mentorship)
                - Biggest Pain Point: {pain_point} ({pain_explain})
                
                **YOUR INSTRUCTIONS:**
                1. **Score:** Give a strict "Market Readiness Score" out of 100. Be realistic.
                2. **The Gap:** Identify 3 specific weaknesses in their resume or skills that will cause rejection.
                3. **The ForeTeach Solution:** For EVERY weakness, you MUST recommend a specific "ForeTeach Solution" to fix it.
                   - If their resume is weak -> Recommend "ForeTeach Resume Sprint".
                   - If they lack DSA/Projects -> Recommend "ForeTeach Capstone Project Cohort".
                   - If they struggle with OA/Confidence -> Recommend "ForeTeach 1:1 Mentorship".
                
                **OUTPUT FORMAT (Strict Markdown):**
                
                ## 🎯 Market Readiness Score: [Score]/100
                
                ## 🚩 Critical Rejection Risks
                (List 3 major flaws. Be direct. E.g., "Your project descriptions are too vague for an SDE role.")
                
                ## 💡 How ForeTeach Fixes This
                | Your Weakness | The ForeTeach Fix |
                | :--- | :--- |
                | [Weakness 1] | **ForeTeach Project Cohort** (Build industry-grade projects) |
                | [Weakness 2] | **ForeTeach Resume Review** (Get shortlisted) |
                | [Weakness 3] | **ForeTeach Mock Interviews** (Beat the anxiety) |
                
                ## 🚀 Your Personal Roadmap
                (Give a 4-week plan. End with: "We can help you execute this faster.")
                """
                
                # Corrected Model Name
                model = genai.GenerativeModel('gemini-3-flash-preview')
                response = model.generate_content(system_prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                st.link_button("🔓 Unlock Full Roadmap", "https://foreteach.com")
                
            except Exception as e:
                st.error(f"Error: {e}")