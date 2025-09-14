from verifier import verify_signature
from explainer import generate_explanation
import os

def main():
    doc = "data/sample.pdf"
    sig = "data/sample.sig"
    cert = "data/sample.crt"

    print("🔎 Memverifikasi dokumen...")

    # Pastikan file ada
    missing = []
    for path in [doc, sig, cert]:
        if not os.path.isfile(path):
            missing.append(path)
    if missing:
        print(f"Error: file(s) berikut tidak ditemukan: {', '.join(missing)}")
        return

    result = verify_signature(doc, sig, cert)
    print("\n📑 Hasil Verifikasi (Raw):")
    print(result)

    print("\n🤖 Penjelasan AI:")
    explanation = generate_explanation(result)
    print(explanation)

if __name__ == "__main__":
    main()
