"""
script.py: třetí projekt do Engeto Online Python Akademie

author: Jan Juřík
email: jurik.jan.2222@gmail.com
discord: jackobs1395
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

# nacti html stranku a udelej soup
def nacti_html_stranku(url):
    file = requests.get(url)
    soup = BeautifulSoup(file.text, "html.parser")
    return soup

# vyber volebni vysledky
def ziskej_volebni_vysledky(soup) -> dict:
    """
    Z HTML struktury vybere hodnoty volebních výsledků
    :param soup: objekt html
    :return: slovník výsledků
    """
    vysledek = {}
    volici = soup.find_all("table")[0].find("td", headers="sa2").string
    vysledek["registered"] = int(vymaz_pevnou_mezeru(volici))
    obalek = soup.find_all("table")[0].find("td", headers="sa3").string
    vysledek["envelopes"] = int(vymaz_pevnou_mezeru(obalek))
    hlasu_celkem = soup.find_all("table")[0].find("td", headers="sa6").string
    vysledek["valid"] = int(vymaz_pevnou_mezeru(hlasu_celkem))

    for child in soup.find_all("table")[1:]:
        for elem in child.find_all("tr"):
            for i, td in enumerate(elem.find_all("td")):
                if "overflow_name" in td['class']:
                    jmeno_strany = td.text
                    hlasu = elem.find_all("td")[i+1].get_text()
                    vysledek[jmeno_strany] = int(vymaz_pevnou_mezeru(hlasu))
                    continue
    return vysledek

def vymaz_pevnou_mezeru(text: str) -> str:
    """
    Vymaže znak - pevnou mezeru z vloženého textu
    """
    if "\xa0" in text:
        text = text.replace("\xa0", "")
    return text

#ziskej seznam mest
def ziskej_seznam_mist(soup) -> list:
    """
    Ze stránky zvoleného územního celku vybere seznam mist a url stránek jejich volebních výsledků
    :param soup: objekt html struktury
    :return: list (id, misto, url)
    """
    prefix = "https://volby.cz/pls/ps2017nss/"
    output = []
    for elem in soup.find_all("tr"):
        for i, td in enumerate(elem.find_all("td")):
            if "overflow_name" in td['class']:
                mesto = td.text
                mesto_id = elem.find_all("td")[i - 1].text
                mesto_rel_link = elem.find_all("td")[i - 1].find('a')['href']
                mesto_link = prefix + mesto_rel_link
                output.append((int(mesto_id), mesto, mesto_link))
                continue
    return output

def priprav_vystup(url):
    """
    připraví požadované volební výsledky pro daný uzemní celek
    :param url: string, url odkaz (Př. https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103)
    :return: list slovniků
    """
    output = []
    for mesto in ziskej_seznam_mist(nacti_html_stranku(url)):
        print(mesto[1])
        soupis = {}
        soupis["code"] = mesto[0]
        soupis["location"] = mesto[1]
        soupis.update(ziskej_volebni_vysledky(nacti_html_stranku(mesto[2])))
        output.append(soupis)
    return output

# otestuj vstup
def test_vstupu():
    url = sys.argv[1]
    if not (requests.get(url).ok):
        print(f"smula, url doesn't exist. Chyba: {requests.get(url).status_code}")
        sys.exit(1)
    elif len(sys.argv) != 3:
        print("smula, spatny pocet argumentu")
        sys.exit(1)
    return print("test prošel, jedeme dál")

# Vyjimka ze zpracovani
def vyjimka(url: str):
    if url == "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6202":
        print("pro 'Brno - mesto' to data nevybere, jina struktura")
        sys.exit(1)
    elif url == "https://volby.cz/pls/ps2017nss/ps36?xjazyk=CZ":
        print("pro 'Zahranici' to data nevybere, jina struktura")
        sys.exit(1)
    return

# zapis do CSV souboru
def vytvor_csv_soubor(output, obsah):
    with open(output, mode='w', newline='', encoding='UTF-8') as csvfile:
        fieldnames = obsah[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(obsah)
    return

def main():
    """
    Hlavní funkce programu, načte url okresu, stáhne html stránky, vybere volební výsledky
    a uloží je do výstupního csv souboru.
    Vyžaduje 2 argumenty ke spuštění, první - "url stranky", druhý -  název výstupního csv souboru
    (Př. spuštění z příkazové řádky:
    python script.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' vystup_Prostejov.csv
    """
    test_vstupu()
    url = sys.argv[1]
    vyjimka(url)
    output_file = sys.argv[2]
    out = priprav_vystup(url)
    vytvor_csv_soubor(output_file, out)
    return print(f"HOTOVO, vysledky jsou v {output_file}")


if __name__ == "__main__":
    main()