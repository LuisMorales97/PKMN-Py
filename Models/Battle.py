from constants import *
import random

class Battle:

    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.actual_turn = 0

    def is_finished(self):
        finished = self.pokemon1.current_hp <= 0 or self.pokemon2.current_hp <= 0
        if finished:
            self.print_winner()
        return finished

    def execute_turn(self, turn):
        command1 = turn.command1
        command2 = turn.command2
        attack1 = None
        attack2 = None
        if DO_ATTACK in command1.action.keys():
            attack1 = self.pokemon1.attacks[command1.action[DO_ATTACK]]
        if DO_ATTACK in command2.action.keys():
            attack2 = self.pokemon2.attacks[command2.action[DO_ATTACK]]

        #Formula de daño
        self.pokemon2.current_hp -= self.compute_damage(attack1, self.pokemon1, self.pokemon2)
        self.pokemon1.current_hp -= self.compute_damage(attack2, self.pokemon2, self.pokemon1)
        self.actual_turn += 1

    def print_winner(self):
        if self.pokemon1.current_hp <= 0 < self.pokemon2.current_hp:
            print(self.pokemon2.name + " gano en " + str(self.actual_turn) + " turnos")
        elif self.pokemon2.current_hp <= 0 < self.pokemon1.current_hp:
            print(self.pokemon1.name + " gano en " + str(self.actual_turn) + " turnos")
        else:
            print("Doble KO")

    def print_current_status(self):
        print(self.pokemon1.name + " solo tiene " + str(self.pokemon1.current_hp) + " HP!")
        print(self.pokemon2.name + " solo tiene " + str(self.pokemon2.current_hp) + " HP!")

    def compute_damage(self, attack, pokemon1, pokemon2):
        aux = ((2*pokemon1.level)/5) + 2
        powerFactor = aux * attack.power
        if attack.category == PHYSICAL:
            print("Ataque Fisico")
            powerFactor *= (pokemon1.stats[ATTACK]/pokemon2.stats[DEFENSE])
        else:
            powerFactor *= (pokemon1.stats[SPATTACK]/pokemon2.stats[SPDEFENSE])
        damage_without_modifier = powerFactor/50 + 2
        finalDamage = damage_without_modifier * self.compute_damage_modifier(attack, self.pokemon1, self.pokemon2)
        print(finalDamage)
        
        return finalDamage
    
    def compute_damage_modifier(self, attack, pokemon1, pokemon2):
        stab = 1
        if attack.type == pokemon1.type1 or attack.type == pokemon1.type2:
            print("Tiene Stab")
            stab = 1.5
        #Computar tipo de efectividad
        effectiveness1 = TYPE_CHART[pokemon2.type1][attack.type]
        effectiveness2 = TYPE_CHART[pokemon2.type2][attack.type]
        effectiveness_final = effectiveness1 * effectiveness2
        print(stab*effectiveness_final)
        
        critical = 1
        if random.random() < 0.1:
            print(pokemon1.name, "realizo un ataque critico")
            critical = 1.5
        return stab* effectiveness_final

class Turn:
    def __init__(self):
        self.command1 = None
        self.command2 = None
    
    def can_start(self):
        return self.command1 is not None and self.command2 is not None

class Command:
    def __init__(self, action):
        self.action = action