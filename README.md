# PA_project3 - Election Scraper 
3. projekt v rámci ENGETO Python Akademie

## Popis projektu:
Cílem projektu bylo vytvořit program k získání výsledků parlamentních voleb z roku 2017 (https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) pro libovolný územní celek na úrovni okresů.

## Požadavky:
Seznam viz: requirements.txt

## Spuštění programu:
Program se spouští z příkazového řádku a vyžaduje povinně dva argumenty. 
První je URL vybraného územního celku, jehož volební výsledky chcete. 
Druhým argumentem je název výstupního CSV souboru, do kterého se výsledky uloží.

### Příklad pro spuštění: (územní celek Prostějov)
první argument: 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103'

druhý argument: vystup_Prostejov.csv

c:\muj_adresar> python script.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' vystup_Prostejov.csv
