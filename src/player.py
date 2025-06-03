from settings import *
from enemy import Enemy

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        # settings
        self.frame_width = 100
        self.frame_height = 100
        self.zoom = 3
        self.is_alive = True


        # Load images
        self.animations = {
            'idle': self.load_frames('Soldier-Idle.png'),
            'walk': self.load_frames('Soldier-Walk.png'),
            'attack': self.load_frames('Soldier-Attack02.png'),
            'hurt': self.load_frames('Soldier-Hurt.png')
        }

        self.state = 'idle'
        self.frames = self.animations[self.state]
        self.frame_index = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-275, -275)

        self.animation_speed = 0.025
        self.animation_timer = 0
        self.last_frames = self.frames

        # Inventory / stats
        self.inventory = {"épée": 1, "clef": 1}
        self.attack_cooldown = 0.5
        self.last_attack_time = 0
        self.attack_damage = 10
        self.max_hp = 100
        self.current_hp = 100
        self.hurt_timer = 0

        # Mouvements
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites
    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frames = self.animations[self.state]
            self.frame_index = 0
        
    def attack(self, enemies_group):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            self.set_state('attack')

            attack_rect = self.rect.inflate(100, 100)
            for enemy in enemies_group:
                if attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.attack_damage)
                    
    def take_damage(self, amount):
        self.current_hp -= amount
        self.set_state('hurt')
        if self.current_hp <= 0:
            self.current_hp = 0
            self.is_alive = False



    
    def add_item(self, item_name, quantity=1):       
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity

    def remove_item(self, item_name, quantity=1):
        if item_name in self.inventory:
            self.inventory[item_name] -= quantity
            if self.inventory[item_name] <= 0:
                del self.inventory[item_name]

    # def set_position(self, pos):
    #     self.rect.center = pos
    #     self.hitbox_rect = self.rect.inflate(-275, -275)
    def load_frames(self, filename):
        sheet = pygame.image.load(join('assets', 'chara', filename)).convert_alpha()
        frames = []
        sheet_width = sheet.get_width()
        zoom = self.zoom

        for i in range(sheet_width // self.frame_width):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            
            # Zoom
            frame = pygame.transform.scale(frame, (self.frame_width * zoom, self.frame_height * zoom))
            frames.append(frame)

        return frames

    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            if self.state in ['attack', 'hurt']:
                self.set_state('idle')  
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]


    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_q])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_z])
        self.direction = self.direction.normalize() if self.direction else self.direction

        if self.state not in ['attack', 'hurt']:  # on n’interrompt pas ces animations
            if self.direction.length_squared() == 0:
                self.set_state('idle')
            else:
                self.set_state('walk')


    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt 
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    

    def update(self, dt):
        if self.is_alive:
            self.input()
            self.animate()
            self.move(dt)
        else:
            pass

