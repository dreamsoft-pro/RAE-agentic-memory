import pytest
import fitz
import os

def test_pymupdf_user_unit_support():
    """
    Test sprawdza, czy PyMuPDF potrafi zapisać i odczytać UserUnit.
    Tworzymy stronę 100x100 pkt.
    Ustawiamy UserUnit na 10.0.
    Oczekujemy, że przy odczycie wymiary będą 1000x1000 pkt (lub biblioteka pozwoli odczytać UserUnit).
    """
    filename = "test_user_unit.pdf"
    
    # 1. Tworzenie PDF
    doc = fitz.open()
    page = doc.new_page(width=100, height=100)
    
    # Ustawienie UserUnit bezpośrednio w słowniku strony
    # PyMuPDF pozwala na dostęp do obiektu xref strony
    # page.set_userunit(10.0) # Brak metody w starszych wersjach/niektórych buildach
    doc.xref_set_key(page.xref, "UserUnit", "10.0")
    
    # Rysujemy prostokąt, żeby coś było
    page.draw_rect(fitz.Rect(10, 10, 90, 90), color=(1, 0, 0), width=2)
    
    doc.save(filename)
    doc.close()
    
    # 2. Weryfikacja
    check_doc = fitz.open(filename)
    check_page = check_doc[0]
    
    # Sprawdźmy wymiary (mediabox / rect)
    rect = check_page.rect
    print(f"\nOriginal Rect: 100x100")
    print(f"Read Rect: {rect.width}x{rect.height}")
    
    # Sprawdźmy UserUnit (powinien być 10.0)
    # W nowszych PyMuPDF (od 1.19?) jest page.userunit
    # Jeśli nie ma, musimy czytać ze słownika
    try:
        user_unit = check_page.userunit
        print(f"Read UserUnit: {user_unit}")
        assert abs(user_unit - 10.0) < 0.001
    except AttributeError:
        # Fallback dla starszych wersji: czytanie surowego słownika PDF
        xref = check_page.xref
        user_unit_raw = check_doc.xref_get_key(xref, "UserUnit")
        print(f"Raw UserUnit from xref: {user_unit_raw}")
        assert user_unit_raw[0] != "null"
        assert abs(float(user_unit_raw[1]) - 10.0) < 0.001

    # PyMuPDF (fitz) zazwyczaj zwraca rect JUŻ PRZESKALOWANY przez UserUnit w nowszych wersjach?
    # Sprawdźmy to. Jeśli UserUnit działa, to rect powinien być 1000x1000?
    # A może rect jest fizyczny (100x100), a UserUnit to mnożnik?
    # Specyfikacja PDF mówi, że UserUnit zmienia interpretację jednostek.
    # Zobaczymy co zwróci test.
    
    check_doc.close()
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    test_pymupdf_user_unit_support()
