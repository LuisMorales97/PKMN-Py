from operator import index
import pygame
from functools import partial
from pygame.locals import *
from sqlalchemy import func
from constants import *
from Models.Battle import *
from Models.Pokemon import *
from Models.Button import *

class Game:
    def __init__(self):
        self.buttons = []
        
        pygame.init()
        self.screen = pygame.display.set_mode((160*4, 144*4))
        pygame.display.set_caption("PKMON-Py")
        # loadResources()
        
        clock = pygame.time.Clock()
        clock.tick(60)

        self.pokemon1 = Pokemon("Bulbasaur", 100, 11, 3)
        self.pokemon2 = Pokemon("Charmander", 100, 9, 1)
        self.initPokemonStats()

        self.pokemon1.attacks = [Attack("Latigo Cepa", 11, PHYSICAL, 10, 10, 100),
                                 Attack("Cepa Latigo", 11, PHYSICAL, 10, 10, 100)]
        self.pokemon2.attacks = [Attack("scratch", 0, PHYSICAL, 10, 10, 100)]

        for idx, attack in enumerate(self.pokemon1.attacks):
            functionTurn = partial(self.makeTurn, index=idx)
            self.buttons.append(
                Button(idx*100, 0, 100, 40, attack.name, functionTurn)
            )

        self.loadResources()
        print('Fuentes cargadas correctamente')

        self.battle = Battle(self.pokemon1, self.pokemon2)
        self.stopped = False
        print('Inicialización terminada')

    
        # while not stopped:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             stopped = True

    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.stopped = True
            for button in self.buttons:
                button.handle_event(event, self)

    def loadResources(self):
        self.loadPokemonImage(self.pokemon1, True)
        self.loadPokemonImage(self.pokemon2, False)

    def loadPokemonImage(self, pokemon, isPlayer):
        pokemon_name = pokemon.name.lower()
        if isPlayer:
            pokemon_img = pygame.image.load('res/pokemon/'+pokemon_name+"_back.png")
            pokemon_img = pygame.transform.scale(pokemon_img, (200, 200))
            pokemon.renderer = pokemon_img
        else:
            pokemon_img = pygame.image.load('res/pokemon/'+pokemon_name+"_front.png")
            pokemon_img = pygame.transform.scale(pokemon_img, (200, 200))
            pokemon.renderer = pokemon_img
        
        # self.bg = pygame.image.load('res/battle_bg/battle_bg_1.png')
        # self.bg = pygame.transform.scale(self.bg, (160*4, 400))
    
    def initPokemonStats(self):
        # Definir nombre, nivel, tipo(s)

        self.pokemon1.current_hp = 45
        self.pokemon2.current_hp = 39

        #Stats

        self.pokemon1.baseStats = {
            HP: 39,
            ATTACK: 52,
            DEFENSE: 43,
            SPATTACK: 80,
            SPDEFENSE: 65,
            SPEED: 65
        }

        self.pokemon1.ev = {
            HP: 0,
            ATTACK: 0,
            DEFENSE: 0,
            SPATTACK: 0,
            SPDEFENSE: 0,
            SPEED: 0
        }

        self.pokemon1.iv = {
            HP: 21,
            ATTACK: 21,
            DEFENSE: 21,
            SPATTACK: 21,
            SPDEFENSE: 21,
            SPEED: 21
        }
        self.pokemon1.compute_stats()
        print(self.pokemon1.stats)

        self.pokemon2.baseStats = {
            HP: 39,
            ATTACK: 52,
            DEFENSE: 43,
            SPATTACK: 80,
            SPDEFENSE: 65,
            SPEED: 65
        }

        self.pokemon2.ev = {
            HP: 0,
            ATTACK: 0,
            DEFENSE: 0,
            SPATTACK: 0,
            SPDEFENSE: 0,
            SPEED: 0
        }

        self.pokemon2.iv = {
            HP: 21,
            ATTACK: 21,
            DEFENSE: 21,
            SPATTACK: 21,
            SPDEFENSE: 21,
            SPEED: 21
        }

        self.pokemon2.compute_stats()
        print(self.pokemon2.stats)

    def renderPokemons(self):
        self.pokemon1.render(self.screen, (10,200))
        self.pokemon2.render(self.screen, (440, 0))

    def renderButtons(self):
        for button in self.buttons:
            button.render(self)

    def render(self):
        self.screen.fill((255, 255, 255))
        self.renderPokemons()
        self.renderButtons()
        pygame.display.update()

    def makeTurn(self, index):
        print('Using attack', index)
        turn = Turn()
        turn.command1 = Command({DO_ATTACK: index})
        turn.command2 = Command({DO_ATTACK: 0})

        if turn.can_start():
            self.battle.execute_turn(turn)
            self.battle.print_current_status()