import pygame

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

# Posições iniciais
pos_alien_x = 500
pos_alien_y = 300

pos_nave_x = 640
pos_nave_y = y - 100


# Variável para movimento vertical
scroll_y = 0

# Velocidade vertical do alien
vel_alien_y = -1

rodando = True

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
        pos_nave_x -= 3
    if tecla[pygame.K_RIGHT] and pos_nave_x < x - 80:  # Movimento para a direita
        pos_nave_x += 3
    
    # Movimento do cenario no eixo vertical
    scroll_y += 1

    # Movimento vertical do alien
    pos_alien_y += vel_alien_y

    # Se atingir os limites da tela, inverte a direção
    if pos_alien_y <= 0 or pos_alien_y >= y -50:
        vel_alien_y *= -1

    # Criar imagens
    screen.blit(alien, (pos_alien_x, pos_alien_y))
    screen.blit(nave, (pos_nave_x, pos_nave_y))
    
    pygame.display.flip()