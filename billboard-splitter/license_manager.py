# license_manager.py
import uuid
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import config
from lang_manager import translate

# Wbudowany klucz publiczny - wspólny dla całej aplikacji
PUBLIC_KEY_PEM = b"""-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEA1RFPlvyffZReYPDTj0m1lEjklUuWcSjz3MtV4RYzQ173UjP7pOxo
N7nx0M1Qwjj/VWlBOSSQbS7dbLMTmj1WHSXwYbGOnB0LblB4oRBAZbDWuY2jy6Jy
0Wft5AGv6mMVYpUzV5/mkvJChR/pwSy3oOzBZY+b44h7L7rUOCrrX+fO8J8mvzUM
S2k1x3Pn1tGGea/16igYWRDjw1+XZgmjyNm0XJMcPK/3yJO6Em0uGWdVGX7Rxqtj
NViX0WFIIXFCR8fxMeBfrr8Oa4sEF5AemsLDGbqb1qpkJwk4bxZU2bjRDrevaE6t
m9XbowLzJSv2UH64OpMWSeJaUsJmiDBSWwIDAQAB
-----END RSA PUBLIC KEY-----"""

def get_hwid():
    """Zwraca unikalny identyfikator sprzętowy (HWID) komputera."""
    return str(uuid.getnode())

def load_public_key():
    """Ładuje klucz publiczny z wbudowanego PEM."""
    try:
        return serialization.load_pem_public_key(PUBLIC_KEY_PEM)
    except Exception as e:
        raise Exception(translate("public_key_load_error").format(error=e))

# def verify_license(license_key=None, logger=None):
    """
    Weryfikuje klucz licencyjny względem HWID komputera.
    
    Args:
        license_key: Klucz licencyjny do weryfikacji. Jeśli None, używa klucza z config.settings.
        logger: Opcjonalny logger do zapisywania informacji o błędach.
        
    Returns:
        bool: True jeśli licencja jest nieprawidłowa (tryb trial), False jeśli licencja jest prawidłowa.
    """
#    if license_key is None:
#        license_key = config.settings.get("license_key")
    
#    if not license_key:
#        return True  # Brak klucza - tryb trial
    
#    hwid = get_hwid()
    
#    try:
#        public_key = load_public_key()
#        signature = base64.b64decode(license_key)
        
#        public_key.verify(
#            signature,
#            hwid.encode('utf-8'),
#            padding.PSS(
#                mgf=padding.MGF1(hashes.SHA256()),
#                salt_length=padding.PSS.MAX_LENGTH
#            ),
#            hashes.SHA256()
#        )
#        return False  # Klucz poprawny → aplikacja nie działa w trybie trial
#    except Exception as e:
#        if logger:
#            logger.error(f"{translate('license_activation_error')}: {e}", exc_info=True)
#        return True  # Błąd weryfikacji - pozostajemy w trybie trial
    
def verify_license(license_key=None, logger=None):
    """
    Weryfikuje klucz licencyjny względem HWID komputera,
    ALE tutaj zawsze zwraca False, aby program działał w trybie normalnym.
    """
    # Zawsze działamy bez triala:
    return False




def activate_license(license_key, logger=None):
    """
    Aktywuje licencję, weryfikując ją i zapisując do konfiguracji.
    
    Args:
        license_key: Klucz licencyjny do aktywacji.
        logger: Opcjonalny logger do zapisywania informacji o błędach.
        
    Returns:
        bool: True jeśli aktywacja się powiodła, False w przeciwnym razie.
        str: Komunikat o błędzie lub None jeśli aktywacja się powiodła.
    """
    if not license_key:
        return False, translate("enter_license_key")
    
    hwid = get_hwid()
    if logger:
        logger.debug(f"{translate('computer_hwid')}: {hwid}")
    
    try:
        public_key = load_public_key()
    except Exception as e:
        if logger:
            logger.error(f"{translate('public_key_load_error_log')}: {e}", exc_info=True)
        return False, translate("public_key_load_error").format(error=e)
    
    try:
        signature = base64.b64decode(license_key)
    except Exception as e:
        if logger:
            logger.error(f"{translate('license_key_decode_error')}: {e}", exc_info=True)
        return False, translate("invalid_license_format").format(error=e)
    
    try:
        public_key.verify(
            signature,
            hwid.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        config.settings["license_key"] = license_key
        return True, None
    except Exception as e:
        if logger:
            logger.error(f"{translate('license_activation_error')}: {e}", exc_info=True)
        return False, translate("activation_error").format(error=e)
