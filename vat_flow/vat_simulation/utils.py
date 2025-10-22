import csv
import re
from datetime import datetime

import fitz

from .models import BillingRecord


class Utils:
    @staticmethod
    def to_float_safe(val, label=""):
        if val is None or val == "":
            print(f"Missing value in field {label}")
            return 0
        val = str(val).replace(" ", "").replace(",", ".")
        try:
            return float(val)
        except Exception:
            print(f"Invalid value '{val}' in field {label}")
            return 0


class InvoiceParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = self._extract_text()

    def _extract_text(self) -> str:
        doc = fitz.open(self.pdf_path)
        return "".join(page.get_text() for page in doc)

    def _search(self, pattern: str):
        match = re.search(pattern, self.text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def get_data(self) -> dict:
        suma_netto = self._search(r"Suma wartość netto[:\s]*([\d\s.,]+)")
        suma_vat = self._search(r"suma podatek VAT[:\s]*([\d\s.,]+)")
        suma_brutto = self._search(r"suma wartość brutto[:\s]*([\d\s.,]+)")

        return {
            "numer": self._search(r"Numer Faktury[:\s]*([A-Za-z0-9/\-]+)"),
            "data_wystawienia": self._search(
                r"data wystawienia[:\s]+(\d{2}[-/\.]\d{2}[-/\.]\d{4}|\d{4}[-/\.]\d{2}[-/\.]\d{2})"
            ),
            "data_sprzedazy": self._search(r"data sprzedaży[:\s]*([\d\-/.]{2,10})"),
            "kontrahent": self._search(r"Kontrahent:\s*([^\n]+)"),
            "adres_siedziba": self._search(r"Adres \(siedziba\):\s*([^\n]+)"),
            "nip": self._search(r"NIP[:\s]*([\d\-]+)"),
            "wart_netto_23": suma_netto
            if suma_netto
            else self._search(r"wartość netto 23%[:\s]*([\d\s.,]+)"),
            "podatek_vat_23": suma_vat
            if suma_vat
            else self._search(r"Podatek VAT 23%[:\s]*([\d\s.,]+)"),
            "wart_brutto_23": suma_brutto
            if suma_brutto
            else self._search(r"Wartość brutto 23%[:\s]*([\d\s.,]+)"),
            "wart_netto_8": self._search(r"wartość netto 8%[:\s]*([\d\s.,]+)"),
            "podatek_vat_8": self._search(r"Podatek VAT 8%[:\s]*([\d\s.,]+)"),
            "wart_brutto_8": self._search(r"Wartość brutto 8%[:\s]*([\d\s.,]+)"),
            "suma_wart_netto": suma_netto,
            "suma_podatek_vat": suma_vat,
            "suma_wart_brutto": suma_brutto,
        }


class InvoiceCSVImporter:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def parse_date(self, value):
        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except Exception:
                continue
        return None

    def import_invoices(self):
        with open(self.csv_path, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_wystawienia = self.parse_date(row["Data wystawienia"])
                data_sprzedazy = self.parse_date(row.get("Data sprzedaży", ""))
                BillingRecord.objects.update_or_create(
                    numer=row["Numer faktury"],
                    defaults={
                        "data_wystawienia": data_wystawienia,
                        "data_sprzedazy": data_sprzedazy,
                        "kontrahent": row.get("Kontrahent"),
                        "adres_siedziba": row.get("Adres (siedziba)"),
                        "nip": row.get("NIP"),
                        "wart_netto_8": Utils.to_float_safe(
                            row.get("Wartość netto 8%"), "Wartość netto 8%"
                        ),
                        "podatek_vat_8": Utils.to_float_safe(
                            row.get("Podatek VAT 8%"), "Podatek VAT 8%"
                        ),
                        "wart_brutto_8": Utils.to_float_safe(
                            row.get("Wartość brutto 8%"), "Wartość brutto 8%"
                        ),
                        "wart_netto_23": Utils.to_float_safe(
                            row.get("Wartość netto 23%"), "Wartość netto 23%"
                        ),
                        "podatek_vat_23": Utils.to_float_safe(
                            row.get("Podatek VAT 23%"), "Podatek VAT 23%"
                        ),
                        "wart_brutto_23": Utils.to_float_safe(
                            row.get("Wartość brutto 23%"), "Wartość brutto 23%"
                        ),
                        "suma_wart_netto": Utils.to_float_safe(
                            row.get("Suma wartość netto"), "Suma wartość netto"
                        ),
                        "suma_podatek_vat": Utils.to_float_safe(
                            row.get("Suma podatek VAT"), "Suma podatek VAT"
                        ),
                        "suma_wart_brutto": Utils.to_float_safe(
                            row.get("Suma wartość brutto"), "Suma wartość brutto"
                        ),
                    },
                )
