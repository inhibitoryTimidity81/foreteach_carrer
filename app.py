# import streamlit as st
# import google.generativeai as genai
# from pypdf import PdfReader

# # --- SECURITY CHECK ---
# # We do not paste the key here. We ask Streamlit for it.
# if "GOOGLE_API_KEY" in st.secrets:
#     # Key found in the "safe" box. Configure the AI.
#     genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# else:
#     # Key missing. Stop the app safely.
#     st.error("🚨 Critical Error: API Key missing.")
#     st.info("Configuring this app? Go to Streamlit Cloud -> Advanced Settings -> Secrets and add GOOGLE_API_KEY.")
#     st.stop() # This halts the app so it doesn't crash ugly

# # --- THE BRAIN (SYSTEM PROMPT) ---
# SYSTEM_PROMPT = """
# You are a senior technical career coach at ForeTeach. 
# Analyze the resume provided and generate a detailed career report.
# You MUST output your response in strict Markdown format, using the EXACT headings below.

# **Structure Your Response Exactly Like This:**

# ## 🎯 Career Potential
# * **Career Potential Score:** [Score]/100
# * **Analysis:** Analyze the user's profile strength. List 3-4 potential career paths that match their skills (e.g., SDE, Backend, ML Engineer, Product Analyst) and rate the "Match Level" (High/Medium) for each.

# ## 🎯 Roles to Target
# * **Immediate Opportunities:** List 3 specific roles they should apply for right now (e.g., "SDE-1 at Fintech Startups").
# * **Target Companies:** Recommend 3-4 types of companies (e.g., "Series B Startups," "MAANG," "High-Frequency Trading firms").
# * **Focus Area:** One sentence on what they should look for (e.g., "Companies valuing strong System Design skills").

# ## 📊 Skill Gaps
# * 🔴 **Critical (Must Fix):** List 1-2 major missing skills that will cause immediate rejection (e.g., System Design, specific languages).
# * 🟡 **Important:** List 2 skills to improve for better offers (e.g., Docker, Cloud platforms).
# * 🟢 **Nice to Have:** List 1 skill that would make them stand out (e.g., Open Source contributions).

# ## 💰 Salary Benchmarking
# (Create a Markdown table with these columns: Role, Company Type, Expected CTC)
# | Role | Company Type | Expected CTC (INR) |
# | :--- | :--- | :--- |
# | [Role 1] | [Type 1] | [Amount] |
# | [Role 2] | [Type 2] | [Amount] |

# ## 💡 ForeTeach Recommendation
# * **Your Next Step:** Recommend ONE specific action.
# * **The Fix:** "To master [Critical Gap], take the **ForeTeach [Module Name]**."
# * **Link:** [Unlock Full Roadmap on ForeTeach](https://foreteach.com)
# """

# # --- VISUAL SETUP ---
# st.set_page_config(page_title="ForeTeach CareerGPT", layout="centered")

# st.markdown("""
#     <style>
#     /* 1. Main Page Background */
#     .stApp {
#         background-color: #ffffff;
#         color: #000000;
#     }
    
#     /* 2. File Uploader Styling */
#     [data-testid="stFileUploader"] {
#         background-color: #f0f2f6;
#         border: 1px solid #d6d6d8;
#         padding: 20px;
#         border-radius: 10px;
#     }
#     [data-testid="stFileUploader"] label {
#         color: #000000 !important;
#         font-weight: bold;
#     }

#     /* 3. 'Analyze' Button (Red) */
#     div.stButton > button {
#         background-color: #FF4B4B; 
#         color: white !important;    
#         font-size: 18px;
#         font-weight: bold;
#         border: none;
#         border-radius: 8px;
#         padding: 10px 20px;
#         width: 100%;
#     }
#     div.stButton > button:hover {
#         background-color: #FF2B2B;
#         color: white !important;
#     }

#     /* 4. 'Unlock Roadmap' Button (Green) */
#     a[href^="http"] {
#         text-decoration: none;
#     }
#     div.stLinkButton > a {
#         background-color: #00C853; 
#         color: white !important;
#         font-size: 20px;
#         font-weight: bold;
#         border: none;
#         border-radius: 8px;
#         text-align: center;
#         box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
#         width: 100%;
#         display: block;
#     }
#     div.stLinkButton > a:hover {
#         background-color: #009624;
#         color: white !important;
#     }

