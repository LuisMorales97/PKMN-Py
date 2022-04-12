from Game import *


# def ask_command(pokemon):
#     command = None
#     while not command:
#         # DO_ATTACK -> attack 0
#         tmp_command = input("¿Que deberia hacer "+pokemon.name+"?").split(" ")
#         if len(tmp_command) == 2:
#             print(tmp_command)
#             try:
#                 if tmp_command[0] == DO_ATTACK and 0 <= int(tmp_command[1]) < 4:
#                     command = Command({DO_ATTACK: int(tmp_command[1])})
#             except Exception:
#                 pass
#     return command

def main():
    game = Game()
    while not game.stopped:
        game.process()
        game.render()


# while not battle.is_finished():
        # #Primero pregunta el comando
        # command1 = ask_command(pokemon1)
        # command2 = ask_command(pokemon2)

        # turn = Turn()
        # turn.command1 = command1
        # turn.command2 = command2

        # if turn.can_start():
        #     # Ejecutar turno
        #     battle.execute_turn(turn)
        #     battle.print_current_status()
        

if __name__ == "__main__":
    main()

