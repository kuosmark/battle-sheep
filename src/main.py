import sys
from ui import Ui


def main(is_simulation: bool):
    ui = Ui(is_simulation)

    while ui.is_running:
        ui.play_game()
        ui.render()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ai':
        main(is_simulation=True)

    main(is_simulation=False)
