import fitz
import os

def test_huge_page_physical():
    """
    Test sprawdza, czy można stworzyć stronę o szerokości 6000mm (~17000 pkt)
    bez użycia UserUnit, i czy zostanie ona poprawnie zapisana.
    """
    filename = "test_huge.pdf"
    
    width_mm = 6000.0
    height_mm = 3000.0
    
    width_pt = width_mm * (72/25.4) # ~17007 pkt
    height_pt = height_mm * (72/25.4) # ~8503 pkt
    
    print(f"Creating page: {width_pt:.2f} x {height_pt:.2f} pts")
    
    doc = fitz.open()
    # PyMuPDF domyślnie tworzy PDF 1.4, ale automatycznie podbija wersję?
    # Sprawdźmy.
    page = doc.new_page(width=width_pt, height=height_pt)
    
    # Rysujemy przekątną
    page.draw_line(fitz.Point(0, 0), fitz.Point(width_pt, height_pt), color=(1, 0, 0), width=5)
    
    doc.save(filename)
    doc.close()
    
    # Weryfikacja
    check_doc = fitz.open(filename)
    page = check_doc[0]
    # print(f"PDF Version: {check_doc.version}") # Attribute not available in all versions
    print(f"Read Rect: {page.rect.width:.2f} x {page.rect.height:.2f}")
    
    assert abs(page.rect.width - width_pt) < 1.0
    
    check_doc.close()
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    test_huge_page_physical()
