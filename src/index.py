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
        x = int(input('X-koordinaatti: '))
        y = int(input('Y-koordinaatti: '))
        sheep = int(input('Lampaiden määrä (1-16): '))
        board.place_sheep(1, sheep, (x, y))

    if command == 'tulosta':
        board.display()

    if command == 'lopeta':
        running = False
