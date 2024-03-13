import json

# Načtení JSON souboru
def nacti_json_soubor(nazev_souboru):
    try:
        with open(nazev_souboru, 'r', encoding='utf-8') as soubor:
            data = json.load(soubor)
        return data
    except Exception as e:
        print(f"Nastala chyba při načítání souboru: {e}")
        return None

def vyhodnot_odpoved(otazka, odpoved):
    body = 0
    for slovo, hodnota in otazka["klicova_slova"].items():
        if slovo in odpoved:
            body += hodnota
    # Ujistěte se, že počet bodů není záporný nebo vyšší než maximum
    body = max(0, min(body, otazka["max_body"]))
    return body

def spust_test():
    celkove_body = 0
    otazky = nacti_json_soubor("test.json")["otazky"]
    for cislo, otazka in enumerate(otazky):
        print(otazka["znění"])
        odpoved = input("Vaše odpověď: ").lower()  # Převedení odpovědi na malá písmena pro jednodušší porovnávání
        body = vyhodnot_odpoved(otazka, odpoved)
        print(f"Získali jste {body} bodů.\n")
        celkove_body += body
    print(f"Celkem jste získali {celkove_body} bodů.")

if __name__ == "__main__":
    spust_test()
