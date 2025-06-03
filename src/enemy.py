from settings import *
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, player):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((200, 50, 50))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)

        self.collision_sprites = collision_sprites
        self.player = player

        self.speed = 100  # pixels/sec
        self.current_hp = 50
        self.attack_damage = 5
        self.attack_cooldown = 2.0
        self.last_attack_time = 0

        # Pour mouvements erratiques
        self.noise_timer = 0
        self.noise_interval = 0.5
        self.noise_vector = pygame.Vector2(0, 0)

    def update(self, dt):
        self.move_bot_like(dt)
        self.attack_player()

    def move_bot_like(self, dt):
        # Direction vers le joueur
        direction = pygame.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery
        )

        if direction.length() > 0:
            direction = direction.normalize()

        # Ajout de bruit aléatoire
        self.noise_timer += dt
        if self.noise_timer >= self.noise_interval:
            self.noise_timer = 0
            self.noise_vector = pygame.Vector2(
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5)
            )

        final_direction = direction + self.noise_vector
        if final_direction.length() > 0:
            final_direction = final_direction.normalize()

        # Déplacement avec collision
        dx = final_direction.x * self.speed * dt
        dy = final_direction.y * self.speed * dt

        self.move_single_axis(dx, 0)
        self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                if dx > 0:  # déplacement droite
                    self.rect.right = sprite.rect.left
                if dx < 0:  # déplacement gauche
                    self.rect.left = sprite.rect.right
                if dy > 0:  # vers le bas
                    self.rect.bottom = sprite.rect.top
                if dy < 0:  # vers le haut
                    self.rect.top = sprite.rect.bottom


    def attack_player(self):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.last_attack_time >= self.attack_cooldown:
            if self.rect.colliderect(self.player.rect):
                self.last_attack_time = current_time
                self.player.current_hp -= self.attack_damage
                print(f"Player hit! HP: {self.player.current_hp}")

    def take_damage(self, amount):
        self.current_hp -= amount
        print(f"Enemy took {amount} damage! HP left: {self.current_hp}")
        if self.current_hp <= 0:
            self.kill()
