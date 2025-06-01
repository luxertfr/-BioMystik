from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        # Load
        self.sheet = pygame.image.load(join('assets', 'chara', 'Soldier-Idle.png')).convert_alpha()

        # settings
        self.frame_width = 100 
        self.frame_height = 100
        self.frames = self.load_frames()
        self.frame_index = 0

        # Animation
        self.animation_speed = 0.0095
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)
        
        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_frames(self):
        frames = []
        sheet_width = self.sheet.get_width()
        zoom = 3

        for i in range(sheet_width // self.frame_width):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            
            # Zoom
            frame = pygame.transform.scale(frame, (self.frame_width * zoom, self.frame_height * zoom))
            frames.append(frame)

        return frames
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_q])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_z])
        self.direction = self.direction.normalize() if self.direction else self.direction
        # self.direction.y
        

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    
    def update(self, dt):
        self.input()
        self.animate()
        self.move(dt)
