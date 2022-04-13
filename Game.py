import pygame
import json
from functools import partial
from pygame.locals import *
from constants import *
from Models.Battle import *
from Models.Pokemon import *
from Models.Button import *
from Models.GUI import *
from Models.Menu import *

class Game:
    def __init__(self):
        self.buttons = []
        self.menu = Menu()
        self.gui = GUI()
        self.bg = None
        pygame.init()
        
        self.screen = pygame.display.set_mode((160*4, 144*4))
        pygame.display.set_caption("PKMON-Py")
        
        clock = pygame.time.Clock()
        clock.tick(60)

        self.initPokemonStats()

        self.pokemon1.attacks = [Attack("Latigo Cepa", 11, PHYSICAL, 10, 10, 100),
                                 Attack("Corte", 11, PHYSICAL, 10, 10, 100)]
        self.pokemon2.attacks = [Attack("Arañazo", 0, PHYSICAL, 10, 10, 100)]

        # for idx, attack in enumerate(self.pokemon1.attacks):
        #     functionTurn = partial(self.makeTurn, index=idx)
        #     self.buttons.append(
        #         Button(idx*100, 0, 100, 40, attack.name, functionTurn)
        #     )

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
            self.menu.handle_event(event, self)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    print(event.pos)

    def loadResources(self):
        self.loadPokemonImage(self.pokemon1, True)
        self.loadPokemonImage(self.pokemon2, False)
        self.gui.loadResources()

    def loadPokemonImage(self, pokemon, isPlayer):
        pokemon_name = pokemon.name.lower()
        if isPlayer:
            pokemon_img = pygame.image.load('res/pokemon/'+pokemon_name+"_back.png")
            pokemon_img = pygame.transform.scale(pokemon_img, (300, 300))
            pokemon.renderer = pokemon_img
        else:
            pokemon_img = pygame.image.load('res/pokemon/'+pokemon_name+"_front.png")
            pokemon_img = pygame.transform.scale(pokemon_img, (200, 200))
            pokemon.renderer = pokemon_img
        
        self.bg = pygame.image.load('res/battle_bg/battle_bg_1.png')
        self.bg = pygame.transform.scale(self.bg, (160*4, 400))
    
    def initPokemonStats(self):
        pokemon1 = "Bulbasaur"
        pokemon2 = "Charmander"
        with open('db/pokemons.json') as f:
            data = json.load(f)
            type2 = None
            if "type2" in data[pokemon1].keys():
                type2 = data[pokemon1]["type2"]
            self.pokemon1 = Pokemon(pokemon1, 100, data[pokemon1]["type1"], type2)
            type22 = None
            if "type2" in data[pokemon2]:
                type22 = data[pokemon2]["type2"]
            self.pokemon2 = Pokemon(pokemon2, 100, data[pokemon2]["type1"], type22)
            self.pokemon1.baseStats = {
                HP: data[self.pokemon1.name]["hp"],
                ATTACK: data[self.pokemon1.name]["attack"],
                DEFENSE: data[self.pokemon1.name]["defense"],
                SPATTACK: data[self.pokemon1.name]["spattack"],
                SPDEFENSE: data[self.pokemon1.name]["spdefense"],
                SPEED: data[self.pokemon1.name]["speed"]
            }

            self.pokemon2.baseStats = {
                HP: data[self.pokemon2.name]["hp"],
                ATTACK: data[self.pokemon2.name]["attack"],
                DEFENSE: data[self.pokemon2.name]["defense"],
                SPATTACK: data[self.pokemon2.name]["spattack"],
                SPDEFENSE: data[self.pokemon2.name]["spdefense"],
                SPEED: data[self.pokemon2.name]["speed"]
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
        self.pokemon1.compute_stats()
        self.pokemon2.compute_stats()
        print(self.pokemon1.stats)
        print(self.pokemon2.stats)
        self.pokemon1.current_hp = self.pokemon1.stats["HP"]
        self.pokemon2.current_hp = self.pokemon2.stats["HP"]
        print(self.pokemon1.current_hp, self.pokemon1.stats["HP"])

    def renderPokemons(self):
        pokemon1Size = self.pokemon1.renderer.get_rect().size
        self.pokemon1.render(self.screen, (10, 460-pokemon1Size[1]))
        self.pokemon2.render(self.screen, (440, 0))

    def renderButtons(self):
        self.menu.render(self)
        self.gui.render(self)
        if self.pokemon1.current_hp > 0 and self.pokemon2.current_hp > 0:
            for button in self.buttons:
                button.render(self)
        
        if self.pokemon1.current_hp > 0 and self.pokemon2.current_hp == 0:
            self.gui.renderMessage(self, self.pokemon1.name+" ha ganado!")
        elif self.pokemon2.current_hp > 0 and self.pokemon1.current_hp == 0:
            self.gui.renderMessage(self, self.pokemon2.name+" ha ganado!")
        elif self.pokemon2.current_hp == 0 and self.pokemon1.current_hp == 0:
            self.gui.renderMessage(self, "Increible! Doble KO!")
        else:
            self.gui.renderMessage(self, "Que deberia hacer "+self.pokemon1.name+"?")

    def render(self):
        self.screen.fill((255, 255, 255)) #fill white
        if (self.bg):
            self.screen.blit(self.bg, (0, 0))
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