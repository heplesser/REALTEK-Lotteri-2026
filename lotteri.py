#!/usr/bin/env python

"""
Skript for gjennomføring av REALTEKs Stipendiatlotteri 2026.

Skriptet kjøres direkte fra kommandolinjen som

    ./lotteri.py deltakere.txt

Filen `deltakere.txt` skal inneholde navn til lotterideltakerne, ett navn per linje.
Tomme linjer ignoreres.

Dato som skal benyttes for å innhente valutakursdata og dekanens tall må legges inn
og bekreftes før trekningen gjennomføres.

Programmet skriver ut noe informasjon først og så navnet til vinneren.

Hans Ekkehard Plesser, NMBU, Februar 2026
"""


# Vi benytter kode for produksjon av slumptall som følger med Python.
# For dokumentasjon, se https://docs.python.org/3/library/random.html.
# Den benytter Mersenne Twister 19937 som underliggende generator.
import random


# Vi benytter et bibliotek for å innhente data fra Norges banks nettside.
# For dokumentasjon se https://docs.python-requests.org/en/latest/index.html
import requests

from matplotlib.pyplot import pause
import sys


def main(ticket_file):
    """
    Gjennomfør lotteriet når programmet kjøres som beskrevet ovenfor.

    Se helt i slutten av filen for koden som kaller denne funksjonen og så starter lotteriet.

    ticket_file - navn på filen som inneholder navnene på dem som er med i lotteriet
    """

    try:
        # Les navnene fra fil, fjern mellomrom på starten eller slutten av linjene samt tomme linjer
        tickets = [name_stripped for name in open(ticket_file, "r")
                   if (name_stripped := name.strip())]
    except IOError:
        print(f"Kunne ikke lese filen {ticket_file}.")
        sys.exit(1)
    num_tickets = len(tickets)

    WIDTH = 60
    W_LEFT = len("Startverdi         : ")
    W_RIGHT = WIDTH - W_LEFT
    
    print()
    print("*" * 60)
    print(f"{'REALTEK Stipendiatlotteri 2026':^{WIDTH}}")
    print("*" * 60)
    print()
    pause(2)
    print(f"{num_tickets:2d} deltakere : {tickets[0]}")
    for deltaker in tickets[1:]:
        print(" " * (W_LEFT-6) + deltaker)
        pause(0.2)
    print()
    print("*" * 60)
    print()
    data_bekreftet = "nei"
    while data_bekreftet != "JA":
        dato = input("Referansedato   : ")
        print()
        dekanens_tall = input("Dekanens tall   : ")
        print()
        print(f"Dato for startverdi: {dato}")
        print(f"Dekanens tall      : {dekanens_tall}")
        print()
        data_bekreftet = input("Er disse data korrekte [JA/nei]? ")
        print()

    # Vi kjører lotteriet allerede nå her. Det gjør det en smule enklere å teste koden
    # i funksjonen lotteri().
    startverdi, vinner = lotteri(tickets, dato, dekanens_tall)
    svsplit = [startverdi[i:i+W_RIGHT] for i in range(0, len(startverdi), W_RIGHT)]

    print("*" * 60)
    print()
    print("Trekningen gjennomføres med")
    print()
    print(f"Pythonversjon      : {sys.version.split(" ")[0]}")
    print(f"Dato for startverdi: {dato}")
    print(f"Dekanens tall      : {dekanens_tall}")
    print(f"Startverdi         : {svsplit[0]}")
    for s in svsplit[1:]:
        pause(0.5)
        print(f"{' ':{W_LEFT}}{s}")
    print()
    print("*" * 60)
    print()
    print("Trekningen pågår ", end="")
    for _ in range(7):
        print(".", end="", flush=True)
        pause(1)
    print("\n")

    pause(2)
    print("*" * 60)
    print()
    print("Stillingen går til ", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        pause(1)
    print(f" {vinner}")
    print()
    print("*" * 60)
    print()
    print()
  

def lotteri(tickets, dato, dekanens_tall):
    """
    Trekk vinneren fra loddene (tickets) med gitt dato for konstruksjon av startverdiene for slumptallsgeneratoren.

    tickets       - liste med navn; hvert navn må forekomme bare en gang og har lik sjanse til å vinne
    dato          - dato i format yyyy-mm-dd som må være et dato der valutakurser ble publisert av Norges bank
    dekanens_tall - må være en streng, skjøtes på teten av startverdien generert fra valutakursene

    Returnerer startverdien brukt og vinnerens navn
    """

    assert len(tickets) == len(set(tickets)), "Noen navn forekommer mer enn en gang"

    # Selve lotteriet
    startverdi = dekanens_tall + valutadata_sammensatt(dato)
    random.seed(startverdi)

    num_tickets = len(tickets)
    winner_index = random.randint(1, num_tickets)
    winner_name = tickets[winner_index - 1]

    return startverdi, winner_name


def valutadata_sammensatt(dato):
    """
    For gitt dato i format YYYY-MM-DD, lag skjøt valutakursene fra Norges banks valutadata.
    """

    VALUTA = ['AUD', 'BDT', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 
              'HKD', 'HUF', 'I44', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MMK', 
              'MXN', 'MYR', 'NZD', 'PHP', 'PKR', 'PLN', 'RON', 'SEK', 'SGD', 'THB', 
              'TRY', 'TWD', 'TWI', 'USD', 'VND', 'XDR', 'ZAR']

    # Bygg URL som etterspør data for gitt dato og alle kurs i VALUTA fra Norges bank. 
    # Se følgende for oppbygging av forespørselen
    # https://app.norges-bank.no/query/index.html#/no/currency?frequency=B&startdate=2026-01-30&stopdate=2026-01-30    
    url = f"https://data.norges-bank.no/api/data/EXR/B.{'+'.join(VALUTA)}.NOK.SP?format=sdmx-json&startPeriod={dato}&endPeriod={dato}&locale=no"

    # Send forespørsel og kontroller at vi fikk en gyldig respons
    response = requests.get(url)
    if not response.ok:
        raise RuntimeError(f"Kunne ikke innhente data for {dato}.")

    # Svaret inneholder kursdata i en dypt nøstet struktur. Rekkefølgen valutadata kommer i, er ikke
    # den alfabetiske rekkefølgen vi sendte inn med URLen. Vi henter nå ut valutakodene og -verdiene.
    data = response.json()["data"]
    valutakoder = list(l['id'] for l in data['structure']['dimensions']['series'][1]['values'])
    valutaverdier = [o['observations']['0'][0] for o in data['dataSets'][0]['series'].values()]

    # Sjekk at vi fikk data for alle valuta vi har forespurt
    if len(valutakoder) != len(VALUTA):
        raise RuntimeError(f"Bare {len(valutakoder)} valutakoder mottatt, forventet {len(VALUTA)}.")
    if len(valutaverdier) != len(VALUTA):
        raise RuntimeError(f"Bare {len(valutaverdier)} valutaverdier mottatt, forventet {len(VALUTA)}.")

    # Sorter valutadata alfabetisk etter valutakodene for å sikre reproduserbarhet
    valuta_alfabetisk = {k: v for k, v in sorted(zip(valutakoder, valutaverdier))}

    # Lag og gi tilbake en lang streng sammensatt av alle kursverdiene, med desimalpunkter fjernet
    return ''.join(valuta_alfabetisk.values()).replace('.', '')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Brukes som ./lotteri.py deltakerfil")
        sys.exit(2)

    main(sys.argv[1])
