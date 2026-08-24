import pygame
import random
import math
import sys

# ============================================================
# AS CRÔNICAS DE AETHERIA
# RPG 2D em Pygame
#
# Instale:
#   pip install pygame
#
# Execute:
#   python aetheria_rpg.py
# ============================================================

pygame.init()

W, H = 1280, 720
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("As Crônicas de Aetheria")
CLOCK = pygame.time.Clock()
FPS = 60

# -------------------- CORES --------------------
WHITE = (245, 248, 255)
BLACK = (8, 10, 18)
DARK = (15, 19, 30)
PANEL = (26, 33, 49)
PANEL2 = (37, 45, 64)
GRAY = (150, 160, 180)
LIGHT_GRAY = (205, 212, 225)
GOLD = (246, 195, 70)
GREEN = (73, 214, 118)
RED = (235, 72, 84)
BLUE = (65, 145, 255)
CYAN = (70, 220, 235)
ORANGE = (255, 142, 55)
PURPLE = (176, 105, 255)
PLANT = (77, 205, 102)

FONT = pygame.font.SysFont("arial", 21)
SMALL = pygame.font.SysFont("arial", 16)
MEDIUM = pygame.font.SysFont("arial", 27, bold=True)
BIG = pygame.font.SysFont("arial", 42, bold=True)
TITLE = pygame.font.SysFont("arial", 64, bold=True)
HUGE = pygame.font.SysFont("arial", 92, bold=True)

ELEMENT_COLOR = {
    "Fogo": (245, 75, 38),
    "Água": (55, 145, 245),
    "Elétrico": (250, 220, 55),
    "Planta": (75, 205, 100),
    "Neutro": (190, 195, 205),
}

# Regra pedida:
# Água causa mais dano em Fogo
# Fogo causa mais dano em Planta
# Elétrico causa mais dano em Água
# Planta causa mais dano em Elétrico
ADVANTAGE = {
    ("Água", "Fogo"),
    ("Fogo", "Planta"),
    ("Elétrico", "Água"),
    ("Planta", "Elétrico"),
}


# -------------------- UTILIDADES --------------------
def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def text(surface, msg, font, color, x, y, center=False):
    img = font.render(str(msg), True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)
    return rect


def rounded_panel(surface, rect, color=PANEL, radius=20, border=None, width=2):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, width, border_radius=radius)


