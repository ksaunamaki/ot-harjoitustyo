# Käyttöohje

## Hae tiedostot

Voit ladata ZIP tai TAR.GZ -tiedostona [viimeisimmän julkaistun version](https://github.com/ksaunamaki/ot-harjoitustyo/releases) joka on purettavissa levylle (Releases / Assets). 

Vaihtoehtoisesti voit kloonata repositoryn suoraan git:llä haluaamaasi hakemistoon. Tällöin saat kuitenkin viimeisimmän tilanteen pelin lähdekoodeista joka ei välttämättä vastaa viimeisintä julkaistua versiota!

## Pelin käyttöönotto & konfigurointi

### Käyttöönotto (kertaluontoisesti)

Planesweeper -peli ei oletuksena tarvitse mitään erityisiä muita konfigurointitoimenpiteitä, kunhan koneelta löytyy Python3 ja Pythonin Poetry on asennettu.

Kertaluontoisesti Poetryn avulla tulee ajaa pelin päähakemistossa **poetry install** komento:

_poetry install_

### Konfigurointi

Halutessasi voit koska tahansa vaihtaa pelin kieltä (englanti / suomi) komentoriviltä ajamalla:

_poetry run invoke configure --setlang=fi_

Huomaa että käynnissä oleva peli _ei_ huomaa tätä muutosta, vaan se tulee sulkea ja ajaa em. komento ja käynnistää peli sitten uudelleen.

Mikäli olet jo aiemmin pelannut peliä ko. hakemistosta ja haluat nollata tuloslistat, voit palauttaa pelin asetukset oletustilaan sekä tyhjentää tuloslistat ajamalla:

_poetry run invoke reset_

## Pelin käynnistys

Peli on käynnistettävissä seuraavalla komennolla:

_poetry run invoke start_

## Kuinka pelaan?

Planesweeper - tai Tutkapinta suomeksi - peli perustuu klassiseen miinaharava-peliin. Pelin perusideana on selvittää kenttä jossa on X x Y suljettua ruutua riippuen peltasosta, ja joiden alta löytyy - myös tasosta riippuen - tietty määrä lentokoneruutuja. 

Kentän selvittäminen onnistuneesti edellyttää että et osu yhteenkään lentokoneruutuun vaan, itseasiassa, merkitset ne tutkamerkillä ja avaat kaikki _muut_ ruudut. Suljettu ruutu avataan hiiren vasemmalla (l. ensisijaisella) napilla ja ruutu taas merkitään tutkamerkinnällä hiiren oikealla (l. toissijaisella) nappulalla kun hiiren osoitin on ruudun päällä. Kun ruutu on merkitty tutkamerkinnällä, sitä ei voi enää vahingossakaan avata klikkaamalla vasemmalla nappulalla - mutta merkitty ruutu voidaan kuitenkin palauttaa takaisin suljetuksi ja merkitsemättömäksi ruuduksi klikkaamalla sitä uudelleen oikealla nappulalla.

Jos vahingossa avaat ruudun jonka alta löytyykin lentokone, peli päättyy (yksittäispeli) ja olet hävinnyt pelin.

Suljettu ruutu: ![](../src/assets/unopened-25.png)

Tutkamerkintä: ![](../src/assets/radar-25.png)

Lentokone: ![](../src/assets/plane-25.png)

### No mutta mistä sitten _tiedän_ mitkä ovat lentokoneruutuja?

Alussa sitä ei tiedäkään, vaan pelaaminen pitää aloittaa avaamalla _joku_ ruuduista. Mutta ei huolta, peli ei koskaan sijoita lentokoneruutua ensimmäiseen avattuun ruutuun vaan ensimmäinen avattu ruutu taataan olevan jokin muu mahdollisista ruuduista.

Kun sinulla on auki yksi tai useampi ruutu, voi aloittaa seuraavien avattavien (tai merkattavien) ruutujen päättelyn käyttämällä vihjeenä ruudusta löytyviä numeroita:

![](../src/assets/number_1-25.png) ![](../src/assets/number_2-25.png) ![](../src/assets/number_3-25.png) ![](../src/assets/number_4-25.png) ![](../src/assets/number_5-25.png) ![](../src/assets/number_6-25.png) ![](../src/assets/number_7-25.png) ![](../src/assets/number_8-25.png)

Jokainen lantokoneruutu aiheuttaa sen vieressä olevien ruutujen osalta sen että niissä on numero, joka kertoo kuinka monta lentokonetta kyseisen ruudun naapureina on. Ruudullahan voi olla (reunaruutuja lukuunottamatta) enintään kahdeksan naapuriruutua joten avatusta ruudusta voi löytyä siis numerot yhdestä kahdeksaan - tai sitten ihan tyhjä ruutu joka tarkoittaa että kyseisellä ruudulla ei ole yhtään lentokonetta naapurinaan. Jos avaat kokonaan tyhjän ruudun, peli myös automaattisesti avaa kaikki sen viereiset muut tyhjät ruudut aina siihen asti että vastaan tulee numeroruutuja.

Kun saat numeroruudun, sinun täytyy päätelllä sekä sen että muiden vieressä olevien numeroruutujen perusteella loogisin sijainti lentokoneruudulle, merkata se ja edetä näin avaten loppuun.

## Pelitilat

Planesweeper pelissä on toteutettuna kaksi pelitilaa:

**Yksittäispeli** joka käynnistyy aloitusruudusta ylemmästä valinnasta _tai_ koska tahansa painamalla ALT+S (käynnissä oleva peli keskeytyy välittömästi ja uusi peli aloitetaan). 

Koska yksittäispelissä pelataan vain yksi pelikenttä, sen läpäiseminen tai epäonnistuminen päättää senhetkisen pelin. Yksittäispelin osalta voi vapaasti myös valita pelin vaikeustason, eli pienemmän tai isomman kentän koon ALT+1 - ALT+6 näppäinyhdistelmillä.

Pelaamisen aloitus (eli ensimmäisen ruudun avaus) käynnistää pelikellon ja mikäli läpäiset kentän ja olet viiden nopeimman pelaajan joukossa (per pelitaso), pääset antamaan nimikirjaimesi (kolme kirjainta) tuloslistalle.

**Haastepeli** jossa sinun tulee pelata läpi kaikki kuusi vaikeustasoa alkaen ensimmäisestä ja edeten viimeiseen.

Tason kentän selvittäminen onnistuneesti kasvattaa vaikeustasoa ja kenttää yhdellä, kun taas lentokoneeseen osuminen ei päätä peliä vaan antaa sinun yrittää kenttää uudelleen (uusilla lentokonesijainneilla!).

Koska haastepelissä voi kestää kauankin läpäistä kaikki kuusi tasoa, tuloslistalle pääsemiseksi pitää nopeimman ajan sijasta saada _eniten pisteitä_ ja viisi suurinta pistemäärää muodostavat tuloslistan. 

Jokaisen tason läpäisy kasvattaa kerättyjä pisteitä kentän ruutujen määrällä (eli esim. 9x9 kokoisessa kentässä pisteitä tulee läpäisyn yhteydessä 81) - mutta jokainen epäonnistunut läpäisy-yritys _vähentää pisteitä yhdellä_! Lisäksi, mikäli lentokoneeseen osuu peräkkäin 10% tason ruutujen kokonaismäärästä (eli em. 9x9 kokoisessa kentässä kahdeksan kertaa) peli tiputtaa takaisin edelliselle tasolle - poislukien tietysti ensimmäinen taso jota voi yrittää kuinka monta kertaa vain.