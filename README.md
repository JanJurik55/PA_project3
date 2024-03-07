# PA_project3 - Election Scraper 
3. projekt v rámci ENGETO Python Akademie

## Popis projektu:
Cílem projektu bylo vytvořit program k získání výsledků parlamentních voleb z roku 2017 (https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) pro libovolný územní celek na úrovni okresů.

## Požadavky:

Pro instalaci knihoven je vhodné používát virtualní prostředí.
Vytvořte pomocí příkazové řádky ve složce vašeho projektu. Jako příklad je název prostředí „myvenv“:

    python.exe -m venv myvenv 
Prostředí je potřeba ještě aktivovat pomocí skriptu activate:

    .\myvenv\Scripts\activate

Seznam použitých knihoven je v souboru requirements.txt. Následujícím příkazem se stáhne a nainstalují veškeré knihovny potřebné ke spuštění programu.

    pip install -r requirements.txt

## Spuštění programu:
Program se spouští z příkazového řádku a vyžaduje povinně dva argumenty. 
První je URL vybraného územního celku, jehož volební výsledky chcete. 
Druhým argumentem je název výstupního CSV souboru, do kterého se výsledky uloží.

### Příklad pro spuštění: (územní celek Prostějov)
1. argument: 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' - uvozovky jsou povinně 

2. argument: vystup_Prostejov.csv


    python script.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' vystup_Prostejov.csv

### Výstupní csv soubor obsahuje:

    code,location,registered,envelopes,valid,Občanská demokratická strana,...
    506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
    589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
    589276,Bílovice-Lutotín,431,279,275,13,0,0,32,0,8,40,1,0,4,0,0,30,0,3,83,0,0,22,0,0,0,1,38,0
    ...

