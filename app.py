import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- CONFIGURATION ---
# Replace with your actual key!
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE" 

genai.configure(api_key="AIzaSyA_AgjydL30QYRoMbmKuKPPkjIwnUJORNQ")

# --- THE BRAIN (SYSTEM PROMPT) ---
SYSTEM_PROMPT = """
You are CareerGPT, a strict senior recruiter for ForeTeach.
Analyze the resume provided.
Output ONLY this structure in Markdown:

## 🎯 Career Readiness Score: [Score]/100
(Be strict. Give a specific reason for the score.)

## 💰 Salary Reality Check
* **Estimated Market Value:** ₹[Low] - ₹[High] LPA
* **Gap:** You are missing [Critical Skill] which is worth ₹2 LPA extra.

## 🚀 The ForeTeach Fix
* ❌ Weakness: [Weak Skill]
* ✅ **Solution:** [Specific Action/Course]
* **Call to Action:** "Unlock your detailed roadmap on ForeTeach Premium."
"""

# --- VISUAL SETUP ---
st.set_page_config(page_title="ForeTeach CareerGPT", layout="centered")

# CSS to make the UI pop and fix the button colors
st.markdown("""
    <style>
    /* 1. Force background to white and normal text to black */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* 2. Fix the File Uploader to be visible */
    [data-testid="stFileUploader"] {
        background-color: #f0f2f6;
        border: 1px solid #d6d6d8;
        padding: 20px;
        border-radius: 10px;
    }
    [data-testid="stFileUploader"] label {
        color: #000000 !important;
        font-weight: bold;
    }

    /* 3. Style the 'Analyze' Button (Red) */
    div.stButton > button {
        background-color: #FF4B4B; /* ForeTeach Red */
        color: white !important;    /* Force text white */
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
    }
    div.stButton > button:hover {
        background-color: #FF2B2B;
        color: white !important;
    }

    /* 4. Style the 'Unlock Roadmap' Button (Green/Gold) */
    a[href^="http"] {
        text-decoration: none;
    }
    /* Target the link button wrapper */
    div.stLinkButton > a {
        background-color: #00C853; /* Success Green */
        color: white !important;
        font-size: 20px;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    div.stLinkButton > a:hover {
        background-color: #009624;
        color: white !important;
    }

    /* 5. Ensure headings and normal text remain black */
    h1, h2, h3, p, li {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIC ---
st.title("ForeTeach Career Scorer 🚀")
st.write("Upload your resume (PDF) to check your true Market Value.")

# 1. The Upload Button
uploaded_file = st.file_uploader("Drop your Resume here...", type=['pdf'])

# 2. Variable to hold text
resume_text = ""

# 3. Process the file if uploaded
if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text()
        st.success("✅ Resume Loaded! Click Analyze below.")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")

# 4. The Analyze Button
if st.button("Analyze My Career"):
    if resume_text:
        with st.spinner("Analyzing your market value..."):
            try:
                # model = genai.GenerativeModel('gemini-pro')
                # model = genai.GenerativeModel('gemini-1.5-flash')
                # model = genai.GenerativeModel('gemini-1.0-pro')
                model = genai.GenerativeModel('gemini-3-flash-preview')
                response = model.generate_content(SYSTEM_PROMPT + "\n\nRESUME TEXT:\n" + resume_text)
                
                # Show Result
                st.markdown("---")
                st.markdown(response.text)
                
                # The "Trap" Link (Opens in new tab)
                st.link_button("🔓 Unlock Full Roadmap (ForeTeach Premium)", "https://foreteach.com")
                
            except Exception as e:
                st.error(f"Error connecting to AI: {e}")
    else:
        st.warning("⚠️ Please upload a PDF first!")