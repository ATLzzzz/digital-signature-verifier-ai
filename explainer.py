import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ambil API key dari .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY tidak ditemukan di .env")

# Inisialisasi client
client = Groq(api_key=GROQ_API_KEY)
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"


def map_data_to_prompt_fields(data: dict) -> dict:
    status_map = {
        "VALID": "Tanda tangan valid dan sertifikat masih berlaku.",
        "SERTIFIKAT KADALUARSA": "Tanda tangan valid, tetapi sertifikat sudah kadaluwarsa.",
        "TANDA TANGAN TIDAK VALID": "Tanda tangan tidak cocok dengan dokumen. Mungkin dokumen telah diubah.",
        "GAGAL": f"Gagal memverifikasi: {data.get('error_message', 'Tidak diketahui')}."
    }

    return {
        "status_tanda_tangan": "Valid" if data.get("signature_match") else "Tidak Valid",
        "status_sertifikat": "Kedaluwarsa" if data.get("certificate_details", {}).get("is_expired") else "Masih Berlaku",
        "nama_pemilik": data.get("certificate_details", {}).get("subject", "Tidak tersedia"),
        "nama_penerbit": data.get("certificate_details", {}).get("issuer", "Tidak tersedia"),
        "tanggal_kadaluarsa": data.get("certificate_details", {}).get("valid_to", "Tidak diketahui"),
        "info_tambahan": status_map.get(data.get("overall_status"), "Tidak diketahui")
    }


def generate_explanation(data: dict) -> str:
    fields = map_data_to_prompt_fields(data)

    prompt = f"""
Kamu adalah asisten AI yang menjelaskan hasil verifikasi tanda tangan digital.
Berikut hasil verifikasi yang perlu dijelaskan:

- Status tanda tangan: {fields['status_tanda_tangan']}
- Status sertifikat: {fields['status_sertifikat']}
- Nama pemilik: {fields['nama_pemilik']}
- Nama penerbit sertifikat: {fields['nama_penerbit']}
- Berlaku sampai: {fields['tanggal_kadaluarsa']}
- Informasi tambahan: {fields['info_tambahan']}

Jelaskan dengan bahasa sederhana agar mudah dipahami ASN atau masyarakat awam.
"""

    try:
        response = client.chat.completions.create(
            model=DEFAULT_GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Kamu adalah AI yang menjelaskan hasil verifikasi tanda tangan digital."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Penjelasan AI tidak dapat dibuat: {str(e)}"
