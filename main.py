import pygame
import sys

#Inicializa Pygame
pygame.init()

#Carga las imágenes
fondo = pygame.image.load("assets/images/background.jpg")
fondo = pygame.transform.scale(fondo,(fondo.get_width()//5.5, fondo.get_height()//5.5))
jugador_imagen = pygame.image.load("assets/images/player.png")
jugador_imagen = pygame.transform.scale(jugador_imagen,(jugador_imagen.get_width()//30, jugador_imagen.get_height()//30))
enemigo_imagen = pygame.image.load("assets/images/enemy.png")
enemigo_imagen = pygame.transform.scale(enemigo_imagen,(enemigo_imagen.get_width()//30, enemigo_imagen.get_height()//40))

#Crea una ventana de 800x600
screen = pygame.display.set_mode((800, 600))

#Define el título de la ventana
pygame.display.set_caption("Juego de Aventura: La ardilla y el cocodrilo")

#Define constantes
PLAYER_SIZE = 50
ENEMY_SIZE = 50

#Define el jugador y enemigos
player = {"x": 100, "y": 100, "score": 0, "health": 1}
enemies = []
collectibles = []

#Niveles
levels = [
    {
        "enemies": [{"x": 300, "y": 300}],
        "collectibles": [{"x": 200, "y": 200, "type": "coin"}],
    },
    {
        "enemies": [{"x": 100, "y": 100}, {"x": 500, "y": 500}],
        "collectibles": [{"x": 300, "y": 200, "type": "powerup"}],
    },
]

current_level = 0

def load_level(level_index):
    global enemies, collectibles
    enemies = levels[level_index]["enemies"]
    collectibles = [
        {"x": 200, "y": 200, "type": "coin"},
        {"x": 400, "y": 100, "type": "coin"},
        {"x": 600, "y": 300, "type": "coin"},
    ]

def show_start_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("la ardilla y el cocodrilo", True, (0, 0, 255))
    screen.blit(text, (200, 250))
    pygame.display.flip()
    pygame.time.wait(2000)

def show_game_over_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("¡Fin del juego!", True, (255, 0, 0))
    screen.blit(text, (300, 250))
    pygame.display.flip()
    pygame.time.wait(2000)

def show_victory_message():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("¡Ganaste!", True, (0, 255, 0))
    screen.blit(text, (300, 250))
    pygame.display.flip()
    pygame.time.wait(2000)


def update_player(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player["x"] -= 5
    if keys[pygame.K_RIGHT]:
        player["x"] += 5
    if keys[pygame.K_UP]:
        player["y"] -= 5
    if keys[pygame.K_DOWN]:
        player["y"] += 5

def update_enemies(enemies, player):
    for enemy in enemies:
        if enemy["x"] < player["x"]:
            enemy["x"] += 1
        elif enemy["x"] > player["x"]:
            enemy["x"] -= 1
        if enemy["y"] < player["y"]:
            enemy["y"] += 1
        elif enemy["y"] > player["y"]:
            enemy["y"] -= 1

def check_collisions(player, enemies):
    for enemy in enemies:
        if (
            player["x"] < enemy["x"] + ENEMY_SIZE
            and player["x"] + PLAYER_SIZE > enemy["x"]
            and player["y"] < enemy["y"] + ENEMY_SIZE
            and player["y"] + PLAYER_SIZE > enemy["y"]
        ):
            player["health"] -= 1
            if player["health"] <= 0:
                return True  # Game Over
    return False

def draw_collectibles(collectibles):
    for collectible in collectibles:
        pygame.draw.circle(screen, (255, 255, 0), (collectible["x"], collectible["y"]), 10)

def check_collectibles(player, collectibles):
    for collectible in collectibles:
        if (
            player["x"] < collectible["x"] + 10
            and player["x"] + PLAYER_SIZE > collectible["x"]
            and player["y"] < collectible["y"] + 10
            and player["y"] + PLAYER_SIZE > collectible["y"]
        ):
            if collectible["type"] == "coin":
                player["score"] += 1
            elif collectible["type"] == "powerup":
                player["powerup_active"] = True  # Activar un poder especial
            collectibles.remove(collectible)
            if player ["score"] == 3: 
                show_victory_message()
            return

def draw_level():
    screen.blit(fondo, (0, 0))  # Dibuja la imagen de fondo
    screen.blit(jugador_imagen, (player["x"], player["y"]))  # Dibuja la imagen del jugador
    for enemy in enemies:
        screen.blit(enemigo_imagen, (enemy["x"], enemy["y"]))  # Dibuja la imagen del enemigo
    draw_collectibles(collectibles)
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Puntos: {player['score']}", True, (0, 0, 255))
    health_text = font.render(f"Salud: {player['health']}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 40))

def main():
    show_start_screen()
    load_level(current_level)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        update_player(player)
        update_enemies(enemies, player)
        if check_collisions(player, enemies):
            show_game_over_screen()
            break
        check_collectibles(player, collectibles)
        if player ["score"] == 3: 
            show_victory_message()
            break
        draw_level()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()