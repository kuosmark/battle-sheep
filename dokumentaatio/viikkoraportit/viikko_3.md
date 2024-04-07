# Viikkoraportti 3

Käytin kolmannen "viikon" aikana projektiin noin 19 tuntia.

Kolmanteen palautukseen kuuluneiden viikkojen aikana rakensin pelimekaniikan toimivaksi. Pelilautaa kuvaaviin tietorakenteisiin ja siirtojen tekoon tarvittavaan logiikkaan kului merkittävästi aikaa. Jumiuduin pidemmäksi aikaa etenkin sallittujen siirtojen laskemisessa käytettäviin suuntavektoreihin.

Tällä hetkellä minulla on graafisen käyttöliittymän kautta pelattava peli, jota voi pelata satunnaisia (sääntöjen mukaisia) siirtoja tekevää "tekoälyä" vastaan. Peli päättyy kun siirtoja ei enää ole mahdollista tehdä. Peli voittajaa ei vielä lasketa tai ilmoiteta. Pelissä on bugeja, jotka hankaloittavat pelaamista. Tilanne parantunee kunhan saan kirjoitettua ykiskkötestejä.

![Kuva sovelluksesta viikon 3 päättyessä](/dokumentaatio/kuvat/viikko_3.png "Kuva sovelluksesta viikon 3 päättyessä")

Olisin näin jälkeenpäin ajatellen voinut kopioida laajemminkin koodia pelimekaniikkaa varten. Päädyin kirjoittamaan suurimman osan myös laitumien koordinaatteja laskevasta koodista itse. Toteutus ei ole optimaalinen eikä helpoin mahdollinen, mutta toimii. Työ on ollut kiinnostavaa, ja koen oppineeni paljon. Siirtojen laskemiseen heksagonaalilaudalla piti hyödyntää vektorilaskentaa, geometriaa ja Pythagorasta.

Tekeminen on ollut aiempaa organisoidumpaa, ja vähemmän poukkoilevaa. Tein ensimmäisen viikon aikana valtaosan tämän etapin työstä. Toisella viikolla en ehtinyt juurikaan edistää peliä, ja yksikkötestaaminen jäi taas seuraavaan viikkoon.

Suurin haaste on vieläkin aika, ja se, etten ole itse heuristiikkaan ja minimax-algoritmiin vieläkään kunnolla päässyt. Toisaalta olen tyytyväinen siihen, että minulla on nyt kolmen palautuksen jälkeen pohjana pelattava (vaikkakin hieman buginen) peli, johon voin alkaa toteuttaa älykkäämpää tietokonevastustajaa.
