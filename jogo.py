import pygame
import random

pygame.init()

#Dimensões da tela
x = 1280
y = 720

screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("SpaceShip")

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

pontos = 1

rodando = True

font = pygame.font.Font(None, 50)

nave_rect = nave.get_rect()
alien_rect = alien.get_rect()
missil_rect = missil.get_rect()

def respawn():
    return [random.randint(0, x - 50), random.randint(-50, y -50)]

def respawn_missil():
    global triggered
    triggered = False
    respawn_missil_x = pos_nave_x + 37
    respawn_missil_y = pos_nave_y
    vel_y_missil = 0
    return [respawn_missil_x, respawn_missil_y, triggered, vel_y_missil]

def colisao():
    global pontos
    if nave_rect.colliderect(alien_rect) or alien_rect.x == 60:
        pontos -= 1
        return True
    elif missil_rect.colliderect(alien_rect):
        pontos += 1
        return True
    else:
        return False

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
    
    if pontos == -1:
        rodando = False

    # Respawn colisão
    if pos_alien_x == 50:
        pos_alien_x = respawn()[0]
        pos_alien_y = respawn()[1]

    if pos_x_missil == 1300:
        pos_x_missil, pos_y_missil, triggered, vel_y_missil = respawn_missil()

    if pos_alien_x == 50 or colisao():
        pontos_mudam = True
        pos_alien_x = respawn()[0]
        pos_alien_y = respawn()[1]

    # Posições rect
    nave_rect.y = pos_nave_y
    nave_rect.x = pos_nave_x

    missil_rect.x = pos_x_missil
    missil_rect.y = pos_y_missil

    alien_rect.x = pos_alien_x
    alien_rect.y = pos_alien_y

    # Atualização do missil enquanto não disparado
    if not triggered:
        pos_x_missil = pos_nave_x + 37
        pos_y_missil = pos_nave_y
        visivel = False
    
    # Movimento do cenario no eixo vertical
    scroll_y += 0.5

    # Movimento vertical do alien
    pos_alien_y += vel_alien_y
    
    # Quando disparar o míssil
    if triggered:
        visivel = True
        pos_y_missil += vel_y_missil

    # Respawn vertical do alien
    if pos_alien_y > y:
        pos_alien_x = random.randint(0, x - 50)
        pos_alien_y = -50

    # Respawn vertical do missil
    if pos_y_missil < -25:
        pos_x_missil, pos_y_missil, triggered, vel_y_missil = respawn_missil()
    
    cor_brilho = (abs(int(pygame.time.get_ticks() % 510 - 255)), 0, 0)
    pygame.draw.rect(screen, cor_brilho, alien_rect, 4)

    score = font.render(f'Pontos: {int(pontos)}', True, (255, 255, 255))
    screen.blit(score, (50, 50))

    # Criar imagens
    screen.blit(alien, (pos_alien_x, pos_alien_y))
    if visivel:
        screen.blit(missil, (pos_x_missil, pos_y_missil))
    screen.blit(nave, (pos_nave_x, pos_nave_y))

    pontos_mudam = False

    if pontos_mudam:
        print(f"Pontos: {pontos}")
        pontos_mudam = False
    
    pygame.display.flip()