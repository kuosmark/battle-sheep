# Testausraportti

![Ohjelman testikattavuusraportti](/dokumentaatio/kuvat/testikattavuus.png "Ohjelman testikattavuusraportti")

Käyttöliittymäluokkaa lukuunottamatta kaikkien luokkien testikattavuus on lähes 100%, ja jokainen olennainen metodi on testattu.

Kaikki testit menevät läpi.

Testejä on yhteensä 65, joista monet sisältävät useita testitapauksia. Pasture- ja Game-luokkien testeissä todennetaan, että metodit palauttavat oikeat arvot tai muuttavat pelitilannetta odotetulla tavalla. Game-luokan testeissä todistetaan, että kokonaisten vuorojen pelaaminen sekä peruminen toimii, ja että peli päättyy odotetusti.

Olennaisimmat testit algoritmin oikeanlaisen toiminnan varmistamiseksi löytyvät tiedostosta `src/tests/minimax_test.py`. Testeissä todistetaan, että pelitilanteen arvo lasketaan odotetulla tavalla, ja algoritmi valitsee seuraavaksi siirroksi sen, jonka heuristinen arvo on joko korkein tai matalin.

Heuristiikan toimivuus todistetaan sillä, että heuristiikan perusteella parhaan siirron valitseva pelaaja voittaa aina vastustajan, joka valitsee arvoltaan huonoimman siirron.

Viimeksi testeissä todetaan, että eri laskentasyvyyksiä käyttävä minimax-algoritmi voittaa pelin aina kun se löytää voittavan siirron laskentasyvyydeltään. Testit on kirjoitettu käyttäen laskentasyvyyksiä 1-5.

Testeissä käytetään oikeaa peliä pienempää pelilaudan kokoa, jossa on 4x4 laidunta. Ajoin testit myös pelissä käyttämälläni 8x4 kokoisella laudalla - lukuunottamatta laskentasyvyyden 5 testejä. Suorituksessa kesti 17 minuuttia 28 sekuntia, mutta kaikki tapaukset menivät läpi. (Testi myös osoittaa, että laskentasyvyyttä 4 käyttävän vastustajan kanssa on mahdollista otella, sillä testeissä pelattiin kokonainen peli myös tuolla syvyydellä.)

Testaus on toistettavissa ajamalla komento `poetry run pytest src/` sekä muokkaamalla tiedoston `src/tests/minimax_test.py` muuttujien _BOARD_HEIGHT_ ja _BOARD_WIDTH_ arvoja.
