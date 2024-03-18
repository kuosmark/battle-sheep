# Vaatimusmäärittely

## Yleistä

Opiskelen tietojenkäsittelytieteen kandiohjelmassa.

Käytän projektissa ohjelmointikielenä Pythonia. Vertaisarvioinnin vaatimalla tasolla hallitsen myös Javan, JavaScriptin ja TypeScriptin.

## Vaatimukset

Tarkoituksena on toteuttaa Battle Sheep -lautapeli sääntöjen mukaan toimiva peli, jota voi pelata graafisella käyttöliittymällä tekoälyä vastaan.

Ohjelma antaa pelaajan valita siirtonsa käyttöliittymään piirretyltä pelilaudalta, ja odottaa sitten tekoälyn siirtoa. Algoritmi laskee tekoälyn siirron, joka sitten näytetään pelaajalle. Peli päättyy, kuten lautepelikin, kun siirtoja ei ole enää mahdollista tehdä. Ohjelma ilmoittaa pelaajan ja tekoälyvastustajan pisteet sekä ilmaisee voittajan.

Projektin laajuuden rajaamiseksi pelilaudan rakentamista ei toteuteta, vaan peli pelataan joka kerta samanlaisella, geneerisellä laudalla.

## Suunniteltu ratkaisu

Ratkaisussa käytetään minimax-alrogitmia alfa-beta-karsinnalla tehostettuna. Kunkin hetken pelitilanne talletetaan hajautustauluun. Tekoälyn vuorolla algoritmi laskee tulevista siirroista puun aloittaen nykyisestä pelitilanteesta, ja lisäten puuhun solmuiksi ensin kaikki mahdolliset tekoälyn siirrot, sitten niiden lapsiksi kaikki mahdolliset niitä seuraavat pelaajan siirrot ja niin edelleen. Tätä tehdään tiettyyn syvyyteen asti. Lehtisolmut käydään läpi heuristisen funktion avulla, joka arvioi tilanteiden suosiollisuutta tekoälylle. Näistä minimax-algoritmi laskee parhaan mahdollisen seuraavan siirron. Alfa-beta-karsinta tehostaa merkittävästi algoritmin suoritusta karsien puun läpikäytäviä oksia.

## Ongelman ydin

Harjoitustyön ydin on parhaan pelitilanteen laskevan minimax-algoritmin toteutuksessa sekä sen heuristisessa funktiossa, joka arvioi eri pelitilanteiden suosiollisuutta osapuolille.

## Jatkokehitys

Kiinnostavia jatkokehitysaihioita olisi esimerkiksi pelilaudan muokkausmahdollisuus ja tekoälyvastustajan vaikeustason valinta (vaikeampi vastustaja kykenisi laskemaan siirtoja pidemmälle).

## Lähdeviitteet