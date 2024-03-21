import board

running = True

# Pelin suoritus
while running:
    print('Peli on käynnissä')
    print('Komennolla "tulosta" voit tulostaa laudan.')
    print('Komennolla "lammas" voit syöttää lampaita.')
    command = input('Komennolla "lopeta" voit lopettaa pelaamisen.\n')

    if command == 'lammas':
        print('Syötä koordinaatit ja lampaiden määrä.\n')
        q = int(input('Q-koordinaatti: '))
        r = int(input('R-koordinaatti: '))
        s = int(input('S-koordinaatti: '))
        sheep = int(input('Lampaiden määrä (1-16): '))

        position = (q, r, s)
        board.place_sheep(1, sheep, position)

    if command == 'tulosta':
        board.display()

    if command == 'lopeta':
        running = False
