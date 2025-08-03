# 📄 utils/ocr.py

import easyocr
from PIL import Image
import numpy as np
import tempfile
import os

# OCR okuyucuyu global tanımla (her seferinde yeniden başlatmaz)
reader = easyocr.Reader(['en', 'tr'], gpu=False)

def extract_text_from_image(uploaded_file) -> str:
    """
    Kullanıcıdan yüklenen görselden OCR ile metin çıkarır.
    """
    try:
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        # Görseli yükle ve RGB'ye çevir
        image = Image.open(tmp_file_path).convert("RGB")
        img_array = np.array(image)

        # OCR ile metni al
        result = reader.readtext(img_array, detail=0)
        return " ".join(result).strip()

    except Exception as e:
        return f"[HATA] OCR sırasında sorun oluştu: {e}"

    finally:
        # Geçici dosyayı sil
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
