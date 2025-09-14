from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import datetime

def load_certificate(cert_path):
    """Load X.509 certificate from file"""
    with open(cert_path, "rb") as f:
        return x509.load_pem_x509_certificate(f.read())

def load_signature(sig_path):
    """Load digital signature"""
    with open(sig_path, "rb") as f:
        return f.read()

def load_document(doc_path):
    """Load document as bytes"""
    with open(doc_path, "rb") as f:
        return f.read()

def verify_signature(document_path, signature_path, cert_path):
    """Verify digital signature validity and certificate status"""
    try:
        cert = load_certificate(cert_path)
        signature = load_signature(signature_path)
        document = load_document(document_path)

        public_key = cert.public_key()

        # Verify digital signature
        try:
            public_key.verify(
                signature,
                document,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            signature_status = "VALID"
        except Exception:
            signature_status = "TANDA TANGAN TIDAK VALID"

        # Certificate expiry check
        is_expired = datetime.datetime.utcnow() > cert.not_valid_after

        result = {
            "signature_match": signature_status,
            "certificate_details": {
                "subject": cert.subject.rfc4514_string(),
                "issuer": cert.issuer.rfc4514_string(),
                "valid_from": cert.not_valid_before.isoformat(),
                "valid_to": cert.not_valid_after.isoformat(),
                "is_expired": is_expired
            },
            "overall_status": (
                "SERTIFIKAT KADALUARSA" if is_expired else signature_status
            )
        }

        return result

    except Exception as e:
        return {
            "signature_match": "GAGAL",
            "certificate_details": {},
            "overall_status": "GAGAL",
            "error_message": str(e)
        }
