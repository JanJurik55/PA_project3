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
        td_elem = elem.find_all("td")
        if not elem.find("td", ({'class': "cislo"})):
            continue
        else:
            misto_id = td_elem[0].text
            misto_rel_link = td_elem[0].find("a").get("href")
            misto = td_elem[1].text
            misto_link = prefix + misto_rel_link
            output.append((int(misto_id), misto, misto_link))
    return output
def ziskej_seznam_statu(soup) -> list:
    '''
    Vyber seznamu statu a jejich url pro vysledky ze zahranici
    '''
    prefix = "https://volby.cz/pls/ps2017nss/"
    output = []
    for elem in soup.find_all("tr"):
        if not elem.find("td") or not elem.find(headers='s2'):
            continue
        country = elem.find(headers='s2').text
        if not elem.find(rowspan='1', headers='s2'):
            url_rel = elem.find(headers='s2').a['href']
        else:
            url_rel = elem.find(headers='s4').a['href']
        url = prefix + url_rel
        country_id = ziskej_country_number(url_rel)
        output.append((country_id, country, url))
    return output

def ziskej_country_number(text):
    cislo = [int(cast.split('=')[1]) for cast in text.split('&') if 'xzeme' in cast][0]
    return cislo

def priprav_vystup(seznam_odkazu):
    """
    připraví požadované volební výsledky pro daný seznam mist
    :param url: string, url odkaz (Př. https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103)
    :return: list slovniků
    """
    output = []
    for misto in seznam_odkazu:
        print(misto[1])
        soupis = {}
        soupis["code"] = misto[0]
        soupis["location"] = misto[1]
        soupis.update(ziskej_volebni_vysledky(nacti_html_stranku(misto[2])))
        output.append(soupis)
    return output

# otestuj vstup
def test_vstupu():
    url = sys.argv[1]
    if "ps311" in url or "ps361" in url:
        print(f" spatny odkaz, jiny sloupec")
        sys.exit(1)
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
        print("pro 'Brno - mesto' zmena url")
        url = "https://volby.cz/pls/ps2017nss/ps34?xjazyk=CZ&xkraj=11&xobec=582786"
    return url

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
    url = vyjimka(sys.argv[1])
    output_file = sys.argv[2]
    if url == "https://volby.cz/pls/ps2017nss/ps36?xjazyk=CZ":
        out = priprav_vystup(ziskej_seznam_statu(nacti_html_stranku(url)))
    else:
        out = priprav_vystup(ziskej_seznam_mist(nacti_html_stranku(url)))
    vytvor_csv_soubor(output_file, out)
    return print(f"HOTOVO, vysledky jsou v {output_file}")


if __name__ == "__main__":
    main()