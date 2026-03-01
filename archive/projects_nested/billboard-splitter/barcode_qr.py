# Plik: barcode_qr.py
# barcode_qr.py
import qrcode
from qrcode.constants import ERROR_CORRECT_L
# Używamy SvgImage zamiast SvgPathImage, aby uniknąć błędu TypeError w lxml
from qrcode.image.svg import SvgImage # <<< ZMIANA TUTAJ
from barcode import Code128
from barcode.writer import SVGWriter
# PIL nie jest potrzebny, jeśli create_registration_mark jest nieużywany
# from PIL import Image, ImageDraw
import io
import logging # Dodaj import logging

# Pobierz logger używany w splitterze lub skonfiguruj nowy
# To zadziała, jeśli ten moduł jest importowany PO konfiguracji loggera w splitter.py
# W przeciwnym razie, logi stąd mogą nie pojawić się zgodnie z konfiguracją.
# Alternatywnie, przekaż logger jako argument do funkcji.
logger = logging.getLogger('BillboardSplitter')
# Podstawowa konfiguracja, jeśli logger nie został jeszcze skonfigurowany
if not logger.hasHandlers():
    try:
        handler = logging.StreamHandler() # Domyślnie do stderr/konsoli
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING) # Ustaw domyślny poziom na WARNING
        logger.propagate = False # Zapobiegaj podwójnemu logowaniu do roota
        logger.debug("Skonfigurowano podstawowy handler dla loggera w barcode_qr.py")
    except Exception as e:
        print(f"Nie udało się skonfigurować podstawowego loggera w barcode_qr: {e}")


# Definicja koloru - używamy hex, co oznacza zwykły czarny w SVG/PDF
BARCODE_COLOR = "#000000" # Zmieniono nazwę dla jasności

