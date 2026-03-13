from django import forms

class OfflineImportForm(forms.Form):
    jsonl_file = forms.FileField(
        label="Wybierz plik .jsonl",
        help_text="Plik wygenerowany przez ScreenWatcher Agent w trybie offline."
    )
    process_oee = forms.BooleanField(
        initial=True, 
        required=False, 
        label="Przelicz OEE",
        help_text="Automatycznie wyzwalaj obliczenia OEE i wykrywanie przestojów dla zaimportowanych danych."
    )
