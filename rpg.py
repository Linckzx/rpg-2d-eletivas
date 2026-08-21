import pygame
import random
import sys

# ============================================================
# RPG 2D - A LENDA DOS QUATRO ELEMENTOS
# ============================================================

pygame.init()

WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Lenda dos Quatro Elementos")
clock = pygame.time.Clock()

# ---------------- CORES ----------------

WHITE = (245, 245, 245)
BLACK = (20, 20, 25)
GRAY = (80, 80, 90)
DARK = (35, 35, 45)
GREEN = (50, 200, 80)
RED = (220, 60, 60)
BLUE = (60, 130, 240)
YELLOW = (240, 210, 50)
ORANGE = (255, 130, 40)
PURPLE = (170, 80, 220)
CYAN = (50, 220, 220)

ELEMENT_COLORS = {
    "Fogo": ORANGE,
    "Agua": BLUE,
    "Eletrico": YELLOW,
    "Planta": GREEN
}

FONT = pygame.font.SysFont("Arial", 22)
BIG_FONT = pygame.font.SysFont("Arial", 36, bold=True)
SMALL_FONT = pygame.font.SysFont("Arial", 18)

# ============================================================
# DADOS
# ============================================================

ELEMENTS = ["Fogo", "Agua", "Eletrico", "Planta"]

# Fraquezas:
# Agua > Fogo
# Fogo > Planta
# Eletrico > Agua
# Planta > Eletrico

WEAKNESS = {
    "Agua": "Fogo",
    "Fogo": "Planta",
    "Eletrico": "Agua",
    "Planta": "Eletrico"
}

ATTACKS = {
    "Fogo": [
        ("Chama", 25, 35),
        ("Bola de Fogo", 35, 40),
        ("Explosao Flamejante", 45, 45),
        ("Inferno", 60, 50)
    ],
    "Agua": [
        ("Jato de Agua", 25, 35),
        ("Onda", 35, 40),
        ("Tsunami", 45, 45),
        ("Mare Furiosa", 60, 50)
    ],
    "Eletrico": [
        ("Faísca", 25, 35),
        ("Raio", 35, 40),
        ("Trovao", 45, 45),
        ("Tempestade", 60, 50)
    ],
    "Planta": [
        ("Espinhos", 25, 35),
        ("Chicote Verde", 35, 40),
        ("Raizes", 45, 45),
        ("Floresta Furiosa", 60, 50)
    ]
}

MONSTERS = [
    {
        "name": "Slime Flamejante",
        "element": "Fogo",
        "hp": 100,
        "damage": 12,
        "defense": 3,
        "coins": (15, 30),
        "xp": (20, 35)
    },
    {
        "name": "Lobo Aquatico",
        "element": "Agua",
        "hp": 120,
        "damage": 15,
        "defense": 5,
        "coins": (20, 40),
        "xp": (25, 40)
    },
    {
        "name": "Golem Eletrico",
        "element": "Eletrico",
        "hp": 145,
        "damage": 18,
        "defense": 8,
        "coins": (30, 55),
        "xp": (30, 50)
    },
    {
        "name": "Treant Sombrio",
        "element": "Planta",
        "hp": 170,
        "damage": 20,
        "defense": 10,
        "coins": (40, 70),
        "xp": (35, 55)
    },
    {
        "name": "Dragao Elemental",
        "element": random.choice(ELEMENTS),
        "hp": 220,
        "damage": 25,
        "defense": 15,
        "coins": (60, 100),
        "xp": (50, 75)
    }
]

SHOP = [
    {
        "name": "Espada de Ferro",
        "price": 50,
        "damage": 15,
        "defense": 0,
        "description": "+15 dano"
    },
    {
        "name": "Cajado Elemental",
        "price": 100,
        "damage": 25,
        "defense": 0,
        "description": "+25 dano elemental"
    },
    {
        "name": "Armadura de Couro",
        "price": 150,
        "damage": 0,
        "defense": 15,
        "description": "+15 defesa"
    },
    {
        "name": "Espada do Heroi",
        "price": 250,
        "damage": 40,
        "defense": 5,
        "description": "+40 dano / +5 defesa"
    },
    {
        "name": "Armadura Elemental",
        "price": 400,
        "damage": 10,
        "defense": 35,
        "description": "+35 defesa"
    }
]

