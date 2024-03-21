# Vaatimusmäärittely

## Yleistä

Opiskelen tietojenkäsittelytieteen kandiohjelmassa.

Käytän projektissa ohjelmointikielenä Pythonia. Vertaisarvioinnin vaatimalla tasolla hallitsen myös Javan, JavaScriptin ja TypeScriptin.

## Vaatimukset

Tarkoituksena on toteuttaa Battle Sheep -lautapeli sääntöjen mukaan toimiva peli, jota voi pelata graafisella käyttöliittymällä tekoälyä vastaan.

Ohjelma antaa pelaajan valita siirtonsa käyttöliittymään piirretyltä pelilaudalta, ja odottaa sitten tekoälyn siirtoa. Algoritmi laskee tekoälyn siirron, joka sitten näytetään pelaajalle. Peli päättyy, kuten lautepelikin, kun siirtoja ei ole enää mahdollista tehdä. Ohjelma ilmoittaa pelaajan ja tekoälyvastustajan pisteet sekä ilmaisee voittajan.

Projektin laajuuden rajaamiseksi toteutetaan ainoastaan kaksinpeli yhden tekoälyvastustajan kanssa. Myöskään pelilaudan rakentamista ei toteuteta, vaan peli pelataan joka kerta samanlaisella, geneerisellä laudalla.

## Suunniteltu ratkaisu

Ratkaisussa käytetään minimax-alrogitmia alfa-beta-karsinnalla tehostettuna. Kunkin hetken pelitilanne talletetaan hajautustauluun. Tekoälyn vuorolla algoritmi kokoaa tulevista siirroista puun, aloittaen nykyisestä pelitilanteesta, ja lisäten puuhun solmuiksi ensin kaikki mahdolliset tekoälyn siirrot, sitten niiden lapsiksi kaikki mahdolliset pelaajan seuraavat siirrot ja niin edelleen. Tätä tehdään tiettyyn syvyyteen asti. Lehtisolmut käydään läpi heuristisen funktion avulla, joka arvioi tilanteiden suosiollisuutta tekoälylle. Näistä minimax-algoritmi laskee parhaan mahdollisen seuraavan siirron. Alfa-beta-karsinta tehostaa merkittävästi algoritmin suoritusta karsien puun läpikäytäviä oksia.

Ratkaisussa alogritmin läpikäymiä siirtoja ei järjestetä karsinnan optimoimiseksi, joten algoritmin aikavaativuus on pahimmassa tapauksessa sama kuin tavanomaisella minimax-algoritmilla eli $O(m^{d}$), ja tilavaativuus $O(md)$, jossa $m$ on sallittujen siirtojen määrä ja $d$ puun enimmäissyvyys. Käytännössä alfa-beta-karsinta yleensä nopeuttaa vaihtoehtojen läpikäyntiä huomattavasti.

## Ongelman ydin

Harjoitustyön ydin on parhaan pelitilanteen laskevan minimax-algoritmin toteutuksessa sekä sen heuristisessa funktiossa, joka arvioi eri pelitilanteiden suosiollisuutta osapuolille.

## Jatkokehitys

Kiinnostavia jatkokehitysaihioita olisi esimerkiksi pelilaudan muokkausmahdollisuus, tekoälyvastustajan vaikeustason valinta (vaikeampi vastustaja kykenisi laskemaan siirtoja pidemmälle) ja kolmin- tai nelinpeli useamman tekoälyvastustajan kanssa.

## Lähteet

Alpha–beta pruning. Wikipedia. Viitattu 20.3.2024. https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

Minimax. Wikipedia. Viitattu 20.3.2024. https://en.wikipedia.org/wiki/Minimax

Vasileios Megalooikonomou. 2003. CIS603 S03. Temple University Department of Computer & Information Sciences. https://cis.temple.edu/~vasilis/Courses/CIS603/Lectures/l7.html
