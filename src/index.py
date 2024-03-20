running = True

# Pelin suoritus
while running:
    print('Peli on käynnissä')

    command = input("Syötä komento: ")
    if command == 'lopeta':
        running = False