def generate_qr(data: str) -> io.BytesIO | None:
    """Generuje kod QR w formacie SVG jako obiekt BytesIO."""
    if not data:
        logger.warning("Próba wygenerowania QR kodu dla pustych danych.")
        return None
    try:
        qr = qrcode.QRCode(
            error_correction=ERROR_CORRECT_L, # Niski poziom korekcji (mniej modułów)
            box_size=10, # Rozmiar względny modułu
            border=1,    # Minimalna ramka (strefa ciszy), 1 lub więcej
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Używamy SvgImage, ustawiając kolor wypełnienia i jawnie białe tło
        # module_color - kolor modułów QR, background - kolor tła
        img = qr.make_image(image_factory=SvgImage, module_color=BARCODE_COLOR, background='white') # <<< ZMIANA TUTAJ

        # Zapisz SVG do bufora BytesIO jako UTF-8
        buffer = io.BytesIO()
        svg_string = img.to_string(encoding='unicode') # Pobierz SVG jako string
        # Add title after the opening svg tag
        svg_string = svg_string.replace('<svg', f'<svg>\n<title>{data}</title>\n', 1)
        buffer.write(svg_string.encode('utf-8'))       # Zakoduj do UTF-8 i zapisz w buforze binarnym

        buffer.seek(0)
        logger.debug(f"Wygenerowano QR kod SVG dla: {data[:30]}...")
        return buffer
    except Exception as e:
        logger.error(f"Błąd generowania QR kodu dla danych '{data}': {e}", exc_info=True)
        return None

def generate_barcode(data: str) -> io.BytesIO | None:
    """Generuje kod kreskowy (Code128) w formacie SVG jako obiekt BytesIO.
    
    Logika została zmodyfikowana, aby poprawnie obsługiwać pozycję tekstu:
    - 'bottom': Generuje SVG z tekstem pod spodem (domyślne zachowanie biblioteki).
    - 'side': Generuje SVG BEZ tekstu, aby umożliwić jego osobne narysowanie w splitterze.
    - 'none': Generuje SVG BEZ tekstu.
    """
    if not data:
        logger.warning("Próba wygenerowania kodu kreskowego dla pustych danych.")
        return None
    try:
        # Opcje dla SVGWriter (wartości w mm, dostosuj wg potrzeb)
        # https://python-barcode.readthedocs.io/en/stable/writers/svg.html#writer-options
        import config
        gs = config.settings.get("graphic_settings", {})
        font_size_val = gs.get("barcode_font_size", 8)

        options = {
            'module_width': 0.25,   # Szerokość najwęższego paska w mm (domyślnie 0.2)
            'module_height': 7.0,  # Wysokość pasków w mm (domyślnie 15.0)
            'font_size': int(font_size_val), # Rozmiar czcionki (0 lub pominięcie = brak tekstu)
            'text_distance': 3.0, # Odległość tekstu od kodu w mm (domyślnie 5.0)
            'quiet_zone': 0.0,    # Szerokość marginesu (strefy ciszy) ustawiona na 0
            'write_text': True,   # Domyślna wartość, zostanie nadpisana poniżej
            'background': 'white', # Kolor tła
            'foreground': BARCODE_COLOR, # Kolor pasków
        }
        
        # --- POPRAWIONA LOGIKA ---
        # Dopasowanie opcji do globalnego ustawienia pozycji opisu kodu kreskowego.
        import config
        text_pos = config.settings.get("barcode_text_position", "side") 

        if text_pos == "none":
            # Opcja "brak": Nie rysuj tekstu.
            options['write_text'] = False
            options['font_size'] = 0
            logger.debug(f"generate_barcode: tryb 'none', tekst wyłączony.")
        elif text_pos == "bottom":
            # Opcja "pod spodem": Użyj natywnego renderowania tekstu przez bibliotekę.
            options['write_text'] = True
            options['font_size'] = int(font_size_val)
            logger.debug(f"generate_barcode: tryb 'bottom', tekst włączony (pod spodem).")
        elif text_pos == "side":
            # Opcja "obok": Wyłącz tekst w SVG. Zostanie on narysowany osobno w splitter.py.
            options['write_text'] = False
            options['font_size'] = 0
            logger.debug(f"generate_barcode: tryb 'side', tekst wyłączony w SVG (będzie rysowany osobno).")
        # --- KONIEC POPRAWIONEJ LOGIKI ---
            
        writer = SVGWriter()
        # Kod Code128 nie potrzebuje sumy kontrolnej, biblioteka ją dodaje.
        code128 = Code128(data, writer=writer)

        # Zapisz SVG do bufora BytesIO jako UTF-8.
        buffer = io.BytesIO()
        # Metoda 'write' oczekuje pliku binarnego; przekazujemy opcje tutaj.
        code128.write(buffer, options=options) 

        buffer.seek(0)
        logger.debug(f"Wygenerowano kod kreskowy SVG dla: {data[:30]}...")
        return buffer
    except Exception as e:
        logger.error(f"Błąd generowania kodu kreskowego dla danych '{data}': {e}", exc_info=True)
        return None

def generate_barcode_with_text_forced(data: str, write_text: bool) -> io.BytesIO | None:
    """
    Funkcja pomocnicza generująca kod kreskowy z jawnym ustawieniem opcji 'write_text'.
    Używana w splitterze do uzyskania spójnych wymiarów do skalowania.
    """
    if not data:
        logger.warning("Próba wygenerowania kodu kreskowego dla pustych danych.")
        return None
    try:
        import config
        gs = config.settings.get("graphic_settings", {})
        font_size_val = gs.get("barcode_font_size", 8)

        options = {
            'module_width': 0.25,
            'module_height': 7.0,
            'font_size': int(font_size_val) if write_text else 0,
            'text_distance': 3.0,
            'quiet_zone': 0.0, 
            'write_text': write_text,
            'background': 'white',
            'foreground': BARCODE_COLOR,
        }
        
        writer = SVGWriter()
        code128 = Code128(data, writer=writer)
        buffer = io.BytesIO()
        code128.write(buffer, options=options)
        buffer.seek(0)
        # Dodano logowanie dla ułatwienia diagnostyki
        logger.debug(f"generate_barcode_with_text_forced (write_text={write_text}) wygenerował SVG dla: {data[:30]}...")
        return buffer
    except Exception as e:
        logger.error(f"Błąd generowania kodu kreskowego (forced) dla danych '{data}': {e}", exc_info=True)
        return None