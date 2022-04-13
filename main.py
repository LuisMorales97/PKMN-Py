from Game import *

def main():
    game = Game()
    while not game.stopped:
        game.process()
        game.render()

if __name__ == "__main__":
    main()