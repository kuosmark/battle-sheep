# Viikkoraportti 6

Käytin kuudennen viikon aikana projektiin noin 27 tuntia.

Viikko meni ihan mukavasti. Olen eriyttänyt koodia paremmin loogisiksi kokonaisuuksiksi saamani vertaispalautteen pohjalta. Olen kirjoitellut paljon testejä ohjelmani luokille. Myös monimutkaisempia testejä, jotka testaavat eri luokkien yhteistoimintaa. Testaus on ollut kyllä haastavaa ohjelman luonteen vuoksi enkä ehdi esimerkiksi hyödyllisiä end-to-end-testejä enää tämän projektin puitteissa tekemään.

Olen lisännyt pelinäkymään sivupaneelin, josta näkee pelatessa kätesvästi eri pelitietoja. Siitä on ollut apua bugikorjauksessa. Toteutin myös komentoriviparametrilla käynnistettävän kahden tekoälyn pelin testatakseni algoritmia. Tarkoitus olisi tehdä vielä muutamia automaattitestejä eri tasoisten tekoälyjen peleistä. Aika harmillisesti loppuu nyt, kun testauksessa tuntuu pääseen kiinnostaviin skenaarioihin. Olen myös tajunnut, ettei heuristiikkani ole järkevä, ja kaipaa vielä hiomista. Se onkin dokumentoinnin ohella projektin loppuajan tärkein homma.

![Kuvakaappaus sovelluksesta viikon 6 päättyessä](/dokumentaatio/kuvat/viikko_6.png "Kuvakaappaus sovelluksesta viikon 6 päättyessä")

Algoritmi toimii hitaammin kuin haluaisin. Olen onnistunut kuitenkin merkittävästi nopeuttamaan sitä kuluneen viikon aikana. Ilman alfa-beeta-karsintaa ja siirtojen järjestämistä heuristiikan perusteella, tekoälyn ensisiirron laskemiseen menee 25,17 sekuntia laskentasyvyydellä 3. Alfa-beeta-karsinnan ja siirtojen järjestämisen kanssa ensisiirtoon menee samalla syvyydellä 5,27 sekuntia. Tämä projekti siispä upeasti havainnollistaa, miksi karsintaa kannattaa tehdä. Viikko sitten ajaessani algoritmin ensi kerran järjestämisen ja karsinnan kanssa, kesti suorituksessa 9,59 sekuntia. Sen jälkeen olenkin päivä päivältä saanut ohjelmaani optimoitua. Tiistaina pääsin alle seitsemän sekunnin ja perjantaina kuuden.
