from .models import Invoice


def add_invoice(parsed_data, user, typ):  # TODO: remove
    faktura = Invoice.objects.create(
        typ=typ,
        user=user,
        numer=parsed_data.get("numer", ""),
        data_sprzedazy=parsed_data.get("data_sprzedazy", None),
        kontrahent=parsed_data.get("kontrahent", ""),
        adres_siedziba=parsed_data.get("adres_siedziba", ""),
        kwota_vat=parsed_data.get("kwota_vat", 0),
        kwota_brutto=parsed_data.get("kwota_brutto", 0),
        plik_pdf=parsed_data.get("plik_pdf", None),
    )
    return faktura