#     /* 5. Text Visibility Fixes */
#     h1, h2, h3, p, li, td, th {
#         color: #000000 !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # --- APP LOGIC ---
# st.title("ForeTeach Career Scorer 🚀")
# st.write("Upload your resume to generate your **Personalized Career Strategy**.")

# uploaded_file = st.file_uploader("Drop your Resume here (PDF)...", type=['pdf'])
# resume_text = ""

# if uploaded_file is not None:
#     try:
#         reader = PdfReader(uploaded_file)
#         for page in reader.pages:
#             resume_text += page.extract_text()
#         st.success("✅ Resume Loaded! Click Analyze below.")
#     except Exception as e:
#         st.error(f"Error reading PDF: {e}")

# if st.button("Analyze My Career Strategy"):
#     if resume_text:
#         with st.spinner("Analyzing skill gaps & calculating market salary..."):
#             try:
#                 # Use the stable model for production safety
#                 model = genai.GenerativeModel('gemini-3-flash-preview')
                
#                 response = model.generate_content(SYSTEM_PROMPT + "\n\nRESUME TEXT:\n" + resume_text)
                
#                 st.markdown("---")
#                 st.markdown(response.text)
                
#                 st.markdown("---")
#                 st.link_button("🔓 Unlock Full Roadmap & Referrals (ForeTeach Premium)", "https://foreteach.com")
                
#             except Exception as e:
#                 st.error(f"Error connecting to AI: {e}")
#     else:
#         st.warning("⚠️ Please upload a PDF first!")


import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- SECURITY CHECK ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key.")
    st.stop()

# --- SYSTEM PROMPT (Same as before) ---
SYSTEM_PROMPT = """
You are a career coach. Analyze the resume.
Output strictly in Markdown:
## 🎯 Career Potential
* **Score:** [Score]/100
* **Analysis:** [Analysis]
## 🎯 Roles to Target
* **Roles:** [Roles]
## 📊 Skill Gaps
* 🔴 **Critical:** [Gap]
* 🟡 **Important:** [Gap]
## 💰 Salary Benchmarking
(Table of Roles vs Salary)
## 💡 Recommendation
* **Next Step:** [Action]
"""

# --- VISUAL SETUP ---
st.set_page_config(page_title="ForeTeach CareerGPT", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #000000; }
    [data-testid="stFileUploader"] { background-color: #f0f2f6; border-radius: 10px; padding: 20px; }
    div.stButton > button { background-color: #FF4B4B; color: white !important; width: 100%; }
    div.stLinkButton > a { background-color: #00C853; color: white !important; width: 100%; display: block; }
    h1, h2, h3, p, label { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIC ---
st.title("ForeTeach Career Scorer 🚀")
st.write("Unlock your personalized career strategy.")

# --- DATA COLLECTION FORM ---
with st.container():
    st.subheader("📋 Your Details")
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("First Name")
    with col2:
        user_email = st.text_input("Email Address (Required)")
    
    target_role = st.selectbox(
        "Which role are you targeting?",
        ["Software Engineer (SDE)", "Data Scientist", "Product Manager", "Analyst", "Core Engineering", "Other"]
    )
    
    grad_year = st.selectbox("Graduation Year", ["2024", "2025", "2026", "2027"])

st.markdown("---")

# --- RESUME UPLOAD ---
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
resume_text = ""

if uploaded_file:
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text()
        st.success("✅ Resume Loaded!")
    except:
        st.error("Error reading PDF.")

# --- ANALYZE BUTTON ---
if st.button("Analyze My Strategy"):
    # 1. Validation: Block them if no email
    if not user_email:
        st.warning("⚠️ Please enter your Email Address above to see your results.")
    elif not resume_text:
        st.warning("⚠️ Please upload your resume.")
    else:
        # 2. LOG THE DATA (For the Hackathon Demo)
        # In a real startup, we would send this to a database. 
        # For now, we print it to the console logs so you can see it.
        print(f"NEW LEAD: {user_name} | {user_email} | Role: {target_role} | Year: {grad_year}")
        
        with st.spinner("Generating Report..."):
            try:
                model = genai.GenerativeModel('gemini-3-flash-preview')
                # Inject user context into the prompt
                full_prompt = f"{SYSTEM_PROMPT}\n\nUSER CONTEXT: Target Role: {target_role}, Grad Year: {grad_year}\n\nRESUME TEXT:\n{resume_text}"
                
                response = model.generate_content(full_prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                st.link_button("🔓 Unlock Full Roadmap (ForeTeach Premium)", "https://foreteach.com")
            except Exception as e:
                st.error(f"Error: {e}")
