# 📄 utils/llm_analyze.py

import streamlit as st
from openai import OpenAI

# OpenAI istemcisi: API anahtarı artık streamlit secrets'tan geliyor
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def analyze_question(text: str) -> str:
    """
    Verilen soruyu analiz eder ve 3 satırlık YÖKDİL/YDS formatında cevap üretir.

    1. satır: Doğru şık (örnek: B şıkkı)
    2. satır: Türkçe açıklama + çeviri
    3. satır: Önem ve çıkma ihtimali (örn: Önem: 8/10 | Çıkma ihtimali: 9/10)
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
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sen uzman bir YÖKDİL/YDS analiz asistanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[HATA] LLM cevap verirken sorun oluştu: {e}"
