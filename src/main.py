from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from interaction import DialogBox

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
        self.dialog_box = DialogBox(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.interactables = []
        
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
            sprite = Sprite((x * TILE_SIZE * zoom, y * TILE_SIZE * zoom), image, self.all_sprites)
            
        for obj in map.get_layer_by_name("Objects"):
            if hasattr(obj, "image") and obj.image:
                image = pygame.transform.scale(obj.image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            else:
                image = pygame.Surface((obj.width * zoom, obj.height * zoom), pygame.SRCALPHA)

            message = getattr(obj, "properties", {}).get("message", "Aucun message")

            sprite = CollisionSprite((obj.x * zoom, obj.y * zoom), image, (self.all_sprites, self.collision_sprites), message)

            self.interactables.append(sprite)
            
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        self.debug = not self.debug
                        # print("debugactive")
                    elif event.key == pygame.K_e:
                        for obj in self.interactables:
                            if self.player.rect.colliderect(obj.rect.inflate(20, 20)):
                                self.dialog_box.show_message(obj.message)


                    
            # Update     
            self.all_sprites.update(dt)
            self.dialog_box.update()
            
            # draw
            self.display_surface.fill((30, 30, 30))
            self.all_sprites.custom_draw(self.player)
            self.dialog_box.draw(self.display_surface)

            if self.debug : 
                self.draw_debug()


            pygame.display.update()
    
    def draw_debug(self):
        offset = self.all_sprites.offset

        # Hitbox du joueur
        pygame.draw.rect(self.display_surface, (255, 0, 0), self.player.hitbox_rect.move(-offset.x, -offset.y), 2)

        # Toutes les collisions
        for sprite in self.collision_sprites:
            pygame.draw.rect(self.display_surface, (0, 0, 255), sprite.rect.move(-offset.x, -offset.y), 2)


        
    pygame.quit()
                
if __name__ == '__main__':
    game = Game()
    game.run()
    

        