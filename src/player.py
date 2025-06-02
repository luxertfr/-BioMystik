from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        
        # settings
        self.frame_width = 100 
        self.frame_height = 100

        # Load
        self.idle_sheet = pygame.image.load(join('assets', 'chara', 'Soldier-Idle.png')).convert_alpha()
        self.walk_sheet = pygame.image.load(join('assets', 'chara', 'Soldier-Walk.png')).convert_alpha()
        
        # Load frames
        self.idle_frames = self.load_frames(self.idle_sheet)
        self.walk_frames = self.load_frames(self.walk_sheet)
        self.frames = self.idle_frames 
        self.last_frames = self.frames
        

        self.frame_index = 0

        # Animation
        self.animation_speed = 0.025
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-275, -275)

            
        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites


    def load_frames(self, sheet):
        frames = []
        sheet_width = sheet.get_width()
        zoom = 3

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
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_q])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_z])
        self.direction = self.direction.normalize() if self.direction else self.direction
        
        if self.direction.length_squared() == 0:
            self.frames = self.idle_frames
        else:
            self.frames = self.walk_frames
            
        if self.frames != self.last_frames:
            self.frame_index = 0
        self.last_frames = self.frames

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
        self.input()
        self.animate()
        self.move(dt)
