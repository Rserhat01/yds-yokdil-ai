import streamlit as st
import openai

# ✅ OpenAI API anahtarı Streamlit Cloud'dan geliyor
openai.api_key = st.secrets["OPENAI_API_KEY"]

def analyze_question(text: str) -> str:
    """
    Verilen soruyu analiz eder ve 3 satırlık YÖKDİL/YDS formatında cevap üretir.

    1. satır: Doğru şık (örn: C şıkkı)
    2. satır: Türkçe açıklama + çeviri (sade)
    3. satır: Önem ve çıkma ihtimali (örn: x/10)
    """

    prompt = f"""
Soru: {text}

Sen deneyimli bir YÖKDİL/YDS eğitmenisin.
Aşağıdaki kurallara göre sadece 3 satırdan oluşan cevap üret:

1. satır: Sadece doğru şıkkı yaz (örn: C şıkkı)
2. satır: Türkçe açıklama + çeviri (kısa, sade)
3. satır: Önem: x/10 | Çıkma ihtimali: x/10

Başka açıklama yazma, sadece 3 satırlık sade çıktı ver.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sen uzman bir YÖKDİL/YDS analiz asistanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        st.error("❌ LLM cevabı alınırken hata oluştu.")
        return f"[HATA] {e}"