def bar(surface, rect, value, maximum, fill, label="", label_color=WHITE):
    x, y, w, h = rect
    pygame.draw.rect(surface, (8, 10, 17), (x, y, w, h), border_radius=h // 2)
    ratio = 0 if maximum <= 0 else clamp(value / maximum, 0, 1)
    inner = max(0, int((w - 4) * ratio))
    if inner:
        pygame.draw.rect(surface, fill, (x + 2, y + 2, inner, h - 4), border_radius=(h - 4) // 2)
    if label:
        text(surface, label, SMALL, WHITE, x + 8, y + 1)


def button(surface, rect, label, enabled=True, accent=BLUE, small=False):
    mouse = pygame.mouse.get_pos()
    hover = pygame.Rect(rect).collidepoint(mouse)
    base = accent if enabled else (70, 75, 90)
    if hover and enabled:
        base = tuple(clamp(c + 22, 0, 255) for c in base)
    pygame.draw.rect(surface, base, rect, border_radius=12)
    pygame.draw.rect(surface, (230, 235, 245) if enabled else (115, 120, 135),
                     rect, 2, border_radius=12)
    f = SMALL if small else FONT
    text(surface, label, f, WHITE, rect[0] + rect[2] // 2, rect[1] + rect[3] // 2, True)
    return hover


def draw_gradient_background(surface, top, bottom):
    for y in range(H):
        t = y / max(1, H - 1)
        c = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        pygame.draw.line(surface, c, (0, y), (W, y))


def wrap_text(msg, font, max_width):
    words = msg.split()
    lines = []
    current = ""
    for word in words:
        test = word if not current else current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# -------------------- PARTÍCULAS / ANIMAÇÕES --------------------
class Particle:
    def __init__(self, x, y, color, vx, vy, life, size=5):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 120 * dt
        self.life -= dt

    def draw(self, surf):
        if self.life <= 0:
            return
        alpha = int(255 * clamp(self.life / self.max_life, 0, 1))
        s = max(1, int(self.size * (0.45 + self.life / self.max_life)))
        layer = pygame.Surface((s * 4, s * 4), pygame.SRCALPHA)
        pygame.draw.circle(layer, (*self.color, alpha), (s * 2, s * 2), s)
        surf.blit(layer, (self.x - s * 2, self.y - s * 2))


class FloatingText:
    def __init__(self, x, y, msg, color=WHITE, size=30, duration=1.2):
        self.x = x
        self.y = y
        self.msg = msg
        self.color = color
        self.life = duration
        self.max_life = duration
        self.font = pygame.font.SysFont("arial", size, bold=True)

    def update(self, dt):
        self.y -= 35 * dt
        self.life -= dt

    def draw(self, surf):
        if self.life <= 0:
            return
        alpha = int(255 * clamp(self.life / self.max_life, 0, 1))
        img = self.font.render(self.msg, True, self.color)
        img.set_alpha(alpha)
        rect = img.get_rect(center=(self.x, self.y))
        surf.blit(img, rect)


# -------------------- DADOS DO JOGO --------------------
ATTACKS = {
    "Fogo": [
        ("Faísca Ígnea", 35, 24, "fire"),
        ("Lança de Fogo", 40, 39, "fire_big"),
        ("Chuva de Brasas", 43, 55, "fire_rain"),
        ("Fúria Vulcânica", 45, 72, "fire_ult"),
    ],
    "Água": [
        ("Jato de Água", 35, 24, "water"),
        ("Lâmina Oceânica", 40, 39, "water_big"),
        ("Tsunami", 43, 55, "water_wave"),
        ("Abismo Azul", 45, 72, "water_ult"),
    ],
    "Elétrico": [
        ("Faísca", 35, 24, "electric"),
        ("Raio Cortante", 40, 39, "electric_big"),
        ("Tempestade", 43, 55, "electric_storm"),
        ("Trovão Celestial", 45, 72, "electric_ult"),
    ],
    "Planta": [
        ("Espinho Vivo", 35, 24, "plant"),
        ("Chicote de Vinhas", 40, 39, "plant_big"),
        ("Floresta Furiosa", 43, 55, "plant_forest"),
        ("Cólera da Natureza", 45, 72, "plant_ult"),
    ],
}

MONSTERS = [
    {"name": "Slime de Musgo", "element": "Planta", "hp": 86, "atk": 15, "def": 4, "mana": 70, "coins": (22, 50), "crit": .07},
    {"name": "Lobo das Cinzas", "element": "Fogo", "hp": 98, "atk": 18, "def": 5, "mana": 74, "coins": (26, 50), "crit": .09},
    {"name": "Serpente do Lago", "element": "Água", "hp": 110, "atk": 19, "def": 7, "mana": 82, "coins": (28, 50), "crit": .11},
    {"name": "Golem de Raio", "element": "Elétrico", "hp": 122, "atk": 21, "def": 9, "mana": 90, "coins": (32, 50), "crit": .12},
    {"name": "Orc Rubro", "element": "Fogo", "hp": 142, "atk": 25, "def": 11, "mana": 80, "coins": (40, 65), "crit": .15},
    {"name": "Guardião de Espinhos", "element": "Planta", "hp": 156, "atk": 26, "def": 14, "mana": 95, "coins": (45, 75), "crit": .17},
    {"name": "Tubarão Tempestuoso", "element": "Água", "hp": 175, "atk": 29, "def": 15, "mana": 100, "coins": (48, 80), "crit": .20},
    {"name": "Cavaleiro Voltaico", "element": "Elétrico", "hp": 190, "atk": 32, "def": 17, "mana": 110, "coins": (52, 90), "crit": .23},
]

SHOP = [
    {
        "name": "Espada de Aether",
        "type": "Arma",
        "price": 120,
        "bonus_damage": 12,
        "bonus_def": 0,
        "desc": "+12 dano físico"
    },
    {
        "name": "Armadura Guardiã",
        "type": "Armadura",
        "price": 220,
        "bonus_damage": 0,
        "bonus_def": 15,
        "desc": "+15 defesa"
    },
    {
        "name": "Cajado Arcano",
        "type": "Cajado",
        "price": 340,
        "bonus_damage": 18,
        "bonus_def": 0,
        "desc": "+18 dano mágico"
    },
    {
        "name": "Manto da Aurora",
        "type": "Armadura",
        "price": 500,
        "bonus_damage": 0,
        "bonus_def": 25,
        "desc": "+25 defesa"
    },
    {
        "name": "Relíquia dos Quatro Elementos",
        "type": "Relíquia",
        "price": 700,
        "bonus_damage": 28,
        "bonus_def": 8,
        "desc": "+28 magia, +8 defesa"
    },
]

ALL_ELEMENT_POWER_PRICE = 1000


# -------------------- ESTADOS --------------------
STATE_MAGIC = "magic"
STATE_VILLAGE = "village"
STATE_SHOP = "shop"
STATE_MISSIONS = "missions"
STATE_INTRO_FIGHT = "intro_fight"
STATE_BATTLE = "battle"
STATE_GAMEOVER = "gameover"
STATE_VICTORY = "victory"


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = STATE_MAGIC
        self.magic = None
        self.secondary_magic = None

        self.level = 1
        self.power_level = 1
        self.exp = 0
        self.exp_to_next = 100

        self.max_hp = 100
        self.hp = 100
        self.defense = 8
        self.base_damage = 12
        self.max_mana = 120
        self.mana = self.max_mana

        self.coins = 0
        self.shop_bought = [False] * len(SHOP)
        self.owned_all_elements = False

        self.enemy_bonus = 0
        self.monster_counter = 0
        self.total_wins = 0
        self.turn = 1

        self.missions = [
            {"title": "Primeiro Sangue", "desc": "Vença 1 batalha.", "goal": 1, "current": 0, "reward": 70, "done": False},
            {"title": "Caçador de Monstros", "desc": "Vença 3 batalhas.", "goal": 3, "current": 0, "reward": 130, "done": False},
            {"title": "Veterano", "desc": "Chegue ao nível 3.", "goal": 3, "current": 1, "reward": 180, "done": False},
        ]

        self.enemy = None
        self.enemy_hp = 0
        self.enemy_max_hp = 0
        self.enemy_mana = 0
        self.enemy_shield = 0

        self.intro_timer = 0
        self.intro_phase = 0
        self.message = "Escolha sua magia."
        self.action_log = []
        self.pending_action = None

        self.particles = []
        self.floating = []
        self.anim_timer = 0
        self.anim_kind = None
        self.shake = 0
        self.flash = 0

        self.boss = False
        self.boss_turn = 0

        self.selected_attack = None
        self.shop_scroll = 0

    # ---------- Progressão ----------
    def add_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            self.exp_to_next = int(self.exp_to_next * 1.25)
            self.max_hp += 20
            self.hp = self.max_hp
            self.defense += 5
            self.base_damage += 4
            self.max_mana += 10
            self.mana = self.max_mana
            self.message = f"Você subiu para o nível {self.level}!"

        self.missions[2]["current"] = self.level

    def add_power_exp(self):
        gained = random.randint(10, 20)
        # O poder vai até nível 5. Cada novo nível desbloqueia ataque.
        if self.power_level < 5:
            # progresso escondido simples por barra de batalha:
            self._power_exp = getattr(self, "_power_exp", 0) + gained
            need = 80 + (self.power_level - 1) * 45
            if self._power_exp >= need:
                self._power_exp -= need
                self.power_level += 1
                self.message = f"Seu poder elemental chegou ao nível {self.power_level}!"
        return gained

    def physical_damage(self):
        return self.base_damage + sum(item["bonus_damage"] for i, item in enumerate(SHOP) if self.shop_bought[i])

    def magic_damage(self):
        return 18 + self.level * 2 + sum(item["bonus_damage"] for i, item in enumerate(SHOP) if self.shop_bought[i])

    def current_defense(self):
        return self.defense + sum(item["bonus_def"] for i, item in enumerate(SHOP) if self.shop_bought[i])

    # ---------- Missões ----------
    def update_missions_after_win(self):
        self.missions[0]["current"] = min(1, self.missions[0]["current"] + 1)
        self.missions[1]["current"] = min(self.missions[1]["goal"], self.missions[1]["current"] + 1)
        for mission in self.missions:
            if not mission["done"] and mission["current"] >= mission["goal"]:
                mission["done"] = True
                self.coins += mission["reward"]
                self.message = f"Missão concluída: {mission['title']}! +{mission['reward']} moedas."

    # ---------- Seleção de monstros ----------
    def choose_monster(self):
        # Depois de cada compra, os inimigos ficam mais fortes.
        weighted = []
        for m in MONSTERS:
            weight = 1 + int(m["crit"] * 100) // 4
            # Monstros com crítico maior ficam mais propensos conforme a progressão.
            weight += self.enemy_bonus // 20
            weighted.extend([m] * max(1, weight))

        base = random.choice(weighted)
        m = dict(base)

        # Escala por item comprado: +15 dano, além de pequenos aumentos de vida/defesa.
        scale = self.enemy_bonus
        m["atk"] += scale
        m["hp"] += scale * 2
        m["def"] += scale // 4
        m["max_hp"] = m["hp"]
        return m

    def start_fight(self, boss=False):
        self.boss = boss
        self.turn = 1
        self.boss_turn = 0
        self.anim_timer = 0
        self.intro_phase = 0
        self.state = STATE_INTRO_FIGHT

        if boss:
            self.enemy = {
                "name": "NEXUS, O ARQUITETO DOS ELEMENTOS",
                "element": "Todos",
                "hp": 900,
                "atk": 50,
                "def": 28,
                "mana": 999,
                "crit": .30,
            }
        else:
            self.enemy = self.choose_monster()

        self.enemy_hp = self.enemy["hp"]
        self.enemy_max_hp = self.enemy["hp"]
        self.enemy_mana = self.enemy["mana"]
        self.enemy_shield = 0

    # ---------- Cura ----------
    def return_to_village(self):
        if self.coins >= 50:
            self.coins -= 50
            self.hp = self.max_hp
            self.mana = self.max_mana
            self.message = "Você descansou na vila. Vida e mana restauradas!"
        else:
            self.message = "Você precisa de 50 moedas para voltar à vila."

    # ---------- Loja ----------
    def buy_item(self, index):
        if index < 0 or index >= len(SHOP):
            return

        if self.shop_bought[index]:
            self.message = "Você já possui este item."
            return

        item = SHOP[index]
        if self.coins < item["price"]:
            self.message = "Moedas insuficientes."
            return

        self.coins -= item["price"]
        self.shop_bought[index] = True
        self.enemy_bonus += 15
        self.message = f"Comprou {item['name']}! Os monstros ficaram mais fortes."

        if all(self.shop_bought):
            self.message = "Você comprou os 5 itens! O chefe foi desbloqueado."

    def buy_all_elements(self):
        if self.owned_all_elements:
            self.message = "Você já possui a Relíquia Elemental Suprema."
            return
        if self.coins < ALL_ELEMENT_POWER_PRICE:
            self.message = "Você precisa de 1000 moedas."
            return
        self.coins -= ALL_ELEMENT_POWER_PRICE
        self.owned_all_elements = True
        self.secondary_magic = "Todos"
        self.max_mana += 30
        self.mana = self.max_mana
        self.message = "A Relíquia Suprema concedeu todos os elementos!"

    # ---------- Combate ----------
    def get_attack_list(self):
        if self.owned_all_elements:
            attacks = []
            for element in ["Fogo", "Água", "Elétrico", "Planta"]:
                attacks.append((f"{element}: {ATTACKS[element][min(self.power_level - 1, 3)][0]}",
                                ATTACKS[element][min(self.power_level - 1, 3)][1],
                                ATTACKS[element][min(self.power_level - 1, 3)][2],
                                ATTACKS[element][min(self.power_level - 1, 3)][3],
                                element))
            return attacks

        unlocked = clamp(self.power_level, 1, 4)
        result = []
        for i in range(unlocked):
            a = ATTACKS[self.magic][i]
            result.append((a[0], a[1], a[2], a[3], self.magic))
        return result

    def physical_attack(self):
        self._do_player_attack("Punho", self.physical_damage(), "Neutro", 0, "physical")

    def elemental_attack(self, idx):
        attacks = self.get_attack_list()
        if idx >= len(attacks):
            return
        name, mana_cost, power, anim, element = attacks[idx]
        if self.mana < mana_cost:
            self.message = "Mana insuficiente!"
            return
        self.mana -= mana_cost
        self._do_player_attack(name, self.magic if not self.owned_all_elements else element,
                               power + self.magic_damage() // 5, mana_cost, anim)

    def _do_player_attack(self, name, base, element, mana_cost, animation):
        # O método aceita parâmetros compactos, distinguindo ataque físico e mágico.
        if isinstance(base, str):
            # chamada acidental: base=element, então não ocorre
            return

        # Corrige formato das chamadas: ataque mágico usa:
        # _resolve_attack(name, damage, element, animation)
        if animation == "physical":
            damage = int(base)
            self._resolve_attack(name, damage, "Neutro", animation)
        else:
            # Neste caminho element contém o custo por compatibilidade.
            damage = int(base)
            actual_element = element
            if self.enemy["element"] != "Todos" and (actual_element, self.enemy["element"]) in ADVANTAGE:
                extra = random.randint(15, 30)
                damage += extra
                self.message = "VANTAGEM ELEMENTAL!"
                self.floating.append(FloatingText(800, 235, f"CRITICO +{extra}", GOLD, 38, 1.3))

            # Mesmo elemento: chance de escudo 10-20%.
            if self.enemy["element"] == actual_element and actual_element != "Neutro":
                self.enemy_shield = random.randint(10, 20)
                damage = int(damage * (1 - self.enemy_shield / 100))
                self.message = f"O inimigo criou um escudo elemental de {self.enemy_shield}%!"

            self._resolve_attack(name, damage, actual_element, animation)
            self.add_power_exp()

    def _resolve_attack(self, name, damage, element, animation):
        # Defesa reduz dano, mas ataques nunca causam menos que 1.
        reduced = max(1, damage - self.enemy["def"] // 3)
        crit = random.random() < .10
        if crit:
            reduced = int(reduced * 1.35)
            self.floating.append(FloatingText(850, 255, "CRITICO!", ORANGE, 42, 1.3))

        self.enemy_hp = max(0, self.enemy_hp - reduced)
        self.anim_kind = animation
        self.anim_timer = 0.85
        self.shake = 7
        self.flash = 0.12
        self.spawn_attack_particles(animation)
        self.floating.append(FloatingText(850, 310, f"-{reduced}", WHITE, 32, 1.0))
        self.action_log.append(f"Você usou {name} e causou {reduced} de dano.")

        if self.enemy_hp <= 0:
            self.win_battle()
        else:
            self.pending_action = "enemy"

    def enemy_turn(self):
        if self.enemy_hp <= 0:
            return

        # Mana/vida regeneram a cada turno.
        self.mana = min(self.max_mana, self.mana + random.randint(5, 20))

        if self.boss:
            boss_elements = ["Fogo", "Água", "Elétrico", "Planta"]
            element = boss_elements[self.boss_turn % len(boss_elements)]
            self.boss_turn += 1
            phrases = [
                "Nexus alterna sua energia elemental!",
                "O núcleo de Aetheria pulsa!",
                "Uma força ancestral se aproxima!",
                "Os quatro elementos se chocam!"
            ]
            self.message = random.choice(phrases)
            attack_power = self.enemy["atk"] + self.boss_turn * 2
        else:
            element = self.enemy["element"]
            attack_power = self.enemy["atk"]

        # Ataque do inimigo pode ser crítico.
        enemy_crit = self.enemy.get("crit", .08)
        # Aumenta a chance dos monstros mais agressivos aparecerem já pela seleção.
        crit = random.random() < enemy_crit
        if crit:
            attack_power += random.randint(15, 30)
            self.floating.append(FloatingText(390, 250, "CRITICO!", ORANGE, 42, 1.3))

        # Fraqueza do jogador.
        player_element = self.magic
        if (element, player_element) in ADVANTAGE:
            extra = random.randint(15, 30)
            attack_power += extra
            self.message = f"{element} tem vantagem contra {player_element}!"

        damage = max(1, attack_power - self.current_defense() // 3)
        self.hp = max(0, self.hp - damage)
        self.floating.append(FloatingText(390, 310, f"-{damage}", RED, 32, 1.0))
        self.spawn_attack_particles(element.lower(), enemy=True)
        self.anim_kind = "enemy_" + element
        self.anim_timer = 0.75
        self.shake = 6
        self.action_log.append(f"{self.enemy['name']} atacou com {element} e causou {damage}.")

        if self.hp <= 0:
            self.state = STATE_GAMEOVER
        else:
            self.turn += 1
            self.enemy_shield = 0

    def try_flee(self):
        if random.random() <= 0.333:
            self.message = "Você conseguiu fugir!"
            self.state = STATE_VILLAGE
        else:
            self.message = "A fuga falhou! O inimigo contra-ataca!"
            self.pending_action = "enemy"
            self.enemy_turn()

    def win_battle(self):
        reward = random.randint(*self.enemy["coins"]) if not self.boss else 1500
        exp_gain = random.randint(35, 60) if not self.boss else 300
        self.coins += reward
        self.add_exp(exp_gain)
        self.total_wins += 1
        self.monster_counter += 1
        self.update_missions_after_win()
        self.mana = min(self.max_mana, self.mana + random.randint(5, 20))
        self.hp = min(self.max_hp, self.hp + random.randint(8, 18))
        self.message = f"Vitória! +{reward} moedas e +{exp_gain} EXP."

        if self.boss:
            self.state = STATE_VICTORY
            return

        self.state = STATE_VILLAGE

    # ---------- Partículas ----------
    def spawn_attack_particles(self, kind):
        cx, cy = 895, 300
        color = ORANGE
        if "water" in kind:
            color = BLUE
        elif "electric" in kind:
            color = (250, 235, 75)
        elif "plant" in kind:
            color = PLANT
        elif "fire" in kind:
            color = ORANGE
        elif "physical" in kind:
            color = WHITE

        for _ in range(34 if "ult" in kind or "storm" in kind or "forest" in kind else 20):
            angle = random.random() * math.tau
            speed = random.randint(90, 310)
            self.particles.append(Particle(
                cx, cy,
                color,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                random.uniform(.35, .95),
                random.randint(3, 8)
            ))

    # ---------- Entrada ----------
    def choose_magic(self, magic):
        self.magic = magic
        self.state = STATE_VILLAGE
        self.message = f"Você escolheu a magia de {magic}!"
        self._power_exp = 0

    def all_items_bought(self):
        return all(self.shop_bought)

    # ---------- Desenho ----------
    def draw(self):
        if self.state == STATE_MAGIC:
            self.draw_magic_screen()
        elif self.state == STATE_VILLAGE:
            self.draw_village()
        elif self.state == STATE_SHOP:
            self.draw_shop()
        elif self.state == STATE_MISSIONS:
            self.draw_missions()
        elif self.state == STATE_INTRO_FIGHT:
            self.draw_intro_fight()
        elif self.state == STATE_BATTLE:
            self.draw_battle()
        elif self.state == STATE_GAMEOVER:
            self.draw_gameover()
        elif self.state == STATE_VICTORY:
            self.draw_victory()

        # Sistema de partículas por cima.
        for p in self.particles:
            p.draw(SCREEN)
        for f in self.floating:
            f.draw(SCREEN)

    def draw_background(self):
        draw_gradient_background(SCREEN, (13, 19, 38), (39, 50, 76))

    def draw_magic_screen(self):
        self.draw_background()

        # Lua / brilho decorativo.
        pygame.draw.circle(SCREEN, (210, 225, 255), (1070, 120), 55)
        pygame.draw.circle(SCREEN, (100, 120, 170), (1090, 105), 55)

        text(SCREEN, "AS CRÔNICAS DE AETHERIA", TITLE, WHITE, W // 2, 90, True)
        text(SCREEN, "Escolha sua magia inicial", MEDIUM, GOLD, W // 2, 155, True)
        text(SCREEN, "A escolha define seu elemento e os ataques desbloqueados.", FONT,
             LIGHT_GRAY, W // 2, 190, True)

        options = [
            ("Fogo", ORANGE, "Forte contra Planta"),
            ("Água", BLUE, "Forte contra Fogo"),
            ("Elétrico", (245, 220, 50), "Forte contra Água"),
            ("Planta", PLANT, "Forte contra Elétrico"),
        ]

        card_w, card_h = 245, 315
        start_x = (W - 4 * card_w - 3 * 24) // 2
        for i, (name, color, desc) in enumerate(options):
            x = start_x + i * (card_w + 24)
            rect = pygame.Rect(x, 245, card_w, card_h)
            hover = rect.collidepoint(pygame.mouse.get_pos())
            rounded_panel(SCREEN, rect, (31, 38, 57) if not hover else (45, 54, 78), 24, color, 3)
            pygame.draw.circle(SCREEN, color, (x + card_w // 2, 315), 45)

            # Ícones simples.
            if name == "Fogo":
                for r in [27, 19, 11]:
                    pygame.draw.circle(SCREEN, (255, 210, 90), (x + card_w // 2, 315), r, 3)
            elif name == "Água":
                pygame.draw.arc(SCREEN, WHITE, (x + 92, 286, 65, 65), math.pi, math.tau, 5)
            elif name == "Elétrico":
                pygame.draw.polygon(SCREEN, WHITE, [(x+132,285),(x+105,325),(x+130,320),(x+114,350),(x+152,305),(x+128,310)])
            else:
                pygame.draw.line(SCREEN, WHITE, (x+122,350), (x+122,282), 5)
                pygame.draw.circle(SCREEN, WHITE, (x+102,300), 13, 3)
                pygame.draw.circle(SCREEN, WHITE, (x+142,307), 13, 3)

            text(SCREEN, name, BIG, WHITE, x + card_w//2, 395, True)
            text(SCREEN, desc, SMALL, LIGHT_GRAY, x + card_w//2, 435, True)
            attacks = ATTACKS[name]
            text(SCREEN, f"Mana: {attacks[0][1]}–{attacks[-1][1]}", SMALL, CYAN,
                 x + card_w//2, 470, True)
            text(SCREEN, "Clique para escolher", SMALL, GOLD, x + card_w//2, 505, True)

        text(SCREEN, "Fraquezas: Água > Fogo > Planta > Elétrico > Água",
             SMALL, LIGHT_GRAY, W//2, 610, True)
        text(SCREEN, "A magia causa um bônus crítico de 15 a 30 ao atingir uma fraqueza.",
             SMALL, WHITE, W//2, 638, True)

    def draw_village(self):
        draw_gradient_background(SCREEN, (22, 39, 56), (74, 71, 76))

        # Céu.
        pygame.draw.circle(SCREEN, (248, 205, 105), (1040, 115), 42)
        # Montanhas.
        pygame.draw.polygon(SCREEN, (42, 54, 67), [(0,430),(190,240),(360,430)])
        pygame.draw.polygon(SCREEN, (52, 64, 78), [(250,430),(500,215),(760,430)])
        pygame.draw.polygon(SCREEN, (37, 48, 60), [(690,430),(900,250),(1120,430)])

        # Chão.
        pygame.draw.rect(SCREEN, (72, 91, 70), (0, 430, W, H-430))
        for i in range(18):
            x = (i * 83 + 20) % W
            y = 470 + (i * 41) % 190
            pygame.draw.line(SCREEN, (59, 76, 58), (x,y), (x+8,y-10), 3)

        # Casa da vila.
        pygame.draw.rect(SCREEN, (103, 69, 50), (75, 300, 285, 190), border_radius=8)
        pygame.draw.polygon(SCREEN, (73, 43, 38), [(45,315),(215,210),(390,315)])
        pygame.draw.rect(SCREEN, (45, 34, 28), (175, 395, 65, 95))
        pygame.draw.rect(SCREEN, (220, 195, 120), (105, 350, 55, 48))
        pygame.draw.rect(SCREEN, (220, 195, 120), (280, 350, 55, 48))

        text(SCREEN, "VILA DE AETHERIA", BIG, WHITE, 55, 40)
        text(SCREEN, f"Moedas: {self.coins}", MEDIUM, GOLD, 55, 92)
        text(SCREEN, f"Nível {self.level}  |  Poder {self.power_level}/5", FONT, WHITE, 55, 128)
        text(SCREEN, f"Elemento: {self.magic}", FONT, ELEMENT_COLOR[self.magic], 55, 158)

        # Personagem.
        px, py = 640, 360
        pygame.draw.circle(SCREEN, (214, 173, 125), (px, py-78), 31)
        pygame.draw.rect(SCREEN, (66, 82, 112), (px-35, py-50, 70, 112), border_radius=18)
        pygame.draw.rect(SCREEN, (43, 55, 75), (px-27, py+58, 18, 70), border_radius=8)
        pygame.draw.rect(SCREEN, (43, 55, 75), (px+9, py+58, 18, 70), border_radius=8)

        # Pedras decorativas.
        for i in range(10):
            x = 430 + (i * 97) % 730
            y = 500 + (i * 31) % 110
            pygame.draw.ellipse(SCREEN, (91, 99, 102), (x, y, 38, 18))

        # Menu.
        menu_x = 905
        buttons = [
            ("Batalhar", STATE_INTRO_FIGHT),
            ("Loja", STATE_SHOP),
            ("Missões", STATE_MISSIONS),
        ]
        for i, (label, state) in enumerate(buttons):
            r = pygame.Rect(menu_x, 205 + i*62, 290, 48)
            button(SCREEN, r, label, True, BLUE)

        r = pygame.Rect(menu_x, 405, 290, 48)
        button(SCREEN, r, "Voltar à vila (-50)", self.coins >= 50, GREEN)

        # Chefe.
        boss_ready = self.all_items_bought()
        r = pygame.Rect(menu_x, 470, 290, 56)
        button(SCREEN, r, "LUTAR CONTRA NEXUS", boss_ready, PURPLE)
        if not boss_ready:
            text(SCREEN, f"Compre todos os 5 itens ({sum(self.shop_bought)}/5)",
                 SMALL, LIGHT_GRAY, menu_x, 535)
        else:
            text(SCREEN, "O chefe final está esperando...", SMALL, GOLD, menu_x, 535)

        # Botão poderes todos elementos.
        r = pygame.Rect(905, 575, 290, 55)
        button(SCREEN, r, "Relíquia: todos os elementos (1000)",
               self.coins >= ALL_ELEMENT_POWER_PRICE and not self.owned_all_elements, ORANGE, True)
        if self.owned_all_elements:
            text(SCREEN, "✓ Relíquia Suprema adquirida", SMALL, GOLD, 905, 636)

        # Mensagem.
        rounded_panel(SCREEN, (420, 620, 440, 52), (24, 29, 42), 14, GOLD, 1)
        text(SCREEN, self.message, SMALL, WHITE, 640, 646, True)

    def draw_shop(self):
        draw_gradient_background(SCREEN, (18, 25, 41), (31, 39, 58))
        text(SCREEN, "FORJA & LOJA DE AETHERIA", TITLE, WHITE, 65, 48)
        text(SCREEN, f"Suas moedas: {self.coins}", MEDIUM, GOLD, 67, 125)

        for i, item in enumerate(SHOP):
            x = 65 + (i % 3) * 390
            y = 185 + (i // 3) * 205
            r = pygame.Rect(x, y, 350, 170)
            bought = self.shop_bought[i]
            rounded_panel(SCREEN, r, (34, 47, 56) if bought else PANEL, 18, GREEN if bought else GOLD, 2)

            # ícone.
            icon_color = GOLD if item["type"] == "Arma" else CYAN if item["type"] == "Cajado" else PURPLE
            pygame.draw.circle(SCREEN, icon_color, (x+48, y+52), 29)
            if item["type"] == "Arma":
                pygame.draw.line(SCREEN, WHITE, (x+35,y+66),(x+61,y+39),5)
            elif item["type"] == "Cajado":
                pygame.draw.line(SCREEN, WHITE, (x+48,y+78),(x+48,y+35),4)
                pygame.draw.circle(SCREEN, WHITE, (x+48,y+31),9)
            else:
                pygame.draw.circle(SCREEN, WHITE, (x+48,y+52),14,3)

            text(SCREEN, item["name"], MEDIUM, WHITE, x+90, y+22)
            text(SCREEN, item["type"], SMALL, LIGHT_GRAY, x+90, y+55)
            text(SCREEN, item["desc"], SMALL, CYAN, x+22, y+98)

            if bought:
                text(SCREEN, "ADQUIRIDO", MEDIUM, GREEN, x+255, y+66)
            else:
                text(SCREEN, f"{item['price']} moedas", FONT, GOLD, x+22, y+130)
                button(SCREEN, pygame.Rect(x+235,y+120,95,34), "COMPRAR",
                       self.coins >= item["price"], BLUE, True)

        # Poder extra
        r = pygame.Rect(835, 435, 350, 140)
        rounded_panel(SCREEN, r, PANEL2, 18, ORANGE, 2)
        text(SCREEN, "RELÍQUIA SUPREMA", MEDIUM, WHITE, 860, 455)
        text(SCREEN, "Todos os elementos", FONT, ORANGE, 860, 490)
        text(SCREEN, "1000 moedas", FONT, GOLD, 860, 520)
        button(SCREEN, pygame.Rect(1035,500,125,42), "COMPRAR",
               self.coins >= 1000 and not self.owned_all_elements, ORANGE, True)

        button(SCREEN, pygame.Rect(65, 635, 170, 45), "← Voltar", True, GRAY)
        text(SCREEN, self.message, SMALL, WHITE, 270, 648)

    def draw_missions(self):
        draw_gradient_background(SCREEN, (17, 23, 37), (46, 38, 58))
        text(SCREEN, "MISSÕES", TITLE, WHITE, 65, 55)
        text(SCREEN, "Conclua objetivos e receba moedas extras.", FONT, LIGHT_GRAY, 68, 125)

        for i, m in enumerate(self.missions):
            y = 190 + i * 140
            r = pygame.Rect(70, y, 1140, 110)
            rounded_panel(SCREEN, r, PANEL, 18, GREEN if m["done"] else GOLD, 2)

            state_text = "CONCLUÍDA" if m["done"] else f"{m['current']}/{m['goal']}"
            state_color = GREEN if m["done"] else GOLD

            text(SCREEN, m["title"], MEDIUM, WHITE, 100, y+20)
            text(SCREEN, m["desc"], FONT, LIGHT_GRAY, 100, y+55)
            text(SCREEN, f"Recompensa: {m['reward']} moedas", SMALL, GOLD, 100, y+80)
            text(SCREEN, state_text, BIG, state_color, 1060, y+54, True)

            bar(SCREEN, (420, y+70, 520, 20),
                m["goal"] if m["done"] else m["current"], m["goal"], GREEN if m["done"] else BLUE)

        button(SCREEN, pygame.Rect(70, 625, 160, 44), "← Vila", True, GRAY)

    def draw_intro_fight(self):
        draw_gradient_background(SCREEN, (8, 12, 28), (47, 36, 49))

        # Feixe dramático.
        pygame.draw.polygon(SCREEN, (45, 48, 67),
                            [(0,720),(210,0),(390,0),(240,720)])
        pygame.draw.polygon(SCREEN, (53, 50, 63),
                            [(1270,720),(1010,0),(1110,0),(1280,520)])

        if self.enemy:
            if self.intro_timer < 0.8:
                text(SCREEN, "UM INIMIGO SE APROXIMA...", MEDIUM, GOLD, W//2, 150, True)
                pygame.draw.circle(SCREEN, RED, (W//2, 320), 78, 5)
                pygame.draw.circle(SCREEN, (50, 55, 67), (W//2, 320), 62)
            elif self.intro_timer < 1.7:
                text(SCREEN, "VOCÊ IRÁ ENFRENTAR", MEDIUM, LIGHT_GRAY, W//2, 110, True)
                text(SCREEN, self.enemy["name"], TITLE,
                     RED if not self.boss else PURPLE, W//2, 205, True)
                text(SCREEN, self.enemy["element"], BIG,
                     WHITE if self.boss else ELEMENT_COLOR.get(self.enemy["element"], WHITE), W//2, 275, True)
                self.draw_enemy_avatar(W//2, 405, 1.35)
            else:
                text(SCREEN, "PREPARE-SE!", HUGE, GOLD, W//2, 340, True)
                text(SCREEN, "Sua aventura decide o destino de Aetheria.",
                     FONT, WHITE, W//2, 435, True)

        text(SCREEN, "O combate começa automaticamente...", SMALL, GRAY, W//2, 635, True)

    def draw_enemy_avatar(self, cx, cy, scale=1):
        color = PURPLE if self.boss else ELEMENT_COLOR.get(self.enemy["element"], RED)
        r = int(65*scale)
        pygame.draw.circle(SCREEN, (16,18,27), (int(cx),int(cy)), int(r*1.25))
        pygame.draw.circle(SCREEN, color, (int(cx),int(cy)), r, 5)
        pygame.draw.circle(SCREEN, (32,36,51), (int(cx),int(cy)), int(r*.75))
        pygame.draw.circle(SCREEN, WHITE, (int(cx-r*.25),int(cy-r*.15)), int(10*scale))
        pygame.draw.circle(SCREEN, WHITE, (int(cx+r*.25),int(cy-r*.15)), int(10*scale))
        pygame.draw.circle(SCREEN, BLACK, (int(cx-r*.25),int(cy-r*.15)), int(4*scale))
        pygame.draw.circle(SCREEN, BLACK, (int(cx+r*.25),int(cy-r*.15)), int(4*scale))

        if self.boss:
            for a in [0.3, 1.4, 2.6, 4.2]:
                x = cx + math.cos(a)*r*1.6
                y = cy + math.sin(a)*r*1.6
                pygame.draw.line(SCREEN, color, (cx + math.cos(a)*r, cy + math.sin(a)*r), (x,y), 7)

    def draw_battle(self):
        # Arena.
        draw_gradient_background(SCREEN, (12, 17, 29), (62, 54, 57))

        # Fundo da arena e partículas luminosas.
        pygame.draw.ellipse(SCREEN, (30, 35, 46), (95, 325, 1080, 300))
        pygame.draw.ellipse(SCREEN, (53, 60, 71), (140, 365, 1000, 210), 3)
        for x in [160, 310, 980, 1120]:
            pygame.draw.line(SCREEN, (70,75,85), (x, 350), (x, 555), 2)

        if self.anim_timer > 0:
            self.draw_animation()

        # Avatares.
        self.draw_player_avatar(330, 290)
        self.draw_enemy_avatar(900, 290, .95)

        # Balões de fala.
        self.draw_dialogue()

        # Painéis de status.
        self.draw_status_panel(35, 450, False)
        self.draw_status_panel(735, 450, True)

        # Botões de combate: tudo em uma única faixa para não sobrepor os controles.
        button(SCREEN, pygame.Rect(30, 610, 145, 44), "Punho", True, GRAY, True)
        attacks = self.get_attack_list()
        attack_x = [185, 370, 555, 740]
        for i, a in enumerate(attacks):
            r = pygame.Rect(attack_x[i], 610, 175, 44)
            can = self.mana >= a[1]
            button(SCREEN, r, f"{a[0][:16]}", can, ELEMENT_COLOR[a[4]], True)

        # Fugir e vila.
        button(SCREEN, pygame.Rect(925, 610, 130, 44), "Fugir", True, RED, True)
        button(SCREEN, pygame.Rect(1070, 610, 175, 44), "Vila (-50)", self.coins >= 50, GREEN, True)

        text(SCREEN, f"Turno {self.turn}", SMALL, LIGHT_GRAY, 35, 425)
        text(SCREEN, f"Moedas: {self.coins}", SMALL, GOLD, 1050, 425)

    def draw_player_avatar(self, cx, cy):
        color = ELEMENT_COLOR[self.magic]
        pygame.draw.circle(SCREEN, (16,18,28), (cx,cy), 80)
        pygame.draw.circle(SCREEN, color, (cx,cy), 65, 4)
        pygame.draw.circle(SCREEN, (213,172,126), (cx,cy-55), 28)
        pygame.draw.rect(SCREEN, (65,80,110), (cx-32,cy-30,64,100), border_radius=16)
        pygame.draw.line(SCREEN, WHITE, (cx+15,cy+70),(cx+33,cy+123),6)
        pygame.draw.line(SCREEN, WHITE, (cx-15,cy+70),(cx-30,cy+123),6)
        if self.owned_all_elements:
            pygame.draw.circle(SCREEN, GOLD, (cx,cy-5), 12, 3)

    def draw_status_panel(self, x, y, enemy):
        obj_name = self.enemy["name"] if enemy else "Aventureiro"
        obj_hp = self.enemy_hp if enemy else self.hp
        obj_max = self.enemy_max_hp if enemy else self.max_hp
        obj_mana = self.enemy_mana if enemy else self.mana
        obj_max_mana = self.enemy["mana"] if enemy else self.max_mana
        obj_element = self.enemy["element"] if enemy else self.magic
        obj_def = self.enemy["def"] if enemy else self.current_defense()
        obj_damage = self.enemy["atk"] if enemy else self.physical_damage()
        obj_color = RED if enemy else ELEMENT_COLOR[self.magic]

        r = pygame.Rect(x, y, 500, 225)
        rounded_panel(SCREEN, r, PANEL, 18, obj_color, 2)

        text(SCREEN, obj_name, MEDIUM, WHITE, x+20, y+17)
        text(SCREEN, f"Elemento: {obj_element}", SMALL,
             ELEMENT_COLOR.get(obj_element, PURPLE if enemy else WHITE), x+20, y+53)

        bar(SCREEN, (x+20,y+80,460,25), obj_hp, obj_max,
            RED if enemy else GREEN, f"Vida {obj_hp}/{obj_max}")
        bar(SCREEN, (x+20,y+112,460,20), obj_mana, obj_max_mana, BLUE,
            f"Mana {obj_mana}/{obj_max_mana}")

        text(SCREEN, f"Defesa: {obj_def}", SMALL, LIGHT_GRAY, x+20, y+148)
        text(SCREEN, f"Dano: {obj_damage}", SMALL, LIGHT_GRAY, x+155, y+148)
        if enemy and self.enemy_shield > 0:
            text(SCREEN, f"Escudo: {self.enemy_shield}%", SMALL, CYAN, x+290, y+148)
        else:
            text(SCREEN, "Mana regenera +5 a +20/turno", SMALL, CYAN, x+250, y+148)

        if not enemy:
            text(SCREEN, f"EXP: {self.exp}/{self.exp_to_next}", SMALL, GOLD, x+20, y+184)
            bar(SCREEN, (x+165,y+186,320,14), self.exp, self.exp_to_next, GOLD)
        else:
            text(SCREEN, f"Crítico: {int(self.enemy.get('crit',.0)*100)}%", SMALL, ORANGE, x+20, y+184)

    def draw_dialogue(self):
        # Pergunta de ação a cada turno.
        if self.state != STATE_BATTLE:
            return
        r = pygame.Rect(285, 375, 710, 58)
        rounded_panel(SCREEN, r, (18,22,32), 15, GOLD, 2)
        if self.anim_timer > 0:
            phrase = "Ação em andamento..."
        else:
            phrase = "O que você fará agora?"
            if self.message:
                phrase = self.message
        text(SCREEN, phrase, FONT, WHITE, 640, 404, True)

    def draw_animation(self):
        t = 1 - clamp(self.anim_timer / .85, 0, 1)
        if self.anim_kind.startswith("enemy_"):
            # Animação do monstro indo para frente.
            element = self.anim_kind.replace("enemy_", "")
            color = ELEMENT_COLOR.get(element, RED)
            x = 900 - int(math.sin(t * math.pi) * 150)
            y = 290
            pygame.draw.circle(SCREEN, color, (x,y), int(30 + 60*t), 4)
            for a in range(8):
                ang = a * math.tau / 8
                rr = 90 + 70*t
                pygame.draw.line(SCREEN, color, (x,y),
                                 (x+math.cos(ang)*rr, y+math.sin(ang)*rr), 3)
        elif "fire" in self.anim_kind:
            for i in range(5):
                x = 510 + int(t*330) + i*22
                y = 300 + int(math.sin(t*7+i)*35)
                pygame.draw.circle(SCREEN, ORANGE, (x,y), 18+i*2)
        elif "water" in self.anim_kind:
            for i in range(5):
                r = int(25+i*14+t*70)
                pygame.draw.circle(SCREEN, BLUE, (840,300), r, 4)
        elif "electric" in self.anim_kind:
            for i in range(6):
                x1 = 500 + random.randint(-15,15)
                y1 = 250 + random.randint(-90,90)
                x2 = 900 + random.randint(-15,15)
                y2 = 290 + random.randint(-90,90)
                points = [(x1,y1)]
                for j in range(1,6):
                    q = j/6
                    points.append((x1+(x2-x1)*q+random.randint(-35,35),
                                   y1+(y2-y1)*q+random.randint(-35,35)))
                points.append((x2,y2))
                pygame.draw.lines(SCREEN, (255,235,80), False, points, 5)
        elif "plant" in self.anim_kind:
            for i in range(6):
                yy = 285 + i*15
                pygame.draw.arc(SCREEN, PLANT,
                                (650+i*18, yy-50, 250, 110), 0, math.pi, 5)
        elif self.anim_kind == "physical":
            pygame.draw.line(SCREEN, WHITE, (470,300),(800,300),12)

    def draw_gameover(self):
        draw_gradient_background(SCREEN, (24, 8, 15), (9, 9, 17))
        text(SCREEN, "VOCÊ FOI DERROTADO", HUGE, RED, W//2, 210, True)
        text(SCREEN, "A queda exige recomeçar desde o início.", BIG, WHITE, W//2, 315, True)
        text(SCREEN, "Seu progresso desta aventura foi perdido.", FONT, LIGHT_GRAY, W//2, 365, True)
        button(SCREEN, pygame.Rect(480, 480, 320, 58), "RECOMEÇAR", True, PURPLE)

    def draw_victory(self):
        draw_gradient_background(SCREEN, (20, 15, 44), (11, 29, 22))
        for i in range(90):
            x = (i * 149) % W
            y = (i * 71) % H
            pygame.draw.circle(SCREEN, GOLD, (x,y), 2)

        text(SCREEN, "AETHERIA FOI SALVA!", HUGE, GOLD, W//2, 195, True)
        text(SCREEN, "NEXUS, O ARQUITETO DOS ELEMENTOS, caiu.", BIG, WHITE, W//2, 300, True)
        text(SCREEN, "Os quatro elementos agora respondem a você.", FONT, LIGHT_GRAY, W//2, 350, True)
        text(SCREEN, f"Vitórias: {self.total_wins}    Moedas: {self.coins}    Nível: {self.level}",
             FONT, WHITE, W//2, 400, True)
        button(SCREEN, pygame.Rect(490, 500, 300, 58), "JOGAR NOVAMENTE", True, PURPLE)

    # ---------- Atualização ----------
    def update(self, dt):
        self.intro_timer += dt
        self.anim_timer = max(0, self.anim_timer - dt)
        self.flash = max(0, self.flash - dt)
        self.shake = max(0, self.shake - dt * 20)

        for p in self.particles:
            p.update(dt)
        self.particles[:] = [p for p in self.particles if p.life > 0]

        for f in self.floating:
            f.update(dt)
        self.floating[:] = [f for f in self.floating if f.life > 0]

        if self.state == STATE_INTRO_FIGHT and self.intro_timer >= 2.5:
            self.state = STATE_BATTLE
            self.intro_timer = 0
            self.message = "O que você fará agora?"
            self.pending_action = None

        if self.state == STATE_BATTLE and self.anim_timer <= 0 and self.pending_action == "enemy":
            self.pending_action = None
            self.enemy_turn()
            if self.state == STATE_BATTLE:
                self.message = "O que você fará agora?"

    # ---------- Eventos ----------
    def handle_click(self, pos):
        x, y = pos

        if self.state == STATE_MAGIC:
            cards = [
                (pygame.Rect(112,245,245,315), "Fogo"),
                (pygame.Rect(381,245,245,315), "Água"),
                (pygame.Rect(650,245,245,315), "Elétrico"),
                (pygame.Rect(919,245,245,315), "Planta"),
            ]
            for r, magic in cards:
                if r.collidepoint(pos):
                    self.choose_magic(magic)
                    return

        elif self.state == STATE_VILLAGE:
            if pygame.Rect(905,205,290,48).collidepoint(pos):
                self.start_fight(False)
            elif pygame.Rect(905,267,290,48).collidepoint(pos):
                self.state = STATE_SHOP
            elif pygame.Rect(905,329,290,48).collidepoint(pos):
                self.state = STATE_MISSIONS
            elif pygame.Rect(905,405,290,48).collidepoint(pos):
                self.return_to_village()
            elif pygame.Rect(905,470,290,56).collidepoint(pos) and self.all_items_bought():
                self.start_fight(True)
            elif pygame.Rect(905,575,290,55).collidepoint(pos):
                self.buy_all_elements()

        elif self.state == STATE_SHOP:
            # cinco cards
            for i in range(len(SHOP)):
                x0 = 65 + (i % 3) * 390
                y0 = 185 + (i // 3) * 205
                if pygame.Rect(x0,y0,350,170).collidepoint(pos):
                    if pygame.Rect(x0+235,y0+120,95,34).collidepoint(pos):
                        self.buy_item(i)
                        return
            if pygame.Rect(1035,500,125,42).collidepoint(pos):
                self.buy_all_elements()
            if pygame.Rect(65,635,170,45).collidepoint(pos):
                self.state = STATE_VILLAGE

        elif self.state == STATE_MISSIONS:
            if pygame.Rect(70,625,160,44).collidepoint(pos):
                self.state = STATE_VILLAGE

        elif self.state == STATE_BATTLE:
            if self.anim_timer > 0 or self.pending_action == "enemy":
                return

            if pygame.Rect(30,610,145,44).collidepoint(pos):
                self.physical_attack()
                return

            attacks = self.get_attack_list()
            attack_x = [185, 370, 555, 740]
            for i, attack in enumerate(attacks):
                if pygame.Rect(attack_x[i],610,175,44).collidepoint(pos):
                    self.elemental_attack(i)
                    return

            if pygame.Rect(925,610,130,44).collidepoint(pos):
                self.try_flee()
                return

            if pygame.Rect(1070,610,175,44).collidepoint(pos):
                self.return_to_village()
                self.state = STATE_VILLAGE
                return

        elif self.state == STATE_GAMEOVER:
            if pygame.Rect(480,480,320,58).collidepoint(pos):
                self.reset()

        elif self.state == STATE_VICTORY:
            if pygame.Rect(490,500,300,58).collidepoint(pos):
                self.reset()

    def handle_key(self, event):
        if event.key == pygame.K_ESCAPE:
            if self.state in (STATE_SHOP, STATE_MISSIONS):
                self.state = STATE_VILLAGE
            elif self.state == STATE_VILLAGE:
                # ESC encerra somente na vila.
                pygame.quit()
                sys.exit()

        if self.state == STATE_BATTLE and self.anim_timer <= 0 and self.pending_action != "enemy":
            if event.key == pygame.K_1:
                self.physical_attack()
            elif event.key == pygame.K_2:
                self.elemental_attack(0)
            elif event.key == pygame.K_3:
                self.elemental_attack(1)
            elif event.key == pygame.K_4:
                self.elemental_attack(2)
            elif event.key == pygame.K_5:
                self.elemental_attack(3)
            elif event.key == pygame.K_f:
                self.try_flee()


game = Game()

while True:
    dt = CLOCK.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            game.handle_key(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.handle_click(event.pos)

    game.update(dt)
    game.draw()

    if game.flash > 0:
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((255,255,255,int(game.flash * 600)))
        SCREEN.blit(overlay, (0,0))

    # Moldura final.
    pygame.draw.rect(SCREEN, (8, 10, 16), (0,0,W,H), 3)

    pygame.display.flip()
