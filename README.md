# ⚔️ A Lenda dos Quatro Elementos

Um RPG 2D simples desenvolvido em **Python com Pygame**, no qual você começa sem equipamentos e precisa derrotar monstros, ganhar experiência e moedas, evoluir seu personagem e comprar equipamentos para enfrentar o chefe final.

## 🎮 Sobre o jogo

Você começa sua aventura com:

* ❤️ **100 de vida**
* 💧 **100 de mana**
* 👊 **Punhos como arma**
* 🛡️ Defesa inicial básica
* 💰 Nenhuma moeda
* ⭐ Nível 1

No início, você escolhe um dos quatro elementos:

🔥 **Fogo**
💧 **Água**
⚡ **Elétrico**
🌿 **Planta**

Cada elemento possui vantagens e desvantagens contra outro elemento.

## 🔥 Sistema de elementos

As fraquezas funcionam assim:

| Elemento atacante | Causa dano extra contra |
| ----------------- | ----------------------- |
| 💧 Água           | 🔥 Fogo                 |
| 🔥 Fogo           | 🌿 Planta               |
| ⚡ Elétrico        | 💧 Água                 |
| 🌿 Planta         | ⚡ Elétrico              |

Quando você ataca um inimigo que possui uma fraqueza ao seu elemento, recebe um bônus aleatório de **15 a 30 de dano**.

Nesse caso aparece:

> **CRITICO!**

Se você estiver lutando contra um inimigo do **mesmo elemento**, existe a possibilidade de ele criar um escudo elemental que reduz seu dano entre **10% e 20%**.

## ⚔️ Sistema de combate

Os monstros são escolhidos **automaticamente e aleatoriamente**.

Você não pode escolher qual monstro enfrentará.

Durante a batalha você pode:

* 👊 Atacar fisicamente
* 🔥 Usar poderes elementais
* 🏃 Tentar fugir
* 🏠 Voltar para a vila

### Ataque físico

O ataque físico:

* Não consome mana
* Utiliza o dano do personagem e equipamento
* Pode ser usado enquanto você estiver sem mana

### Ataques elementais

Os ataques elementais consomem mana.

Cada poder possui um custo de aproximadamente **35 a 45 de mana**.

A mana é recuperada a cada turno em uma quantidade aleatória de **5 a 20**.

## ✨ Evolução dos poderes

Os poderes elementais possuem seu próprio sistema de experiência.

Ao usar poderes, você recebe entre **10 e 20 XP de poder**.

Os poderes podem chegar até o:

**Nível 5**

Conforme o poder evolui, novos ataques do mesmo elemento são desbloqueados.

O personagem pode ter no máximo:

**4 ataques elementais diferentes.**

## 📈 Evolução do personagem

Ao derrotar monstros você recebe experiência.

Quando sua experiência chega ao valor necessário, você sobe de nível.

Ao subir de nível:

* ❤️ Aumenta a vida máxima
* 💙 Aumenta a mana máxima
* ⚔️ Aumenta o dano
* 🛡️ Aumenta a defesa
* 🔄 Vida e mana são restauradas

## 💰 Moedas

Cada monstro fornece uma quantidade diferente de moedas.

Monstros mais fortes normalmente dão mais dinheiro.

O dinheiro pode ser utilizado na loja para comprar novos equipamentos.

## 🛒 Loja

A loja é uma parte permanente do jogo.

Você começa usando apenas os **punhos**, mas pode comprar equipamentos conforme ganha moedas.

Exemplos:

* ⚔️ Espada de Ferro
* 🔮 Cajado Elemental
* 🛡️ Armadura de Couro
* ⚔️ Espada do Herói
* 🛡️ Armadura Elemental

Cada equipamento possui um preço específico.

Você **não pode comprar um item se não tiver moedas suficientes**.

Cada equipamento comprado aumenta os atributos do jogador.

## 👹 Dificuldade progressiva

Os monstros ficam mais fortes conforme você compra equipamentos.

Cada item comprado aumenta a dificuldade dos próximos inimigos.

Isso impede que o jogador fique simplesmente comprando equipamentos e derrotando todos os inimigos facilmente.