# ============================================================
# JOGADOR
# ============================================================

class Player:
    def __init__(self, element):
        self.element = element

        self.level = 1
        self.hp = 100
        self.max_hp = 100

        self.mana = 100
        self.max_mana = 100

        self.damage = 10
        self.defense = 5

        self.coins = 0
        self.xp = 0
        self.xp_needed = 100

        self.weapon = "Punho"
        self.owned_items = []

        self.power_level = 1
        self.power_xp = 0
        self.power_xp_needed = 100

    def gain_xp(self, amount):
        self.xp += amount

        while self.xp >= self.xp_needed:
            self.xp -= self.xp_needed
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 30
        self.hp = self.max_hp

        self.max_mana += 10
        self.mana = self.max_mana

        self.damage += 8
        self.defense += 5

        self.xp_needed = int(self.xp_needed * 1.35)

        add_message(
            f"SUBIU PARA O NIVEL {self.level}!",
            YELLOW
        )

    def gain_power_xp(self, amount):
        self.power_xp += amount

        while (
            self.power_xp >= self.power_xp_needed
            and self.power_level < 5
        ):
            self.power_xp -= self.power_xp_needed
            self.power_level += 1

            add_message(
                f"PODER ELEMENTAL NIVEL {self.power_level}!",
                CYAN
            )

            self.power_xp_needed = int(
                self.power_xp_needed * 1.4
            )

    def buy(self, item):
        if item["name"] in self.owned_items:
            add_message("Voce ja possui este item.", RED)
            return False

        if self.coins < item["price"]:
            add_message("Moedas insuficientes!", RED)
            return False

        self.coins -= item["price"]

        self.damage += item["damage"]
        self.defense += item["defense"]

        self.owned_items.append(item["name"])

        self.weapon = item["name"]

        add_message(
            f"Comprou: {item['name']}!",
            GREEN
        )

        return True

# ============================================================
# MONSTRO
# ============================================================

class Monster:
    def __init__(self, data, difficulty):
        self.name = data["name"]
        self.element = data["element"]

        self.max_hp = data["hp"]
        self.hp = self.max_hp

        self.damage = data["damage"] + difficulty
        self.defense = data["defense"]

        self.coins = data["coins"]
        self.xp = data["xp"]

        # Conforme a loja progride, monstros ficam mais fortes
        self.damage += difficulty

# ============================================================
# ESTADO DO JOGO
# ============================================================

player = None

state = "ELEMENT_SELECT"

current_monster = None

difficulty = 0

message_log = []

mission_kills = 0
mission_coins = 0

boss_unlocked = False
boss_defeated = False

selected_shop_item = 0

# controle de tempo
last_regen = pygame.time.get_ticks()

# ============================================================
# MENSAGENS
# ============================================================

def add_message(text, color=WHITE):
    message_log.insert(0, (text, color))

    if len(message_log) > 7:
        message_log.pop()

# ============================================================
# TEXTO
# ============================================================

def draw_text(text, x, y, color=WHITE, font=FONT):
    image = font.render(str(text), True, color)
    screen.blit(image, (x, y))

# ============================================================
# BARRA
# ============================================================

def draw_bar(x, y, width, height, value, maximum, color):
    pygame.draw.rect(
        screen,
        BLACK,
        (x, y, width, height)
    )

    if maximum > 0:
        current_width = int(
            width * max(0, value) / maximum
        )
    else:
        current_width = 0

    pygame.draw.rect(
        screen,
        color,
        (x, y, current_width, height)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (x, y, width, height),
        2
    )

# ============================================================
# PLAYER SPRITE
# ============================================================

