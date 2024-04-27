# Viikkoraportti 4

Käytin neljännen viikon aikana projektiin noin 19 tuntia.

Olen aika tyytyväinen tähän viikkoon ja projektin edistymiseen. Lisäsin ohjelmalleni yksikkötestejä, ja korjasin bugeja. Sain toteutettua pelin tekoälyvastustajalle toimivan minimax-algoritmin, jolla tekoäly etsii parhaan mahdollisen siirron (ottaen huomioon mahdolliset pelitilanteet kaksi siirtoa eteenpäin). Algoritmi käyttää pelitilanteiden arviointiin toistaiseksi yksinkertaista heuristiikkaa.

Tällä hetkellä pelin voi pelata loppuun saakka kohtuullisen hyvin pelaavaa tekoälyvastustajaa vastaan. Huolimattomasti pelaamalla saattaa hyvinkin hävitä. Nyt kun olen saanut pelin kokonaisuudessaan toimimaan, on seuraava vaihe optimoida ja nopeuttaa algoritmin toimintaa, jotta voidaan laskea tulevia vuoroja pidemmälle riittävän nopeasti. Heuristiikkaa voinee parantaa, ja algoritmin toiminnan kattavaa testausta tarvitaan. Ohjelmakoodi vaatii hiomista, ja on osin vielä karkeaa. Nyt peli kuitenkin toimii, ja refaktoroinnille sekä dokumentoinnille on onneksi hyvin aikaa!

![Kuvakaappaus sovelluksesta viikon 4 päättyessä](/dokumentaatio/kuvat/viikko_4.png "Kuvakaappaus sovelluksesta viikon 4 päättyessä")

Viimeisin viikko on ollut projektin mielenkiintoisimpia. Päivätyössäni verkkosovellusten parissa pääsen harvoin toteuttamaan algoritmeja tai rekrusiivisia funktioita. Heuristiikkaa on ollut kiinnostava pohtia, sekä kokeilla erilaisia kertoimia, ja kuinka ne vaikuttavat tekoälyvastustajan siirtoihin. Suurimmat haasteet koin muutaman algoritmin toimintaa sotkeneen hankalasti havaittavan bugin kanssa.
