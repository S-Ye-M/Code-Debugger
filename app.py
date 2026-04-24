
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=my_api_key)

st.set_page_config(
    page_title="AI Code Debugger",
    page_icon="🔬",
    layout="centered",
)

# ── Header ─────────────────────────────────────────────────────────────────
st.title("🔬 AI Code Debugger",anchor=False)
st.caption("Upload a screenshot of your code error and let Gemini AI find the bug and provide a solution.")
st.divider()

# ── Upload ──────────────────────────────────────────────────────────────────
st.subheader("📁 Upload Screenshot",anchor=False)
uploaded_file = st.file_uploader(
    "Drag and drop your code error screenshot here",
    type=["png", "jpg", "jpeg"],
    help="Supported formats: PNG, JPG, JPEG",
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption=f"📌 {uploaded_file.name}", use_container_width=True)
    st.success("✅ Screenshot uploaded successfully!")

st.divider()

# ── Debug Mode ──────────────────────────────────────────────────────────────
st.subheader("🎯 Select Debug Mode",anchor=False)

col1, col2 = st.columns(2)
with col1:
    st.info("💡 **Hints Only**\nGet guided clues to find the bug yourself. Great for learning!")
with col2:
    st.info("⚡ **Full Solution**\nGet the complete fixed code with full explanation.")

debug_mode = st.radio(
    "What do you want from the AI?",
    options=["💡 Hints Only", "⚡ Full Solution + Code"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# ── Debug Button ────────────────────────────────────────────────────────────
debug_clicked = st.button(
    "🚀 Debug My Code",
    type="primary",
    use_container_width=True,
    disabled=not uploaded_file,
)

# ── Logic ───────────────────────────────────────────────────────────────────
if debug_clicked:
    if "Hints" in debug_mode:
        prompt = """You are an expert code debugger. Analyze the code error screenshot provided.

Give HINTS only (do not give the full solution or corrected code).

Your response should include:
1. **Error Identification**: What type of error is this? (syntax, runtime, logic, etc.)
2. **Error Location**: Where in the code does the error occur?
3. **Hints to Fix**: Provide 3-5 helpful hints that guide the user toward fixing the bug on their own.
4. **Key Concepts**: Mention any relevant programming concepts the user should review.

Format your response clearly using markdown with headers and bullet points."""
    else:
        prompt = """You are an expert code debugger. Analyze the code error screenshot provided.

Give a COMPLETE SOLUTION with corrected code.

Your response should include:
1. **Error Identified**: Clearly state what the bug/error is.
2. **Root Cause**: Explain why this error occurred.
3. **Fixed Code**: Provide the complete corrected code in a proper code block.
4. **Explanation**: Walk through what changes were made and why.
5. **Best Practices**: Any additional tips to avoid this error in the future.

Format your response clearly using markdown with headers, bullet points, and code blocks."""

    with st.spinner("🤖 Gemini AI is analyzing your code..."):
        try:
            image = Image.open(uploaded_file)
            model = genai.GenerativeModel("gemini-3-flash-preview")
            response = model.generate_content([prompt, image])
            result_text = response.text

            st.divider()
            st.success("✅ Analysis complete!")

            # ── Result metrics ──────────────────────────────────────────────
            m1, m2, m3 = st.columns(3)
            m1.metric("Mode", "Hints" if "Hints" in debug_mode else "Full Solution")
            m2.metric("Model", "gemini-3-flash-preview")
            m3.metric("Status", "Done ✓")

            st.divider()

            # ── Report ──────────────────────────────────────────────────────
            st.subheader("📋 AI Debug Report",anchor=False)

            with st.container(border=True):
                st.markdown(result_text)

            st.divider()

            # ── Download ────────────────────────────────────────────────────
            st.download_button(
                label="📥 Download Report",
                data=result_text,
                file_name="debug_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.warning("💡 Please check your GEMINI_API_KEY in the .env file and try again.")

# ── Footer ──────────────────────────────────────────────────────────────────
st.divider()
 
col1, col2, col3 = st.columns(3)
 
with col1:
    st.caption("👨‍💻 **Developer**")
    st.caption("Sayem Mahmud")
 
with col2:
    st.caption("🎓 **Education**")
    st.caption("AIUB · 8th Semester")
 
with col3:
    st.caption("📧 **Contact**")
    st.caption("Sayem205258@gmail.com")
 
st.divider()
st.caption(" AI Code Debugger · Built with Streamlit & Gemini AI · © 2025 Sayem Mahmud")









