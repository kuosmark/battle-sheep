# Viikkoraportti 5

Käytin viidennen viikon aikana projektiin noin 26 tuntia.

Tämä oli eittämättä projektin haastavin viikko. Sain vastaani useita hankalia bugeja, joiden parissa aikaa kului rutkasti. Korjasin pelistä toimintavarmempaa ja ohjelman rakenteesta ymmärrettävämpää ja ylläpidettävämpää.

Olen sisäistänyt minimax-algoritmin ja alfa-beeta-karsinnan toiminnan. Lähdin toteuttamaan alfa-beeta-karsintaa yhdellä tavalla, mutta törmäsin suuriin haasteisiin ohjelmani toimintalogiikasta johtuen. Minun täytyikin valita uusi lähestymistapa, ja muuttaa algoritmiani niin, että jokaisessa pelitilanteessa sallitut seuraavat siirrot lisätään ensin listaan, jota algoritmi sitten käy läpi. Itse alfa-beeta-karsintaa tällä uudella lähestymistavalla en ehtinyt toteuttaa enkä ole tätä uutta versiota sovelluksesta vielä mergennyt päähaaraan. Yritän pitää repositorion päähaaran kunnossa vertaisarviointeja varten.

Tulevan viikon ja loppuprojektin aikana pyrin saamaan alfa-beeta-karsinnan toimimaan, ja varmistamaan testauksen avulla pelin toiminnan eri tilanteissa. Saamani vertaispalautteen pohjalta yritän ohjelman rakenteessa paremmin erottaa pelin käyttöliittymän ja toimintalogiikan. Uutta toiminnallisuutta ei enää ole tulossa. Jos aikaa jää, refaktoroin koodia sekä hion visuaalista puolta.
