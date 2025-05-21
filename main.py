import pygame
import random
import sys

pygame.init()
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Atrapa la pelota")

AZUL_CIELO = (70, 160, 220)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

fuente_principal = pygame.font.SysFont("Comfortaa", 36)
fuente_titulo = pygame.font.SysFont("Comfortaa", 72, bold=True)

canasta_img = pygame.image.load("img/basket.png").convert_alpha()
canasta_img = pygame.transform.scale(canasta_img, (100, 60))
fruta_img = pygame.image.load("img/ball.png").convert_alpha()
fruta_img = pygame.transform.scale(fruta_img, (64, 64))

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_actual = color_base

    def dibujar(self):
        pygame.draw.rect(VENTANA, self.color_actual, self.rect, border_radius=10)
        texto = fuente_principal.render(self.texto, True, BLANCO)
        VENTANA.blit(texto, (self.rect.centerx - texto.get_width() // 2, 
                            self.rect.centery - texto.get_height() // 2))

    def verificar_hover(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse):
            self.color_actual = self.color_hover
            return True
        self.color_actual = self.color_base
        return False

def mostrar_menu():
    titulo = fuente_titulo.render("ATRAPA LA FRUTA", True, BLANCO)
    boton_jugar = Boton(ANCHO // 2 - 100, ALTO // 2, 200, 50, "JUGAR", VERDE, (0, 200, 0))
    boton_salir = Boton(ANCHO // 2 - 100, ALTO // 2 + 80, 200, 50, "SALIR", ROJO, (200, 0, 0))

    while True:
        VENTANA.fill(AZUL_CIELO)
        VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))

        pos_mouse = pygame.mouse.get_pos()
        for boton in [boton_jugar, boton_salir]:
            boton.verificar_hover(pos_mouse)
            boton.dibujar()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.verificar_hover(pos_mouse):
                    return "jugar"
                if boton_salir.verificar_hover(pos_mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def jugar():
    canasta_x = ANCHO // 2
    canasta_y = ALTO - 70
    fruta_x = random.randint(0, ANCHO - 64)
    fruta_y = -64
    velocidad_fruta = 5
    puntaje = 0
    vidas = 3

    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        reloj.tick(60)
        VENTANA.fill(AZUL_CIELO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and canasta_x > 0:
            canasta_x -= 8
        if teclas[pygame.K_RIGHT] and canasta_x < ANCHO - 100:
            canasta_x += 8

        fruta_y += velocidad_fruta
        if fruta_y > ALTO:
            fruta_y = -64
            fruta_x = random.randint(0, ANCHO - 64)
            vidas -= 1
        canasta_rect = pygame.Rect(canasta_x, canasta_y, 100, 60)
        fruta_rect = pygame.Rect(fruta_x, fruta_y, 64, 64)
        if canasta_rect.colliderect(fruta_rect):
            puntaje += 1
            fruta_y = -64
            fruta_x = random.randint(0, ANCHO - 64)
            velocidad_fruta += 0.2  

        if canasta_img:
            VENTANA.blit(canasta_img, (canasta_x, canasta_y))
        else:
            pygame.draw.rect(VENTANA, (0, 0, 139), (canasta_x, canasta_y, 100, 60))

        if fruta_img:
            VENTANA.blit(fruta_img, (fruta_x, fruta_y))
        else:
            pygame.draw.circle(VENTANA, (255, 165, 0), (fruta_x + 32, fruta_y + 32), 32)

        texto_puntaje = fuente_principal.render(f"Puntaje: {puntaje}", True, BLANCO)
        texto_vidas = fuente_principal.render(f"Vidas: {vidas}", True, BLANCO)
        VENTANA.blit(texto_puntaje, (20, 20))
        VENTANA.blit(texto_vidas, (ANCHO - 150, 20))

        pygame.display.update()

        if vidas <= 0:
            ejecutando = False

    texto_game_over = fuente_titulo.render("GAME OVER", True, ROJO)
    texto_final = fuente_principal.render(f"Puntaje final: {puntaje}", True, BLANCO)
    VENTANA.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 3))
    VENTANA.blit(texto_final, (ANCHO // 2 - texto_final.get_width() // 2, ALTO // 2))
    pygame.display.update()
    pygame.time.delay(3000)  

if __name__ == "__main__":
    while True:
        opcion = mostrar_menu()
        if opcion == "jugar":
            jugar()