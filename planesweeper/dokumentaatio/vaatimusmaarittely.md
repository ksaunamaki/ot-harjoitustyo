# Vaatimusmäärittely

## Sovelluksen kuvaus

Toteutettava sovellus on tietokonepeli, joka on muunneltu toteutus klassisesta Miinaharava -pelistä. Toteutettavassa pelissä miinojen sijasta etsitään tutkakontakteja lentokoneista ja pelialueen (ruutujen) taustana toimii maailmankartta. 

Pelin perustoimintalogiikkana on "avata" yksittäisiä ruutuja (vasen hiiren näppäin) ja päätellä alla olevien numeroiden kautta missä vielä avaamattomissa ruuduissa ovat lentokoneet, jotka tulee merkitä tutkakontaktimerkinnällä (oikea hiiren näppäin) kunnes kaikki valittuun vaikeustasoon kuuluvat koneet on tunnistettu ja kaikki muut ruudut on avattu. Mikäli ruudun avaa ja sieltä paljastuukin lentokone, on pelikierros päättynyt epäonnistumiseen.

## Käyttäjät

Koska sovellus on peli, erityisiä käyttäjärooleja ei sovelluksessa ole vaan ainoa käyttäjä on pelin interaktiivinen pelaaja.

## Perustoiminnallisuudet

Pelissä on toteutettuna seuraavat toiminnallisuudet:

- Vaihtuvakokoinen pelialue / vaikeustaso
  - Ruudukon koko sekä koneiden määrä
- Kaksi pelitilaa: 
  - Satunnaispeli yksittäiseen pikapeliin vapaasti valittavalla vaikeustasolla
  - Haastepeli, jossa edetään vaikeustasojen välillä; kentän selvittämisen epäonnistuminen riittävän monta kertaa peräkkäin palauttaa aiemmalle tasolle ja läpäisy seuraavalle tasolle
- Paikalliseen tietokantaan tallennettava high-score lista
  - Pohjautuu vaikeustasoon ja pelialueen selvityksen kokonaisaikaan yksittäispelissä
  - Pohjautuu kerättyihin pisteisiin haastepelissä
- Monikielisyys käyttöliittymätekstien osalta:
  - Englanti
  - Suomi

## UI konseptikuva

![](./kuvat/ui-sketch.png)

## Lisätoiminnallisuudet

Jatkokehitysmahdollisuuksina on tunnistettuna mm. seuraavia:

- Muiden kielien tuen lisäys
- Reaaliaika-API:sta haettavat oikeiden koneiden sijainnit (esim. [Flightaware:n AeroAPI](https://flightaware.com/aeroapi//))
  - Yleisenä haasteena positio-data -API:en kanssa on ilmaisten tasojen erittäin rajoitettu hakumäärä / kk ja/tai hakutulosten määrä jotta lentokoneiden positioita saa riittävästi satunnaisuutta varten
  - Oma pelitilansa satunnaisesti arvottujen koneiden sijasta, haettujen konesijaintien joukosta arvotaan vaikeustasoon kuuluvan totaalikonemäärän mukainen määrä koneita ja jotka sijoitetaan pelialueen taustalla olevan maailmankartan mukaan oikeisiin geopositioihin
  - Jatkokehitysmahdollisuutena lisäksi API-datan osalta koneiden raportoidun sijainnin ekstrapolointi tulevaisuuteen suuntavektorin ja nopeuden perusteella
- Pelialueen animaatiot