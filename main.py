# 📄 main.py
import streamlit as st
from utils.ocr import extract_text_from_image
from utils.llm_analyze import analyze_question
from utils.vocab_tracker import update_vocab_list, show_vocab_list
import json
import os
from dotenv import load_dotenv
load_dotenv()
st.markdown("<style>" + open("assets/dark_theme.css").read() + "</style>", unsafe_allow_html=True)


# Dark theme ayarı (Streamlit ayarlarında ayrıca tema seçilecek)
st.set_page_config(page_title="YDS/YÖKDİL AI Eğitmen", layout="centered")

# 📊 Kullanım istatistikleri dosyası
stats_path = "data/stats.json"
# Dosya yoksa veya boşsa baştan yaz
if not os.path.exists(stats_path) or os.path.getsize(stats_path) == 0:
    with open(stats_path, "w") as f:
        json.dump({"total_questions": 0}, f)

def update_stats():
    with open(stats_path, "r") as f:
        stats = json.load(f)
    stats["total_questions"] += 1
    with open(stats_path, "w") as f:
        json.dump(stats, f)

# 🎨 Arayüz Başlığı
st.markdown("""
    <h1 style='text-align: center; color: #E0E0E0;'>📘 YÖKDİL / YDS Akıllı Eğitmen</h1>
    <p style='text-align: center; color: #AAAAAA;'>Görselden soruyu analiz et, açıklama ve önem derecesini al!</p>
""", unsafe_allow_html=True)

# 📷 Görsel Yükleme
uploaded_file = st.file_uploader("Soru görselini yükle veya kamerayla çek:", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with st.spinner("🔍 Soru analiz ediliyor..."):
        question_text = extract_text_from_image(uploaded_file)
        if question_text:
            response = analyze_question(question_text)
            update_stats()
            update_vocab_list(question_text)

            st.markdown("---")
            st.subheader("📄 Çözüm")
            st.code(response, language="markdown")
        else:
            st.error("❌ Görselden metin çıkarılamadı. Daha net bir fotoğraf yükleyin.")

# 📈 İstatistik Paneli
with open(stats_path, "r") as f:
    stats = json.load(f)

with st.expander("📊 İstatistiklerim"):
    st.metric("Çözülen Soru Sayısı", stats["total_questions"])
    st.caption("İlerlemen otomatik kaydediliyor.")

# 📚 Kelime Defteri
with st.expander("📖 Kelime Defteri"):
    show_vocab_list()
