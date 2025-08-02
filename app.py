# -----------------------------------------------------------
#  DreamSeed 2.10 – Marketing Copy & Micro-Growth Edition
# -----------------------------------------------------------
import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
import requests
import re
import json
import zipfile
import io
from fpdf import FPDF
import backoff

# ---------------- CONFIGURATION ----------------
export_folder = Path("outputs")
export_folder.mkdir(exist_ok=True)
FONT_DIR = Path(__file__).parent / "assets"
FONT_NORMAL = FONT_DIR / "DejaVuSans.ttf"
FONT_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"

# -----------------------------------------------------------
#  HELPERS
# -----------------------------------------------------------
@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=3)
def call_ollama(prompt: str, model: str = "gemma") -> str:
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120
    )
    r.raise_for_status()
    return r.json()["response"]

def safe_slug(text: str) -> str:
    return re.sub(r'[^0-9a-zA-Z0-9_-]+', '_', text).strip('_')[:40] or "untitled"

def safe_multi_cell(pdf, text, width=0, height=10):
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.alias_nb_pages()
    paragraphs = text.split("\n\n")
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if para.startswith("#"):
            pdf.set_font("DejaVu", style="B", size=14)
            pdf.cell(0, 10, para.strip("# "), ln=True)
            continue
        else:
            pdf.set_font("DejaVu", size=12)
        if pdf.get_y() + 30 > pdf.h - 20:
            pdf.add_page()
        pdf.multi_cell(width, height, para)
        pdf.ln(2)

# -----------------------------------------------------------
#  SIDEBAR
# -----------------------------------------------------------
st.sidebar.title("DreamSeed")
product_idea = st.sidebar.text_input("🌱 Enter your Product Idea")
audience = st.sidebar.text_input("Who is it for?")
format_choice = st.sidebar.selectbox(
    "Format", ["eBook", "Video Course", "Workshop Outline", "Printable PDF Guide",
               "Notion Template", "Email Series", "Funnel Script", "Web App (MVP)",
               "Interactive Quiz", "Social Media Toolkit"]
)
voice = st.sidebar.selectbox("Tone", ["Conversational", "Academic", "Story-driven"])
model_choice = st.sidebar.selectbox("Model", ["Local (Ollama)", "OpenAI (API)"])
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password") if model_choice == "OpenAI (API)" else None

if model_choice == "OpenAI (API)" and openai_api_key:
    st.sidebar.caption(f"Estimated cost: ~${len(product_idea)//4 * 0.03 / 1000:.3f} USD")

if st.sidebar.button("🗑️ Clean Old Files"):
    cutoff = datetime.now().timestamp() - 24 * 3600
    for f in export_folder.iterdir():
        if f.stat().st_mtime < cutoff:
            f.unlink()
    st.sidebar.success("Old files removed.")

# -----------------------------------------------------------
#  MAIN
# -----------------------------------------------------------
st.title("🌱 DreamSeed: From Idea to Income")
st.markdown(
    """
Just tell us what you’re dreaming up.  
Fill out the sidebar with your product idea, who it’s for, and how you want it to feel.  
DreamSeed will generate a compelling product description, chapter outline, and basic marketing angles — ready to feed into your favorite AI model or creative process to bring your vision to life.
"""
)

if st.button("🌱 Generate Outline"):
    if not product_idea:
        st.error("Please enter a product idea.")
    else:
        with st.spinner("Creating your outline…"):
            try:
                prompt = f"""
You are DreamSeed, a product strategist.  
Create a {format_choice} outline for "{product_idea}" aimed at "{audience}".

Deliverables:
1. Title & subtitle
2. Format description (keep it {format_choice})
3. 3–5 section headers with one-line summaries
4. Monetization strategy
5. 3 sample social-media promos

Voice: {voice}
"""
                outline = call_ollama(prompt)
                st.session_state.outline = outline
                st.session_state.slug = safe_slug(product_idea)

                now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                slug = st.session_state.slug
                output_txt_file = export_folder / f"dreamseed_{slug}_outline_{now}.txt"
                output_pdf_file = export_folder / f"dreamseed_{slug}_outline_{now}.pdf"
                output_md_file = export_folder / f"dreamseed_{slug}_outline_{now}.md"

                output_txt_file.write_text(outline, encoding="utf-8")
                output_md_file.write_text(outline, encoding="utf-8")

                pdf = FPDF()
                pdf.add_page()
                if FONT_NORMAL.exists():
                    pdf.add_font("DejaVu", "", str(FONT_NORMAL), uni=True)
                    pdf.set_font("DejaVu", size=12)
                if FONT_BOLD.exists():
                    pdf.add_font("DejaVu", style="B", fname=str(FONT_BOLD), uni=True)
                safe_multi_cell(pdf, outline)
                pdf.output(str(output_pdf_file))

                st.success("Outline created!")
                st.markdown("---")
                st.subheader("🌱 Here’s What Your Idea Wants to Become")
                st.markdown(
                    """
Every heading can become a full chapter, course module, or email series.  
From a tiny idea, there is big growth ahead.
                    """
                )
                st.text_area("Outline", outline, height=400)

                st.subheader("📦 Downloads")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.download_button("📄 .txt", data=open(output_txt_file, "rb"), file_name=output_txt_file.name)
                with col2:
                    st.download_button("📄 .pdf", data=open(output_pdf_file, "rb"), file_name=output_pdf_file.name)
                with col3:
                    st.download_button("📄 .md", data=open(output_md_file, "rb"), file_name=output_md_file.name)
                with col4:
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                        zf.write(output_txt_file, output_txt_file.name)
                        zf.write(output_pdf_file, output_pdf_file.name)
                        zf.write(output_md_file, output_md_file.name)
                    st.download_button("📦 Bundle.zip", data=zip_buffer.getvalue(), file_name=f"dreamseed_{slug}_bundle.zip")

            except Exception as e:
                st.error(f"Error: {e}")

# -----------------------------------------------------------
#  GOODBYE BUTTON
# -----------------------------------------------------------
st.markdown("---")
if st.button("👋 Exit DreamSeed"):
    st.warning("Please close this browser tab to exit DreamSeed.")