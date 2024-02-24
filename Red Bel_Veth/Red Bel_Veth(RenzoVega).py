import pygame
import random

# Clase para el jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (64, 64))  # Cambiar el tamaño del jugador
        self.rect = self.image.get_rect()
        self.rect.centerx = 800 // 2  # Centrar el jugador en el eje x
        self.rect.centery = 600 // 2  # Centrar el jugador en el eje y
        self.speed_x = 0
        self.speed_y = 0
        self.score = 0
        self.lives = 3
        self.shoot_delay = 500  # Retardo inicial entre disparos
        self.last_shot_time = pygame.time.get_ticks()  # Último momento en que se realizó un disparo

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Limitar la posición del jugador dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > 600:
            self.rect.bottom = 600

    def shoot(self, projectiles):
        # Verificar el tiempo transcurrido desde el último disparo
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            projectile = Projectile("Recursos/Proyectil.png")
            projectile.rect.center = self.rect.center
            projectiles.add(projectile)
            self.last_shot_time = current_time

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(-100, -40)
        self.speed_x = random.randint(-2, 2)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Invertir la dirección si se sale de la pantalla
        if self.rect.left < 0 or self.rect.right > 800:
            self.speed_x = -self.speed_x
        if self.rect.top > 600:
            self.rect.x = random.randint(0, 800)
            self.rect.y = random.randint(-100, -40)
            self.speed_x = random.randint(-2, 2)
            self.speed_y = random.randint(1, 3)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load("Recursos/PowerUp.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = 2

    def update(self):
        self.rect.y += self.speed_y

        # Eliminar el power-up si sale de la pantalla
        if self.rect.top > 600:
            self.kill()

    def activate_power_up(self, player):
        # Aumentar la velocidad de disparo del jugador
        player.shoot_delay -= 100  # Reducir el retardo entre disparos

        # Establecer un límite mínimo para la velocidad de disparo
        if player.shoot_delay < 100:
            player.shoot_delay = 100

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()
        self.speed_y = 8

    def update(self):
        self.rect.y -= self.speed_y

        # Si el proyectil sale de la pantalla, se elimina
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = [
            pygame.image.load("Recursos/Explosión 1.png").convert(),
            pygame.image.load("Recursos/Explosión 2.png").convert(),
            pygame.image.load("Recursos/Explosión 3.png").convert(),
            pygame.image.load("Recursos/Explosión 4.png").convert(),
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.finished = False  # Atributo para indicar si la explosión ha finalizado
        self.animation_duration = len(self.images) * self.frame_rate

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.finished = True  # La explosión ha finalizado
            else:
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect(center=self.rect.center)


class Background:
    def __init__(self, image_path, speed):
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()
        self.rect.y = -600
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

        # Reiniciar la posición de la imagen si sale de la pantalla
        if self.rect.top > 0:
            self.rect.y = -600

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)

    def update(self):
        pass

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

class Sound:
    def __init__(self, sound_path):
        pygame.mixer.music.load(sound_path)

    def play(self):
        pygame.mixer.music.play()

class Game:
    velocidad_jugador = 5
    velocidad_enemigo = 3
    velocidad_proyectil = 8
    velocidad_power_up = 2
    velocidad_fondo = 2

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Red BelVeth")
        self.clock = pygame.time.Clock()
        self.is_running = True

        # Requerimientos y configuraciones
        ruta_imagen_jugador = "Recursos/Player.png"
        ruta_imagen_proyectil = "Recursos/Proyectil.png"  
        ruta_imagen_fondo = "Recursos/Fondo.png"
        ruta_sonido_fondo = "Recursos/Sound.wav"

        # Creación de instancias de clases
        self.player = Player(ruta_imagen_jugador)
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.background = Background(ruta_imagen_fondo, self.velocidad_fondo)
        self.hud = HUD(self.player)
        self.sound = Sound(ruta_sonido_fondo)

        # Variables para controlar el tiempo y spawn de los enemigos y power-ups
        self.enemy_spawn_time = pygame.time.get_ticks()
        self.powerup_spawn_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot(self.projectiles)
                elif event.key == pygame.K_LEFT:
                    self.player.speed_x = -self.velocidad_jugador
                elif event.key == pygame.K_RIGHT:
                    self.player.speed_x = self.velocidad_jugador
                elif event.key == pygame.K_UP:  # Agregar movimiento hacia arriba
                    self.player.speed_y = -self.velocidad_jugador
                elif event.key == pygame.K_DOWN:  # Agregar movimiento hacia abajo
                    self.player.speed_y = self.velocidad_jugador

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.speed_x < 0:
                    self.player.speed_x = 0
                elif event.key == pygame.K_RIGHT and self.player.speed_x > 0:
                    self.player.speed_x = 0
                elif event.key == pygame.K_UP and self.player.speed_y < 0:
                    self.player.speed_y = 0
                elif event.key == pygame.K_DOWN and self.player.speed_y > 0:
                    self.player.speed_y = 0

    def update(self):
        self.player.update()
        self.enemies.update()
        self.projectiles.update()
        self.powerups.update()
        self.background.update()
        self.hud.update()

        # Detectar colisiones entre el jugador y los enemigos
        if pygame.sprite.spritecollide(self.player, self.enemies, True):
            explosion = Explosion(self.player.rect.center)
            self.explosions.add(explosion)
            self.player.lives -= 1

            if self.player.lives == 0:
                self.is_running = False

        # Detectar colisiones entre los proyectiles y los enemigos
        for projectile in self.projectiles:
            enemies_hit = pygame.sprite.spritecollide(projectile, self.enemies, True)
            for enemy in enemies_hit:
                explosion = Explosion(enemy.rect.center)
                self.explosions.add(explosion)
                self.player.score += 1

        # Detectar colisiones entre el jugador y los power-ups
        powerup_hit = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in powerup_hit:
            powerup.activate_power_up(self.player)

        # Generar nuevos enemigos cada 2 segundos
        if pygame.time.get_ticks() - self.enemy_spawn_time > 2000:
            self.spawn_enemy()
            self.enemy_spawn_time = pygame.time.get_ticks()

        # Generar nuevos power-ups cada 5 segundos
        if pygame.time.get_ticks() - self.powerup_spawn_time > 5000:
            self.spawn_powerup()
            self.powerup_spawn_time = pygame.time.get_ticks()

    def spawn_enemy(self):
        enemy = Enemy("Recursos/Enemy.png")
        self.enemies.add(enemy)

    def spawn_powerup(self):
        powerup = PowerUp( "Recursos/PowerUp.png")
        self.powerups.add(powerup)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        self.enemies.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.powerups.draw(self.screen)
        self.explosions.draw(self.screen)
        self.hud.draw(self.screen)
        pygame.display.flip()

    def run(self):
        self.sound.play()

        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()