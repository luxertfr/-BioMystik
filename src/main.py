from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

from random import randint

class Game:
    def __init__(self):
        # Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Bio Mystik')
        self.clock = pygame.time.Clock()
        self.running = True
        self.debug = False # Doesnt work idk why 
        
        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        
        # Debug


        
        self.setup()
        
 
        
        # Sprites
        # self.player = Player((686.0 * 2.75, 1575.45 * 2.75), self.all_sprites, self.collision_sprites)

    
    def setup(self):
        zoom = 2.75
        map = load_pygame(join("assets", "tmx", "start.tmx"))

        for x, y, image in map.get_layer_by_name('ground').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            Sprite((x * TILE_SIZE * zoom, y * TILE_SIZE * zoom), image, self.all_sprites)
            
        for x, y, image in map.get_layer_by_name('c(housewat)').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            Sprite((x * TILE_SIZE * zoom, y * TILE_SIZE * zoom), image, self.all_sprites)
            
        for x, y, image in map.get_layer_by_name('c(treedeco)').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            Sprite((x * TILE_SIZE * zoom, y * TILE_SIZE * zoom), image, self.all_sprites)
            
        for x, y, image in map.get_layer_by_name('deco').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            Sprite((x * TILE_SIZE * zoom, y * TILE_SIZE * zoom), image, self.all_sprites)
            
        for obj in map.get_layer_by_name("Objects"):
            image = pygame.transform.scale(obj.image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            CollisionSprite((obj.x * zoom, obj.y * zoom), image, (self.all_sprites, self.collision_sprites))
            
        for coll in map.get_layer_by_name("Collisions"):
            x = coll.x * zoom
            y = coll.y * zoom
            width = coll.width * zoom
            height = coll.height * zoom

            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            CollisionSprite((x, y), surface, (self.all_sprites, self.collision_sprites))
        
        for marker in map.get_layer_by_name("Entities"):
            print(marker)
            if marker.name == "playerSpawn":
                print("a")
                print(marker.x, marker.y)
                self.player = Player((marker.x * zoom, marker.y * zoom), self.all_sprites, self.collision_sprites)
            
    def run(self):
        while self.running:
            # Dt
            dt = self.clock.tick() / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            if self.debug:
                self.draw_debug()

                    
            # Update     
            self.all_sprites.update(dt)
            
            # draw
            self.display_surface.fill((30, 30, 30))
            self.all_sprites.draw(self.player.rect.center)

            pygame.display.update()
    
    def draw_debug(self):
        # Hitbox du joueur
        pygame.draw.rect(self.display_surface, (255, 0, 0), self.player.hitbox_rect, 2)

        # Toutes les collisions
        for sprite in self.collision_sprites:
            pygame.draw.rect(self.display_surface, (0, 0, 255), sprite.rect, 2)


        
        pygame.quit()
                
if __name__ == '__main__':
    game = Game()
    game.run()
    

        