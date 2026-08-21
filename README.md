import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG 2D - Elemental Quest")

font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()

# =========================
# ELEMENTOS
# =========================
ELEMENTS = ["Fogo", "Agua", "Eletrico", "Planta"]

def vantagem(atk, enemy):
    return (
        (atk == "Agua" and enemy == "Fogo") or
        (atk == "Fogo" and enemy == "Planta") or
        (atk == "Eletrico" and enemy == "Agua") or
        (atk == "Planta" and enemy == "Eletrico")
    )

# =========================
# PLAYER
# =========================
class Player:
    def __init__(self, element):
        self.max_hp = 100
        self.hp = 100
        self.mana = 100
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.element = element
        self.weapon = "Punho"
        self.defense = 5
        self.attack = 10
        self.skills = [f"Golpe {element}"]

    def level_up(self):
        if self.exp >= 100 and self.level < 5:
            self.exp = 0
            self.level += 1
            self.max_hp += 20
            self.attack += 5
            self.defense += 3
            self.hp = self.max_hp
            if len(self.skills) < 4:
                self.skills.append(f"Skill Lv{self.level}")

# =========================
# MONSTRO
# =========================
class Monster:
    def __init__(self, player_level, shop_purchases):
        self.element = random.choice(ELEMENTS)
        base = 40 + player_level * 15 + shop_purchases * 10
        self.hp = base
        self.attack = 10 + player_level * 6 + shop_purchases * 3
        self.defense = 5 + player_level * 3
        self.gold = random.randint(15, 40) + shop_purchases * 5
        self.crit_chance = 10 + shop_purchases * 5

# =========================
# LOJA
# =========================
shop = [
    {"name": "Espada de Ferro", "atk": 15, "price": 50},
    {"name": "Cajado Místico", "atk": 20, "price": 80},
    {"name": "Armadura Leve", "def": 10, "price": 60},
    {"name": "Armadura Pesada", "def": 20, "price": 120},
]

# =========================
# BOSS
# =========================
boss = {
    "name": "DEVORADOR DO ABISMO",
    "hp": 400,
    "attack": 40,
    "defense": 20
}

# =========================
# JOGO
# =========================
class Game:
    def __init__(self):
        self.state = "CHAR"
        self.player = None
        self.monster = None
        self.shop_bought = 0
        self.village_regen = False

    def spawn_monster(self):
        self.monster = Monster(self.player.level, self.shop_bought)

    def draw_text(self, text, x, y):
        img = font.render(text, True, (255,255,255))
        screen.blit(img, (x, y))

game = Game()

# =========================
# LOOP PRINCIPAL
# =========================
while True:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # =========================
            # ESCOLHA DE ELEMENTO
            # =========================
            if game.state == "CHAR":
                if event.key == pygame.K_1:
                    game.player = Player("Fogo")
                    game.state = "VILLAGE"
                if event.key == pygame.K_2:
                    game.player = Player("Agua")
                    game.state = "VILLAGE"
                if event.key == pygame.K_3:
                    game.player = Player("Eletrico")
                    game.state = "VILLAGE"
                if event.key == pygame.K_4:
                    game.player = Player("Planta")
                    game.state = "VILLAGE"

            # =========================
            # VILA
            # =========================
            elif game.state == "VILLAGE":
                if event.key == pygame.K_1:
                    game.spawn_monster()
                    game.state = "BATTLE"
                if event.key == pygame.K_2:
                    game.state = "SHOP"
                if event.key == pygame.K_3:
                    game.village_regen = True

            # =========================
            # BATALHA
            # =========================
            elif game.state == "BATTLE":
                p = game.player
                m = game.monster

                if event.key == pygame.K_1:
                    dmg = p.attack + random.randint(5,15)
                    if vantagem(p.element, m.element):
                        dmg += random.randint(15,30)
                        print("CRITICO")
                    m.hp -= dmg

                if event.key == pygame.K_2:
                    cost = random.randint(35,45)
                    if p.mana >= cost:
                        p.mana -= cost
                        dmg = 25 + random.randint(10,20)
                        if vantagem(p.element, m.element):
                            dmg += random.randint(15,30)
                            print("CRITICO")
                        m.hp -= dmg

                if event.key == pygame.K_3:
                    game.state = "VILLAGE"

                if event.key == pygame.K_4:
                    game.state = "VILLAGE"

                # turno monstro
                if m.hp > 0:
                    mdmg = m.attack + random.randint(0,10)
                    if random.randint(1,100) < m.crit_chance:
                        mdmg *= 2
                        print("CRITICO MONSTRO")
                    p.hp -= mdmg

                # regen mana
                p.mana = min(100, p.mana + random.randint(5,20))

                # morte
                if p.hp <= 0:
                    game = Game()

                # vitória
                if m.hp <= 0:
                    p.gold += m.gold
                    p.exp += random.randint(10,20)
                    p.level_up()
                    game.state = "VILLAGE"

            # =========================
            # LOJA
            # =========================
            elif game.state == "SHOP":
                p = game.player

                if event.key == pygame.K_1:
                    if p.gold >= shop[0]["price"]:
                        p.gold -= shop[0]["price"]
                        p.attack += shop[0]["atk"]
                        game.shop_bought += 1

                if event.key == pygame.K_2:
                    if p.gold >= shop[1]["price"]:
                        p.gold -= shop[1]["price"]
                        p.attack += shop[1]["atk"]
                        game.shop_bought += 1

                if event.key == pygame.K_3:
                    if p.gold >= shop[2]["price"]:
                        p.gold -= shop[2]["price"]
                        p.defense += shop[2]["def"]
                        game.shop_bought += 1

                if event.key == pygame.K_4:
                    if p.gold >= shop[3]["price"]:
                        p.gold -= shop[3]["price"]
                        p.defense += shop[3]["def"]
                        game.shop_bought += 1

                if event.key == pygame.K_0:
                    game.state = "VILLAGE"

    # =========================
    # DESENHO
    # =========================

    if game.state == "CHAR":
        game.draw_text("ESCOLHA ELEMENTO:", 50, 50)
        game.draw_text("1-Fogo 2-Agua 3-Eletrico 4-Planta", 50, 80)

    elif game.state == "VILLAGE":
        p = game.player
        game.draw_text("VILA:", 50, 50)
        game.draw_text("1-Lutar 2-Loja 3-Descansar", 50, 80)
        game.draw_text(f"HP:{p.hp} Mana:{p.mana} Gold:{p.gold}", 50, 120)

    elif game.state == "BATTLE":
        p = game.player
        m = game.monster
        game.draw_text("BATALHA!", 50, 50)
        game.draw_text(f"Monstro HP:{m.hp}", 50, 80)
        game.draw_text(f"Seu HP:{p.hp} Mana:{p.mana}", 50, 110)
        game.draw_text("1-Atk 2-Magia 3-Fugir 4-Vila", 50, 140)

    elif game.state == "SHOP":
        p = game.player
        game.draw_text("LOJA:", 50, 50)
        game.draw_text("1-Espada 2-Cajado 3-Armadura 4-Armadura Pesada 0-Sair", 50, 80)
        game.draw_text(f"Ouro:{p.gold}", 50, 120)

    pygame.display.update()
    clock.tick(30)
