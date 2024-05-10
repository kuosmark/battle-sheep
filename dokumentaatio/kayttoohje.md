# Käyttöohje

Battle Sheep on strategiapeli, jossa pelaajat ohjaavat lampaita taistelussa niityn herruudesta. Peliä voi pelata itse, tai simuloida kahden tekoälyn välistä ottelua.

## Vaatimukset

- Python 3.12
- Poetry (testattu versiolla 1.8.2)

## Asennus

### Ympäristön tarkistus

Varmista, että sinulla on oikeat versiot Pythonista ja Poetrysta. Voit tarkistaa asennetut versiot komennoilla:

```sh
python3 --version
poetry --version
```

### Repositorion kloonaus:

```sh
git clone https://github.com/kuosmark/battle-sheep
```

### Riippuvuuksien asennus:

```sh
cd battle-sheep
poetry install --no-root
```

## Käynnistys

### Tavallinen peli:

```sh
poetry run python3 src/main.py
```

### Kahden tekoälypelaajan simulaatio:

```sh
poetry run python3 src/main.py ai
```

## Pelaaminen

Pelin aluksi kumpikin pelaaja asettaa omat lampaansa (16 kpl) yhdelle laudan reunalaitumista. Omalla vuorollaan pelaaja siirtää joltakin laitumeltaan valitsemansa lammasmäärän linjassa kunnes se törmää pelialueen laitaan tai valloitettuun laitumeen. Lähtölaitumelle on jätettävä vähintään yksi lammas.

Kun lauta täyttyy, ja pelaajalla ei ole enää laitumia, joista siirtää lampaita vapaalle laitumelle, päättyy hänen pelinsä. Peli loppuu kun kummallakaan pelaajalla ei ole enää siirtoja jäljellä. Eniten lampaitaan laudalle levittänyt pelaaja voittaa pelin.

## Käyttöliittymä ja komennot

Lähtölaidun valitaan painamalla hiiren vasenta painiketta, minkä jälkeen mahdolliset kohdelaitumet valaistaan pelilaudalla. Tämän jälkeen valitaan kohdelaidun. Siirrettävien lampaiden määrä valitaan vierittämällä hiiren rullaa tai käyttämällä nuolinäppäimiä. Siirto vahvistetaan Enter-näppäimellä tai hiiren oikealla painikkeella.

Pelitilanteen tiedot esitetään ruudun oikeassa reunassa. _Vaikeustaso_ tarkoittaa tekoälyvastustajan algoritmin laskentasyvyyttä. _Tilanne_ kertoo pelitilanteen heuristisen arvon ja _siirron kesto_ tietokoneen tekemän viimeisimmän siirron laskenta-ajan.

## Pelin muokkaaminen

Peliä on mahdollista muokata muuttamalla tiedoston `src/constants.py` arvoja kohdassa _Säädettävät muuttujat_. Pelilaudan mittoja voi säätää muuttamalla arvoja _BOARD_HEIGHT_ ja _BOARD_WIDTH_. Tekoälyvastustajan laskentasyvyyttä voi säätää muuttamalla arvoa _COMPUTER_DEPTH_. Suurempi luku tekee vastustajasta haastavamman, mutta samalla pidentää laskenta-aikaa. Muuttujan _SIMULATED_PLAYER_DEPTH_ arvo on simulaatiopelien "pelaajan" laskentasyvyys, jota säätämällä voi muuttaa simulaatioiden dynamiikkaa.

## Testit

### Kaikkien testien ajaminen:

```sh
poetry run pytest src/
```

### Testikattavuusraportin luonti:

1. Kerätään testikattavuusdata:

```sh
poetry run coverage run --branch -m pytest src/
```

2. Luodaan visuaalinen raportti:

```sh
poetry run coverage html
```

Raportti tallennetaan tiedostoon `htmlcov/index.html`, josta se on helppo avata selaimella.

### Koodin staattinen analyysi:

```sh
poetry run pylint src/
```
