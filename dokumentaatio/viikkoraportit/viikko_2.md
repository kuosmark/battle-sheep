# Viikkoraportti 2

Käytin toisen viikon aikana projektiin noin 18 tuntia.

Otin käyttöön Poetryn ja Pylintin projektinhallinnan avuksi. Päivitin vaatimusmäärittelyä, ja siinä kuvaamaani ratkaisua. Lähdin rakentamaan projektin ydintä eli itse minimax-algoritmia sekä tietorakennetta, johon pelilaudan tilanne talletetaan. Algoritmin testaukseen kirjoitin yksinkertaisen komentorivikäyttöliittymän, jonka hylkäsin kuitenkin pian, ja aloin tehdä "oikeaa" käyttöliittymää GitHubista kopioimani heksagonaalitiiliä generoivan koodin pohjalta. Tutkin kotoani löytyvää Battle Sheep -lautapeliä, ja hahmottelin sen avulla ohjelman toimintaa. Tarkoitus oli myös kirjoittaa testejä jo laatimalleni koodille, mutten ehtinyt aloittaa sitä vielä.

Tällä hetkellä minulla on ajettava ohjelma, joka piirtää näytölle 32 kuusikulmion pelilaudan. Pelilaudalta voi hiirellä valita ruudun, jolloin siihen lisätään 16 lammasta. Pelimekaniikkaa ei vielä ole.

![Kuvakaappaus sovelluksesta viikon 2 päättyessä](/dokumentaatio/kuvat/viikko_2.png "Kuvakaappaus sovelluksesta viikon 2 päättyessä")

Olen käyttänyt Pythonia viime vuosina lähinnä skriptaukseen, joten nyt on pitänyt palauttaa mieleen olio-ohjelmoinnin hyviä käytäntöjä. Tämä projekti on ollut hyvä muistinvirkistys siitä, miksi toteutuksen suunnittelu ja asianmukaisen työjonon kokoaminen on niin tärkeää. Kuten usein ohjelmistoprojekteissa, paine päästä koodaamaan oli kova, minkä takia suunnitteluvaihe jäi turhan suppeaksi. Jouduinkin käyttöliittymän kanssa heittämään vanhan tekeleeni roskiin, ja aloittamaan alusta.

Hankalaa on ollut tekemisen organisointi ja priorisointi. Työskentely yksin on poukkoilevaa. Pitäisikö ensin laatia jonkinlainen käyttöliittymä, jotta algoritmia olisi helpompi ajaa? Vai pitäisikö aloittaa pelimekaniikasta? Projektin ydin on kuitenkin "tekoäly" ja sen päätöksentekoa ohjaava heuristiikka. Myös kiire tuntuu jo nyt. Tekemistä on paljon, ja ohjelman valmistuminen aikataulussa mietityttää.

Minulla onkin edessäni dilemma. Työskentelenkö seuraavaksi pelimekaniikan parissa, ja yritän saada pelistä pelattavan vai jatkanko minimax-algoritmin parissa? Tietorakenne, johon pelitilanne talletetaan ei myöskään sisällä vielä kaikkea tarpeellista dataa.
