# Toteutusraportti

## Ohjelman rakenne

Käyttöliittymäluokka `ui.py` huolehtii pelin suoritussilmukasta, pelaajan syötteiden välittämisestä peliluokalle sekä graafisen käyttöliittymän päivittämisestä.

Peliluokka `game.py` kuvaa pelitilannetta, ja sisältää metodit sen manipulointiin. Yksittäinen olio sisältää kaiken tarvittavan datan kustakin pelilaudan tilanteesta. Luokassa säilytetään listaa pelilaudan laitumista. Laitumet ovat laidunluokan `pasture.py` olioita, joissa on tallessa yksittäisen laitumen tiedot, ja metodit niiden muokkaamiseen.

Itse minimax-algoritmi `minimax.py` käsittelee peliluokan olioita. Tekoälyvastustaja (tai simulaatiossa myös "pelaaja") pyytävät minimax-funktiolta parasta seuraavaa siirtoa. Ensin käydään läpi mahdolliset seuraavat siirrot, ja talletetaan nämä pelitilanteet listaan, joka vielä järjestetään heuristiikan perusteella parhaimmasta huonoimpaan. Minimax-algoritmi kokoaa pelitilannetta seuraavia siirtoja rekursiivisesti tällä tavalla aina laskentasyvyyteen asti, minkä jälkeen se alkaa "syvimmällä" olevien siirtojen heurististen arvojen perusteella laskea parasta seuraavaa siirtoa.

Tiedostoissa `pasture.py` ja `utils.py` on muunneltua MIT-lisenssin alla ollutta koodia, jonka olen kopioinut ohjelmaani. Käytän lainattua koodia lähinnä graafisen käyttöliittymäni laidunten generointiin.

## Puutteet ja parannusehdotukset

Yksinkertaistin projektin loppuvaiheessa käyttämääni heuristiikkaa. Nyt lopullisessa versiossa se lasketaan yksinkertaisesti: pelaajan mahdolliset siirrot miinus tekoälyn mahdolliset siirrot. Minimax-algoritmi hakee pelaajan vuorolle heuristiikaltaan mahdollisimman suurta arvoa ja tekoälylle mahdollisimman pientä.

Peliä pelaamalla on kuitenkin ilmeistä, että heuristiikkaa voisi kehittää mielekkäämmän pelikokemuksen saavuttamiseksi. Nyt vastustaja saattaa "paeta" tilanteita, joissa voisi saada suuren määrän pelaajan lampaita saarrettua - laskemalla, että saa lisättyä omia seuraavia siirtojaan parhaiten siirtämällä lampaansa jonnekin pelilaudan avoimelle paikalle. Jonkinlainen painotus hyökkäämiseen voisi parantaa vastustajaa. Heuristiikan "hyvyyden" arviointi on toki haastavaa hommaa.

Toinen kehityskohde olisi algoritmin toiminnan nopeuttaminen. Tällä hetkellä laskentasyvyys 4 on korkein, jolla oma kärsivällisyyteni jaksaa odottaa vastustajan ensimmäisiä siirtoja. Kuten kerroin viikkoraportissa 6, ensimmäisellä minimax-algoritmini versiolla kesti 25,17 sekuntia tekoälyn ensisiirron tekemiseen laskentasyvyydellä 3. Nyt lopullisessa versiossa siirtojen järjestämisen, alfa-beeta-karsinnan käyttöönoton sekä koodin optimoinnin myötä tuohon siirtoon kuluu 7,25 sekuntia. Laskentasyvyydellä 4 siirtoon kuluu 186,66 sekuntia. Laskentasyvyydellä 5 jo 1313,11 sekuntia (yli 21 minuuttia). Uskon, että esimerkiksi hankkiutumalla eroon mahdollisten seuraavien siirtojen listaamisessa käyttämästäni deepcopy-metodista, voisin nopeuttaa algoritmia edelleen.

## Saavutetut aika- ja tilavaativuudet

Toisin kuin vaatimusmäärittelyssä kirjoitin, lopullisessa ratkaisussani alogritmin läpikäymät siirrot järjestetään alfa-beeta-karsinnan optimoimiseksi. Aikavaativuus on siis parhaimmillaan $O(m^{d/2})$, ja tilavaativuus $O(md)$, jossa $m$ on sallittujen siirtojen määrä ja $d$ puun enimmäissyvyys. Vaatimukset siispä saavutettiin.

Kellotin pelitilanteen tallentamisen algoritmin käyttämään listaan sekä tilanteen heuristiikan laskennan, ja sain tulokseksi pyöristettynä 0,001 sekuntia. O-analyysin perusteella voidaan siis ennustaa, että laskentasyvyydellä 3 tekoälyn siirron laskenta-aika olisi pelissäni mahdollisten siirtojen enimmäismäärällä 75 (toisella vuorolla pelaaja voi siirtää 15 lammasta enimmillään 5 eri suuntaan) parhaimmillaan $O(m^{d/2})=O(75^{3/2})=0,001s * 75^{3/2}\approx0,65s$. Pahimmillaanhan aikavaativuus alfa-beeta-karsinnan kanssa oli $O(m^{d})$ eli tässä tapauksessa $O(75^3)=0,001s * 75^3\approx421,88s$. Todellinen laskenta-aika on siis huomattavasti lähempänä parasta kuin pahinta arviota.

Saman kaavan mukaan laskentasyvyydellä 4 aika-arvio on parhaimmillaan $0,001s * 75^{4/2}=5,625s$, ja pahimmillaan $0,001s * 75^4=31640.625s$. Mittaustulos 186,66 sekuntia on siis edelleen paljon lähempänä parasta.

Syvyydellä 5 arvio on parhaimmillaan vasta $0,001s * 75^{5/2}\approx48.71s$, mutta pahimmillaan jo $0,001s * 75^5=23730468.75s$ eli peräti 274 vuorokautta. Mittaustulos 1313,11 sekuntia muistuttaa yhä selvemmin parasta arviota. Laskuharjoitus havainnollistaa myös siirtojen järjestämisen ja karsinnan päivänselvän hyödyn.

## Laajojen kielimallien käyttö

Käytin projektissa ChatGPT 4:ä joissakin tilanteissa. Pyysin siltä apua dokumentaation laatimisessa ja sanamuotojen tarkistuksessa. Hyöty tässä oli rajallista johtuen GPT:n keskinkertaisesta suomen kielen taidosta. Pyysin GPT:ltä ehdotuksia metodien optimointiin ja refaktorointiin. Suurin hyöty tekoälystä oli projektin alkuvaiheessa, kun kyselin siltä graafisesta käyttöliittymästä ja kuusikulmioiden generoimisesta. Pyysin sitä muutamaan otteeseen myös jäljittämään bugia sille tarjoamastani koodilohkosta, mutta lopulta perinteinen muuttujien tulostelu oli kuitenkin nopeampaa. On myös todettava, että tämän projektin kanssa ylipäänsä vanhat kunnon Google ja Wikipedia olivat hyödyllisempiä. Minulla oli kuherruskuukausi GPT 4:n saatuani sen ensi kertaa käyttööni, mutta tunteeni ovat nyt selvästi jo viilenneet.

## Viitteet

Alpha–beta pruning. Wikipedia. Viitattu 10.5.2024. https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

Vasileios Megalooikonomou. 2003. CIS603 S03. Temple University Department of Computer & Information Sciences. https://cis.temple.edu/~vasilis/Courses/CIS603/Lectures/l7.html
