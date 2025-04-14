import pygame
import random

pygame.init()

#Dimensões da tela
x = 1280
y = 720

screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Meu jogo em Python")

cenario = pygame.image.load('imagens/espaço.jpg').convert_alpha()
cenario = pygame.transform.scale(cenario, (x, y))

alien = pygame.image.load('imagens/alien.png').convert_alpha()
alien = pygame.transform.scale(alien, (50, 50))

nave = pygame.image.load('imagens/nave.png').convert_alpha()
nave = pygame.transform.scale(nave, (100, 100)) # Conversão de tamanho da nave
nave = pygame.transform.rotate(nave, 0) 

missil = pygame.image.load('imagens/missil.png').convert_alpha()
missil = pygame.transform.scale(missil, (25, 25))
missil = pygame.transform.rotate(missil, -45)

# Posições iniciais
pos_alien_x = 500
pos_alien_y = 300

pos_nave_x = 640
pos_nave_y = y - 100

vel_y_missil = 0
pos_x_missil = pos_nave_x + 37
pos_y_missil = pos_nave_y

triggered = False

# Variável para movimento vertical
scroll_y = 0

# Velocidade vertical do alien
vel_alien_y = 0.5

rodando = True

def respawn_missil():
    global triggered
    triggered = False
    respawn_missil_x = pos_nave_x + 37
    respawn_missil_y = pos_nave_y
    vel_y_missil = 0
    return [respawn_missil_x, respawn_missil_y, triggered, vel_y_missil]

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Coordenada relativa no eixo y
    rel_y = scroll_y % cenario.get_rect().height
    screen.blit(cenario, (0, rel_y - cenario.get_rect().height)) # Desenha a primeira parte do cenario
    if rel_y < y:
        screen.blit(cenario, (0, rel_y)) # Desenha a segunda parte do cenario

    # Teclas
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_LEFT] and pos_nave_x > 1:  # Movimento para a esquerda
        pos_nave_x -= 1

    if tecla[pygame.K_RIGHT] and pos_nave_x < x - 80:  # Movimento para a direita
        pos_nave_x += 1

    if tecla[pygame.K_SPACE]:
        triggered = True
        vel_y_missil = -2

    # Atualização do missil enquanto não disparado
    if not triggered:
        pos_x_missil = pos_nave_x + 37
        pos_y_missil = pos_nave_y
    
    # Movimento do cenario no eixo vertical
    scroll_y += 0.5

    # Movimento vertical do alien
    pos_alien_y += vel_alien_y
    
    # Movimento do míssil disparado
    if triggered:
        pos_y_missil += vel_y_missil

    # Respawn vertical do alien
    if pos_alien_y > y:
        pos_alien_x = random.randint(0, x - 50)
        pos_alien_y = -50

    # Respawn vertical do missil
    if pos_y_missil < -25:
        pos_x_missil, pos_y_missil, triggered, vel_y_missil = respawn_missil()

    # Criar imagens
    screen.blit(alien, (pos_alien_x, pos_alien_y))
    screen.blit(missil, (pos_x_missil, pos_y_missil))
    screen.blit(nave, (pos_nave_x, pos_nave_y))
    
    pygame.display.flip()