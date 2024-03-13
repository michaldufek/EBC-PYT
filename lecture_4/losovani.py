# Losovani sportky
import random

"""
Losování sportky: místo losování vytvořte funkci, která vrátí seznam 7 náhodných čísel z intervalu 1 až 49 (čísla se mohou v seznamu objevovat jen jednou). 
Uživatel zadá typ (svých 6 čísel). Aplikace vypíše, která čísla uživatel uhodnul a kolikátou cenu obdrží (1. až 3.) pokud cenu neobdrží, může typovat nová čísla, ty však bude porovnávat s nově  vylosovanými.
"""

def losuj_cisla():
    """Vrátí seznam 7 náhodných, jedinečných čísel z intervalu 1 až 49."""
    return random.sample(range(1, 50), 7)


def zkontroluj_typy(uzivatelske_cisla, vylosovane_cisla):
    """Porovná uživatelské čísla s vylosovanými a vrací počet shod."""
    shody = set(uzivatelske_cisla).intersection(set(vylosovane_cisla))
    return shody


def main():
    done = False  # Inicializace proměnné pro kontrolu ukončení
    while not done:
        # Vylosování čísel
        vylosovane_cisla = losuj_cisla()
        print("Vylosovaná čísla:", sorted(vylosovane_cisla))
        
        # Získání tipů od uživatele
        uzivatelske_cisla = input("Zadejte vašich 6 čísel oddělených čárkou (např. 1,2,3,4,5,6): ")
        uzivatelske_cisla = [int(x.strip()) for x in uzivatelske_cisla.split(',')]

        # Kontrola shod
        shody = zkontroluj_typy(uzivatelske_cisla, vylosovane_cisla)
        print("Uhodnutá čísla:", sorted(shody))
        
        # Určení výhry
        pocet_shod = len(shody)
        if pocet_shod == 6:
            print("Gratulujeme! Obdržíte 1. cenu!")
            done = True
        elif pocet_shod == 5:
            print("Gratulujeme! Obdržíte 2. cenu!")
            done = True
        elif pocet_shod == 4:
            print("Gratulujeme! Obdržíte 3. cenu!")
            done = True
        else:
            print("Bohužel jste nevyhráli. Zkuste to znovu.")


if __name__ == "__main__":
    main()

# EoF