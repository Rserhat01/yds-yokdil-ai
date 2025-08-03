# 📄 utils/vocab_tracker.py

import streamlit as st
import json
import os
import re
from googletrans import Translator

VOCAB_PATH = "data/vocab.json"
translator = Translator()

# Dosya var mı kontrolü, yoksa oluştur
os.makedirs("data", exist_ok=True)
if not os.path.exists(VOCAB_PATH):
    with open(VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump({}, f)


def load_vocab() -> dict:
    try:
        with open(VOCAB_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except json.JSONDecodeError:
        st.warning("⚠️ Kelime dosyası bozuk. Yeni dosya oluşturuluyor.")
        return {}


def save_vocab(vocab: dict):
    with open(VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)


def update_vocab_list(text: str):
    """
    Verilen metindeki İngilizce kelimeleri tespit edip Türkçe karşılıklarıyla kaydeder.
    """
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text)
    words = list(set(word.lower() for word in words))

    vocab = load_vocab()

    for word in words:
        if word not in vocab:
            try:
                translation = translator.translate(word, src="en", dest="tr").text
                vocab[word] = translation
            except Exception as e:
                vocab[word] = "-"
                st.warning(f"{word} kelimesi çevrilemedi: {e}")

    save_vocab(vocab)


def show_vocab_list():
    """
    Kayıtlı kelime listesini gösterir.
    """
    vocab = load_vocab()
    if not vocab:
        st.info("📭 Henüz kelime eklenmedi.")
        return

    st.subheader("📘 Kelime Defteri")
    for word, translation in vocab.items():
        st.markdown(f"🔹 **{word}** → _{translation}_")
