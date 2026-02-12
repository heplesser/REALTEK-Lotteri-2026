# Loddtrekning for stipendiatstillinger

#### Hans Ekkehard Plesser, 2026-02-12

Etter tilrådning fra Forskningsutvalget har dekanen bestemt at den ledige stipendiatstillingen ved REALTEK skal tildeles via loddtrekning. Loddtrekningen skal gjennomføres elektronisk. Hvert lodd tilsvarer navnet til en mulig hovedveileder og alle mulige hovedveiledere skal ha lik sannsynlighet for å bli valgt ut ved loddtrekning.

## Gjennomføring av elektronisk loddtrekning

Navnene til alle ansatte som har fått tildelt lodd legges inn i en liste i den rekkefølgen de står oppført i listen over loddene som er publisert på intranett. Så trekkes et slumptall mellom 1 og listens lengde og det velges det navnet som står på tilsvarende plass på listen. Til dette finnes det egnede algoritmer som sikrer likefordeling av resultatene. Det er viktig å sikre at loddtrekningen (a) skal være etterprøvbart og (b) skal være uforutsigbart og ikke manipulerbart. 

Datamaskiner benytter slumptallsgeneratorer til å produsere tilfeldige resultater, slik som f eks trengs til loddtrekningen (se f eks Plesser, 2010). Slumptallsgeneratorer er deterministiske algoritmer: Startes de med en gitt startverdi, produserer de akkurat de samme "tilfeldige" tall hver gang de kjøres. Dette sikrer etterprøvbarheten, men resultatene er dermed forutsigbare. 

### Valg av startverdi

For å sikre utforutsigbarhet må derfor startverdien velges på en måte som (a) er etterprøvbart, (b) er utforutsigbart og (c) ikke kan manipuleres. For et eksempel på en slik løsning se avsnitt 3 av Marsaglia og Tsang (2004).

Metoden som foreslås her er inspirert av Marsaglia og Tsang. Som kilde av uforutsigbare og ikke manipulerbare startverdier benyttes valutakurser publisert daglig av [Norges bank](https://www.norges-bank.no/tema/Statistikk/Valutakurser/?tab=all). Så lenge dagen for trekningen er fastsatt i forkant, vil valutakursene på dagen før trekningen være ukjente og ikke manipulerbare tall. Valutakursene hentes inn, sorteres alfabetisk etter valutakoden og skjøtes sammen til en lang streng. Desimalpunktene fjernes, siden disse endrer seg aldri. Dermed ender man opp med en streng på ca 180 tegn som brukes som startverdi for slumptallsgeneratoren.

En liten ulempe ved bruk av valutakursene er at enhver kan finne resultatet for trekningen som skal finne sted på en gitt dag straks kursene publiseres dagen før. For å sikre et overraskelsesmoment brukes i tillegg *dekanens tall*: Noen dager før trekningsdatoen skriver dekanen et tall på minst fire siffer og forsegler dette i en konvolutt. Under trekningen åpnes konvolutten og dekanens tall legges til startverdien som en streng.

## Bakgrunnsmateriale og kode for loddtrekningen

Dette kodearkivet inneholder filene
- `lotteri.py` med koden som gjennomfører selve lotteriet
- `sjekk_koden.ipynb` med en statistisk test for koden som bygger startverdien
- `deltakere_test.txt` et eksempelfil med deltakernavn for prøvekjøring av koden


#### Referanser

- Marsaglia, G., & Tsang, W. W. (2004). The 64-bit universal RNG. Statistics & Probability Letters, 66, 183–187. https://doi.org/10.1016/j.spl.2003.11.001
- Plesser, H. E. (2010). Generating Random Numbers. In S. Grün & S. Rotter (Eds.), Analysis of Parallel Spike Trains (pp. 399–411). Springer US. https://doi.org/10.1007/978-1-4419-5675-0_19 (Ta kontakt for en reprint, teksten er dessverre ikke open access.)