def draw_player(x, y):
    color = ELEMENT_COLORS[player.element]

    # cabeca
    pygame.draw.rect(
        screen,
        (230, 190, 150),
        (x + 15, y, 30, 30)
    )

    # corpo
    pygame.draw.rect(
        screen,
        color,
        (x + 10, y + 30, 40, 45)
    )

    # pernas
    pygame.draw.rect(
        screen,
        (60, 60, 80),
        (x + 10, y + 75, 15, 30)
    )

    pygame.draw.rect(
        screen,
        (60, 60, 80),
        (x + 35, y + 75, 15, 30)
    )

    # arma
    if player.weapon != "Punho":
        pygame.draw.rect(
            screen,
            (210, 210, 210),
            (x + 48, y + 35, 40, 8)
        )

# ============================================================
# MONSTER SPRITE
# ============================================================

def draw_monster(x, y):
    color = ELEMENT_COLORS[current_monster.element]

    pygame.draw.rect(
        screen,
        color,
        (x, y, 120, 100)
    )

    pygame.draw.rect(
        screen,
        BLACK,
        (x + 20, y + 25, 15, 15)
    )

    pygame.draw.rect(
        screen,
        BLACK,
        (x + 85, y + 25, 15, 15)
    )

    pygame.draw.rect(
        screen,
        BLACK,
        (x + 40, y + 65, 40, 8)
    )

# ============================================================
# TELA DE ESCOLHA
# ============================================================

def draw_element_select():
    screen.fill((25, 25, 40))

    draw_text(
        "A LENDA DOS QUATRO ELEMENTOS",
        300,
        70,
        YELLOW,
        BIG_FONT
    )

    draw_text(
        "Escolha seu elemento inicial:",
        390,
        140
    )

    elements = [
        ("Fogo", 150, ORANGE),
        ("Agua", 350, BLUE),
        ("Eletrico", 550, YELLOW),
        ("Planta", 750, GREEN)
    ]

    for name, x, color in elements:
        pygame.draw.rect(
            screen,
            color,
            (x, 220, 150, 150)
        )

        draw_text(
            name,
            x + 35,
            285,
            BLACK,
            BIG_FONT
        )

    draw_text(
        "Clique em um elemento para começar.",
        350,
        450,
        WHITE
    )

    draw_text(
        "Fraquezas: Agua > Fogo | Fogo > Planta | "
        "Eletrico > Agua | Planta > Eletrico",
        150,
        520,
        CYAN,
        SMALL_FONT
    )

# ============================================================
# VILA
# ============================================================