A chance de monstros realizarem ataques críticos também aumenta conforme a dificuldade.

## 🏘️ Vila

A vila funciona como área segura.

Nela você pode:

* 🛒 Acessar a loja
* ⚔️ Procurar um novo monstro
* 📜 Ver suas missões
* ❤️ Recuperar vida
* 💙 Recuperar mana

Ao permanecer na vila, você recupera:

**+10 de vida por segundo**

**+10 de mana por segundo**

## 📜 Missões

O jogo possui um sistema básico de missões.

### Missão 1 — Derrote 3 monstros

Objetivo:

`0/3`

Recompensa:

**100 moedas**

### Missão 2 — Junte 300 moedas

Objetivo:

`0/300`

A quantidade é atualizada conforme você consegue moedas durante as batalhas.

## 🏃 Fugir

Durante uma batalha existe a opção de tentar fugir.

A fuga possui uma chance de sucesso.

Se conseguir:

> **Você conseguiu fugir!**

Se falhar, o monstro terá a oportunidade de atacar.

## ☠️ Morte

Se sua vida chegar a zero:

> **VOCÊ MORREU!**

Todo o progresso da partida é perdido.

Você precisa começar novamente desde o início.

## 👑 Chefe final

Depois de comprar **todos os equipamentos da loja**, o chefe final é desbloqueado.

### Astaroth, o Guardião do Vazio

Astaroth é um inimigo muito mais poderoso que os monstros normais.

Ele possui:

* ❤️ Grande quantidade de vida
* ⚔️ Alto dano
* 🛡️ Defesa elevada
* 💥 Possibilidade de ataques críticos
* 🌈 Um elemento escolhido durante a batalha

Derrotar Astaroth encerra a aventura.

## 🕹️ Controles

| Tecla | Ação                           |
| ----- | ------------------------------ |
| `1`   | Ataque físico                  |
| `2`   | Primeiro poder elemental       |
| `3`   | Fugir                          |
| `4`   | Voltar para a vila             |
| `5`   | Segundo poder                  |
| `6`   | Terceiro poder                 |
| `7`   | Quarto poder                   |
| `E`   | Abrir loja                     |
| `L`   | Procurar monstro               |
| `V`   | Descansar                      |
| `M`   | Missões                        |
| `ESC` | Voltar                         |
| `R`   | Reiniciar após derrota/vitória |

## 💻 Requisitos

* Python **3.9 ou superior**
* Pygame

## 📦 Instalação

Clone o repositório:

```bash
git clone SEU_LINK_DO_REPOSITORIO
cd SEU_REPOSITORIO
```

Instale o Pygame:

```bash
pip install pygame
```

Execute o jogo:

```bash
python rpg.py
```

## 📁 Estrutura

```text
A-Lenda-dos-Quatro-Elementos/
│
├── rpg.py
├── README.md
└── .gitignore
```

## 🛠️ Tecnologias

* 🐍 Python
* 🎮 Pygame
* 🖥️ Gráficos 2D simples
* ⚔️ Sistema de combate por turnos
* 📈 Sistema de experiência e níveis
* 🛒 Sistema de loja
* ✨ Sistema elemental
* 📜 Sistema de missões

## 🚀 Possíveis melhorias futuras

Algumas ideias para futuras versões:

* 🎨 Sprites 2D mais detalhados
* 🗺️ Mapa explorável
* 🎵 Música e efeitos sonoros
* 🧙 NPCs
* 💾 Sistema de salvamento
* 🏆 Mais chefes
* 👾 Mais monstros
* ⚔️ Mais armas
* 🛡️ Mais armaduras
* 🔮 Mais poderes
* 📜 Mais missões
* 🌎 Novas áreas
* 🧪 Poções e consumíveis
* 💎 Itens raros
* 🎲 Sistema de raridade dos equipamentos

## 📜 Licença

Este projeto pode ser utilizado, estudado e modificado livremente para fins de aprendizado e desenvolvimento pessoal.

---

# ⭐ Aventure-se pelos quatro elementos!

**Escolha seu elemento. Derrote monstros. Evolua. Compre equipamentos. Enfrente Astaroth.**

🔥 💧 ⚡ 🌿
