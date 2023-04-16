# Planesweeper

Planesweeper on mukaeltu toteutus klassisesta Minesweeper -pelistä, jossa on tarkoitus etsiä tutkapinnalta l. maailmankartalta lentokoneita ja merkitä niitä tutkahavaintoina kunnes kaikki lentokoneet on tunnistetty. 

Pelialue koostuu vaikeustason mukaan kooltaan kasvavista ruudukoista, joista pelaaja avaa yksi kerrallaan ruutuja vasemmalla hiirennapilla ja saa numerovihjeitä kuinka monessa viereisessä ruudussa on lentokone tai -koneita. Mikäli pelaaja avaa ruudun jossa on lentokone, peli päättyy. Numeroruutujen vihjeiden mukaan päättelemällä  pelaaja voi merkitä oletetut lentokoneruudut painamalla oikealla hiirennapilla, jolloin ruutu lukittuu tutkakontaktiksi. Pelin voittaa merkitsemällä kaikki lentokoneruudut tutkakontaktilla ja avaamalla kaikki muut ruudut.

Peli toteutetaan harjoitustyönä osana Helsingin yliopiston kevään 2023 tietojenkäsittelytieteen Ohjelmistotekniikka -kurssia ajalla maaliskuu-toukokuu 2023.


## Tekniset vaatimukset

Pelisovellus on toteutettu Python ohjelmointikielen 3.10 versiolla ja se edellyttää Pythonin [Poetry](https://python-poetry.org/) kirjaston version 1.4.0 (tai uudempi) asennusta em. Pythonin version osalta koneelle pelin paketinhallintaa varten. 


## Dokumentaatio

- [Määrittelydokumentti](https://github.com/ksaunamaki/ot-harjoitustyo/blob/master/planesweeper/dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuuri](https://github.com/ksaunamaki/ot-harjoitustyo/blob/master/planesweeper/dokumentaatio/arkkithtuuri.md)
- [Työaikakirjanpito](https://github.com/ksaunamaki/ot-harjoitustyo/blob/master/planesweeper/dokumentaatio/tuntikirjanpito.md)
- [Changelog](https://github.com/ksaunamaki/ot-harjoitustyo/blob/master/planesweeper/dokumentaatio/changelog.md)

## Asennus / käyttöönotto

Kun repository on kloonattu haluamaasi hakemistoon, suorita pakettien asentaminen Poetry:a käyttäen seuraavalla komennolla **planesweeper -hakemistossa**:

```bash
poetry install
```

Kun Poetry on onnistuneesti asentanut tarvittavat paketit, voi pelin käynnistää seuraavalla komennolla:

```bash
poetry run invoke start
```

Vaihtoehtoisesti voit siirtyä terminaalista Poetryn kontekstiin ja käynnistää pelin suoraan ajamalla srv/game.py tiedoston seuraavilla komennoilla (korvaa tarvittaessa *python3* -> *python* riippuen koneesi Python asennuksesta):

```bash
poetry shell
python3 src/game.py
```

## Testaaminen

Mikäli haluat tehdä muutoksia, [Pytestilla](https://docs.pytest.org/) toteutetut automaattiset testit löytyvät repositoryn **src/tests** hakemistosta. Testikattavuusraportti on konfiguroitu [Coveragen](https://coverage.readthedocs.io) avulla. Molemmat paketit ovat projektissa hallittu edelläkuvatun Poetryn avulla.

Voi ajaa testit **planesweeper -hakemistosta** käsin seuraavalla komennolla:

```bash
poetry run invoke test
```

Coverage -raportin voi generoida **htmlcov** -hakemistoon seuraavalla komennolla:

```bash
poetry run invoke coverage-report
```

*Huom: automaattisten testien määrä ja testikattavuus repositoryssa ei toistaiseksi ole kovin korkealla tasolla!* Testejä ja testikattavuutta lisätään kurssin kuluessa.

## Kysymyksiä?

Voit ottaa yhteyttä tekijään sähköpostilla [kalle.saunamaki@helsinki.fi](mailto:kalle.saunamaki@helsinki.fi).

## Attributions

**Game background image**: [Image by starline](https://www.freepik.com/free-vector/minimal-world-map-isolated-white-background-with-shadow_37148820.htm) on Freepik