def draw_village():
    screen.fill((80, 160, 90))

    # chão
    pygame.draw.rect(
        screen,
        (150, 110, 70),
        (0, 470, WIDTH, 230)
    )

    # casa
    pygame.draw.rect(
        screen,
        (170, 100, 60),
        (100, 180, 230, 220)
    )

    pygame.draw.polygon(
        screen,
        (100, 40, 40),
        [
            (80, 180),
            (215, 80),
            (350, 180)
        ]
    )

    draw_text(
        "VILA",
        180,
        230,
        WHITE,
        BIG_FONT
    )

    # loja
    pygame.draw.rect(
        screen,
        (80, 80, 140),
        (430, 180, 230, 220)
    )

    draw_text(
        "LOJA",
        500,
        230,
        WHITE,
        BIG_FONT
    )

    # floresta
    for i in range(7):
        x = 760 + (i % 3) * 90
        y = 130 + (i // 3) * 100

        pygame.draw.rect(
            screen,
            (80, 50, 30),
            (x + 30, y + 60, 20, 70)
        )

        pygame.draw.circle(
            screen,
            (30, 120, 50),
            (x + 40, y + 40),
            45
        )

    draw_player(250, 340)

    draw_text(
        "E - Loja",
        460,
        430,
        WHITE
    )

    draw_text(
        "L - Procurar monstro",
        720,
        430,
        WHITE
    )

    draw_text(
        "V - Descansar",
        460,
        470,
        WHITE
    )

    draw_text(
        "M - Missoes",
        720,
        470,
        WHITE
    )

    draw_player_info()

# ============================================================
# INFO DO PLAYER
# ============================================================

def draw_player_info():
    pygame.draw.rect(
        screen,
        DARK,
        (15, 15, 330, 130)
    )

    draw_text(
        f"Nivel: {player.level}",
        30,
        25
    )

    draw_text(
        f"Elemento: {player.element}",
        30,
        55,
        ELEMENT_COLORS[player.element]
    )

    draw_text(
        f"Moedas: {player.coins}",
        30,
        85,
        YELLOW
    )

    draw_text(
        f"Dano: {player.damage}  Defesa: {player.defense}",
        30,
        115,
        WHITE,
        SMALL_FONT
    )

# ============================================================
# LOJA
# ============================================================

def draw_shop():
    screen.fill((35, 35, 50))

    draw_text(
        "LOJA DE EQUIPAMENTOS",
        350,
        30,
        YELLOW,
        BIG_FONT
    )

    draw_text(
        f"Moedas: {player.coins}",
        850,
        40,
        YELLOW
    )

    for i, item in enumerate(SHOP):
        y = 110 + i * 95

        color = (
            (90, 90, 120)
            if i == selected_shop_item
            else (55, 55, 70)
        )

        pygame.draw.rect(
            screen,
            color,
            (100, y, 900, 75)
        )

        draw_text(
            item["name"],
            120,
            y + 10,
            WHITE
        )

        draw_text(
            f"Preco: {item['price']} moedas",
            400,
            y + 10,
            YELLOW
        )

        draw_text(
            item["description"],
            650,
            y + 10,
            CYAN
        )

        if item["name"] in player.owned_items:
            draw_text(
                "COMPRADO",
                850,
                y + 40,
                GREEN,
                SMALL_FONT
            )

    draw_text(
        "Setas: selecionar | ENTER: comprar | ESC: voltar",
        300,
        620,
        WHITE
    )

# ============================================================
# COMBATE
# ============================================================

def draw_battle():
    screen.fill((35, 45, 55))

    draw_text(
        "BATALHA",
        470,
        20,
        RED,
        BIG_FONT
    )

    # jogador
    draw_player(150, 270)

    # monstro
    draw_monster(800, 250)

    # informações jogador
    draw_text(
        f"Nivel {player.level}",
        100,
        150
    )

    draw_text(
        f"HP: {player.hp}/{player.max_hp}",
        100,
        180
    )

    draw_bar(
        100,
        210,
        300,
        25,
        player.hp,
        player.max_hp,
        GREEN
    )

    draw_text(
        f"Mana: {player.mana}/{player.max_mana}",
        100,
        245
    )

    draw_bar(
        100,
        275,
        300,
        25,
        player.mana,
        player.max_mana,
        BLUE
    )

    # informações monstro
    draw_text(
        current_monster.name,
        750,
        150,
        ELEMENT_COLORS[current_monster.element]
    )

    draw_text(
        f"Elemento: {current_monster.element}",
        750,
        180
    )

    draw_text(
        f"HP: {current_monster.hp}/{current_monster.max_hp}",
        750,
        215
    )

    draw_bar(
        750,
        245,
        300,
        25,
        current_monster.hp,
        current_monster.max_hp,
        RED
    )

    # botoes
    buttons = [
        ("1 - Ataque fisico", 80, 390),
        ("2 - Poder elemental", 80, 440),
        ("3 - Fugir", 80, 490),
        ("4 - Voltar para vila", 80, 540)
    ]

    for text, x, y in buttons:
        pygame.draw.rect(
            screen,
            DARK,
            (x, y, 300, 45)
        )

        draw_text(
            text,
            x + 10,
            y + 10,
            WHITE,
            SMALL_FONT
        )

    # ataques disponíveis
    attacks = ATTACKS[player.element]

    draw_text(
        f"Poder nivel {player.power_level}",
        500,
        390,
        CYAN
    )

    max_attacks = min(
        player.power_level,
        4
    )

    for i in range(max_attacks):
        draw_text(
            f"{i + 1}: {attacks[i][0]} "
            f"({attacks[i][1]} dano / {attacks[i][2]} mana)",
            500,
            430 + i * 35,
            WHITE,
            SMALL_FONT
        )

    # mensagens
    pygame.draw.rect(
        screen,
        BLACK,
        (500, 570, 550, 100)
    )

    for i, (msg, color) in enumerate(message_log[:4]):
        draw_text(
            msg,
            515,
            580 + i * 20,
            color,
            SMALL_FONT
        )

# ============================================================
# MISSOES
# ============================================================

def draw_missions():
    screen.fill((30, 35, 45))

    draw_text(
        "MISSOES",
        470,
        40,
        YELLOW,
        BIG_FONT
    )

    draw_text(
        "Missao 1 - Derrote 3 monstros",
        150,
        150
    )

    draw_text(
        f"Progresso: {min(mission_kills, 3)}/3",
        150,
        190,
        CYAN
    )

    if mission_kills >= 3:
        draw_text(
            "CONCLUIDA! Recompensa: 100 moedas",
            150,
            230,
            GREEN
        )

    draw_text(
        "Missao 2 - Junte 300 moedas",
        150,
        300
    )

    draw_text(
        f"Progresso: {min(player.coins, 300)}/300",
        150,
        340,
        CYAN
    )

    if player.coins >= 300:
        draw_text(
            "CONCLUIDA!",
            150,
            380,
            GREEN
        )

    draw_text(
        "ESC - Voltar",
        450,
        600
    )

# ============================================================
# BOSS
# ============================================================

def create_boss():
    boss = {
        "name": "Astaroth, o Guardiao do Vazio",
        "element": random.choice(ELEMENTS),
        "hp": 900,
        "damage": 65 + difficulty,
        "defense": 30,
        "coins": (500, 700),
        "xp": (500, 700)
    }

    return Monster(boss, difficulty)

# ============================================================
# INICIAR BATALHA
# ============================================================

def start_battle():
    global current_monster, state

    data = random.choice(MONSTERS)

    current_monster = Monster(
        data,
        difficulty
    )

    state = "BATTLE"

    add_message(
        f"Um {current_monster.name} apareceu!",
        RED
    )

# ============================================================
# CALCULAR DANO
# ============================================================

def calculate_damage(base_damage, attacker_element, defender_element):
    damage = base_damage + random.randint(-5, 8)

    # fraqueza elemental
    if WEAKNESS.get(attacker_element) == defender_element:
        critical_bonus = random.randint(15, 30)

        damage += critical_bonus

        add_message(
            f"CRITICO! +{critical_bonus} dano!",
            YELLOW
        )

    # mesmo elemento
    if attacker_element == defender_element:
        shield = random.randint(10, 20)

        damage = int(
            damage * (1 - shield / 100)
        )

        add_message(
            f"Escudo elemental reduziu {shield}% do dano!",
            CYAN
        )

    return max(1, damage)

# ============================================================
# ATAQUE FISICO
# ============================================================

def physical_attack():
    damage = player.damage + random.randint(-3, 6)

    damage -= current_monster.defense

    damage = max(1, damage)

    current_monster.hp -= damage

    add_message(
        f"Voce atacou com {player.weapon} e causou {damage} dano.",
        WHITE
    )

    enemy_turn()

# ============================================================
# ATAQUE ELEMENTAL
# ============================================================

def elemental_attack(index):
    attacks = ATTACKS[player.element]

    if index >= min(player.power_level, 4):
        add_message(
            "Esse poder ainda esta bloqueado!",
            RED
        )
        return

    name, base_damage, mana_cost = attacks[index]

    if player.mana < mana_cost:
        add_message(
            "Mana insuficiente!",
            RED
        )
        return

    player.mana -= mana_cost

    damage = calculate_damage(
        base_damage + player.damage,
        player.element,
        current_monster.element
    )

    damage -= current_monster.defense

    damage = max(1, damage)

    current_monster.hp -= damage

    add_message(
        f"{name} causou {damage} dano!",
        CYAN
    )

    # experiencia do poder
    player.gain_power_xp(
        random.randint(10, 20)
    )

    enemy_turn()

# ============================================================
# TURNO DO INIMIGO
# ============================================================

def enemy_turn():
    global state

    if current_monster.hp <= 0:
        victory()
        return

    # recupera mana a cada turno
    player.mana = min(
        player.max_mana,
        player.mana + random.randint(5, 20)
    )

    enemy_damage = current_monster.damage

    enemy_damage -= player.defense

    enemy_damage = max(
        1,
        enemy_damage + random.randint(-4, 8)
    )

    # chance de critico aumenta com a dificuldade
    critical_chance = min(
        50,
        10 + difficulty * 2
    )

    if random.randint(1, 100) <= critical_chance:
        enemy_damage *= 2

        add_message(
            "O MONSTRO DEU UM ATAQUE CRITICO!",
            RED
        )

    player.hp -= enemy_damage

    add_message(
        f"O inimigo causou {enemy_damage} dano.",
        RED
    )

    if player.hp <= 0:
        game_over()

# ============================================================
# VITORIA
# ============================================================

def victory():
    global state
    global mission_kills
    global mission_coins
    global difficulty
    global boss_defeated

    coins = random.randint(
        *current_monster.coins
    )

    xp = random.randint(
        *current_monster.xp
    )

    player.coins += coins
    player.gain_xp(xp)

    mission_kills += 1
    mission_coins += coins

    add_message(
        f"VITORIA! +{coins} moedas e +{xp} XP!",
        GREEN
    )

    if current_monster.name.startswith("Astaroth"):
        boss_defeated = True
        state = "VICTORY"

        return

    # Cada compra deixa os próximos monstros mais fortes.
    difficulty = len(player.owned_items) * 15

    # Se comprou tudo, libera o chefe
    if len(player.owned_items) == len(SHOP):
        global boss_unlocked
        boss_unlocked = True

        add_message(
            "TODOS OS ITENS FORAM COMPRADOS!",
            YELLOW
        )

        add_message(
            "O chefe Astaroth apareceu na floresta!",
            RED
        )

    state = "VILLAGE"

# ============================================================
# GAME OVER
# ============================================================

def game_over():
    global state

    state = "GAME_OVER"

# ============================================================
# CURA NA VILA
# ============================================================

def village_regeneration():
    global last_regen

    now = pygame.time.get_ticks()

    if now - last_regen >= 1000:
        player.hp = min(
            player.max_hp,
            player.hp + 10
        )

        player.mana = min(
            player.max_mana,
            player.mana + 10
        )

        last_regen = now

# ============================================================
# BOSS
# ============================================================

def start_boss():
    global current_monster
    global state

    if not boss_unlocked:
        add_message(
            "Voce ainda nao comprou todos os equipamentos!",
            RED
        )
        return

    current_monster = create_boss()

    state = "BATTLE"

    add_message(
        "ASTAROTH, O GUARDIAO DO VAZIO, SURGIU!",
        RED
    )

# ============================================================
# RESET
# ============================================================

def restart_game():
    global player
    global state
    global current_monster
    global difficulty
    global mission_kills
    global mission_coins
    global boss_unlocked
    global boss_defeated
    global message_log

    player = None
    current_monster = None

    difficulty = 0

    mission_kills = 0
    mission_coins = 0

    boss_unlocked = False
    boss_defeated = False

    message_log = []

    state = "ELEMENT_SELECT"

# ============================================================
# LOOP PRINCIPAL
# ============================================================

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ----------------------------------------
        # ESC
        # ----------------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if state == "SHOP":
                    state = "VILLAGE"

                elif state == "MISSIONS":
                    state = "VILLAGE"

                elif state == "BATTLE":
                    add_message(
                        "Use 4 para voltar para a vila.",
                        YELLOW
                    )

            # ------------------------------------
            # ESCOLHA ELEMENTO
            # ------------------------------------

            if state == "ELEMENT_SELECT":

                if event.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4
                ]:

                    elements = {
                        pygame.K_1: "Fogo",
                        pygame.K_2: "Agua",
                        pygame.K_3: "Eletrico",
                        pygame.K_4: "Planta"
                    }

                    player = Player(
                        elements[event.key]
                    )

                    state = "VILLAGE"

                    add_message(
                        f"Voce escolheu {player.element}!",
                        CYAN
                    )

            # ------------------------------------
            # VILA
            # ------------------------------------

            elif state == "VILLAGE":

                if event.key == pygame.K_e:
                    state = "SHOP"

                elif event.key == pygame.K_l:

                    if boss_unlocked:
                        add_message(
                            "Voce encontrou a entrada da arena do chefe!",
                            RED
                        )
                        start_boss()
                    else:
                        start_battle()

                elif event.key == pygame.K_m:
                    state = "MISSIONS"

                elif event.key == pygame.K_v:
                    player.hp = min(
                        player.max_hp,
                        player.hp + 10
                    )

                    player.mana = min(
                        player.max_mana,
                        player.mana + 10
                    )

                    add_message(
                        "Voce descansou na vila.",
                        GREEN
                    )

            # ------------------------------------
            # LOJA
            # ------------------------------------

            elif state == "SHOP":

                if event.key == pygame.K_UP:
                    selected_shop_item = max(
                        0,
                        selected_shop_item - 1
                    )

                elif event.key == pygame.K_DOWN:
                    selected_shop_item = min(
                        len(SHOP) - 1,
                        selected_shop_item + 1
                    )

                elif event.key == pygame.K_RETURN:

                    item = SHOP[
                        selected_shop_item
                    ]

                    bought = player.buy(item)

                    if bought:
                        difficulty = (
                            len(player.owned_items) * 15
                        )

                elif event.key == pygame.K_ESCAPE:
                    state = "VILLAGE"

            # ------------------------------------
            # MISSOES
            # ------------------------------------

            elif state == "MISSIONS":

                if event.key == pygame.K_ESCAPE:
                    state = "VILLAGE"

            # ------------------------------------
            # BATALHA
            # ------------------------------------

            elif state == "BATTLE":

                if event.key == pygame.K_1:
                    physical_attack()

                elif event.key == pygame.K_2:
                    elemental_attack(0)

                elif event.key == pygame.K_3:

                    # fugir
                    if random.randint(1, 100) <= 70:

                        add_message(
                            "Voce conseguiu fugir!",
                            GREEN
                        )

                        state = "VILLAGE"

                    else:

                        add_message(
                            "Nao conseguiu fugir!",
                            RED
                        )

                        enemy_turn()

                elif event.key == pygame.K_4:

                    state = "VILLAGE"

                    add_message(
                        "Voce voltou para a vila.",
                        GREEN
                    )

                # teclas 5,6,7 para poderes adicionais
                elif event.key == pygame.K_5:
                    elemental_attack(1)

                elif event.key == pygame.K_6:
                    elemental_attack(2)

                elif event.key == pygame.K_7:
                    elemental_attack(3)

            # ------------------------------------
            # GAME OVER
            # ------------------------------------

            elif state == "GAME_OVER":

                if event.key == pygame.K_r:
                    restart_game()

            # ------------------------------------
            # VITORIA FINAL
            # ------------------------------------

            elif state == "VICTORY":

                if event.key == pygame.K_r:
                    restart_game()

    # ========================================================
    # DESENHO
    # ========================================================

    if state == "ELEMENT_SELECT":
        draw_element_select()

    elif state == "VILLAGE":
        village_regeneration()
        draw_village()

    elif state == "SHOP":
        draw_shop()

    elif state == "BATTLE":
        draw_battle()

    elif state == "MISSIONS":
        draw_missions()

    elif state == "GAME_OVER":

        screen.fill((20, 10, 10))

        draw_text(
            "VOCE MORREU!",
            400,
            230,
            RED,
            BIG_FONT
        )

        draw_text(
            "Todo o progresso foi perdido.",
            350,
            290
        )

        draw_text(
            "Pressione R para recomecar desde o inicio.",
            300,
            350,
            YELLOW
        )

    elif state == "VICTORY":

        screen.fill((15, 30, 20))

        draw_text(
            "VOCE DERROTOU ASTAROTH!",
            300,
            200,
            YELLOW,
            BIG_FONT
        )

        draw_text(
            "A lenda dos quatro elementos chegou ao fim!",
            300,
            270,
            GREEN
        )

        draw_text(
            f"Nivel final: {player.level}",
            430,
            340
        )

        draw_text(
            "Pressione R para jogar novamente.",
            350,
            420,
            WHITE
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
