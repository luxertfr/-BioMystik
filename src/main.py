from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from interaction import DialogBox
from teleporter import Portal
from ui import UI
from enemy import Enemy

from random import randint

class Game:
    def __init__(self):
        # Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Bio Mystik')
        self.clock = pygame.time.Clock()
        self.running = True
        self.debug = False
        self.on_portal = False
        self.current_portal = None 
        self.dialog_box = DialogBox(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.ui = UI()
        self.required_items = {"luciole": 4, "totem": 3} 

        self.interactables = []
        self.objectItems = []
        
        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        
        # Debug


        
        self.setup(load_pygame(join("assets", "tmx", "dungeon.tmx")))

        # Sprites
        # self.player = Player((686.0 * 2.75, 1575.45 * 2.75), self.all_sprites, self.collision_sprites)

    
    def setup(self, tmx_map):
        zoom = 2.75
        self.current_map = tmx_map
        
        # Charger les portails
        portals_layer = self.current_map.get_layer_by_name("Portal")
        self.teleporter = Portal(portals_layer, zoom)
        

        for x, y, image in self.current_map.get_layer_by_name('ground').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            Sprite((x * TILE_SIZE * zoom, y * TILE_SIZE * zoom), image, self.all_sprites)
            

        for x, y, image in self.current_map.get_layer_by_name('c(housewat)').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            Sprite((x * TILE_SIZE * zoom, y * TILE_SIZE * zoom), image, self.all_sprites)
            
        for x, y, image in self.current_map.get_layer_by_name('c(treedeco)').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            Sprite((x * TILE_SIZE * zoom, y * TILE_SIZE * zoom), image, self.all_sprites)
            
        for x, y, image in self.current_map.get_layer_by_name('deco').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            sprite = Sprite((x * TILE_SIZE * zoom, y * TILE_SIZE * zoom), image, self.all_sprites)
            
            
        for obj in self.current_map.get_layer_by_name("NPC"):
            if hasattr(obj, "image") and obj.image:
                image = pygame.transform.scale(obj.image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            else:
                image = pygame.Surface((obj.width * zoom, obj.height * zoom), pygame.SRCALPHA)

            message = getattr(obj, "properties", {}).get("message", "Aucun message")

            sprite = CollisionSprite((obj.x * zoom, obj.y * zoom), image, (self.all_sprites, self.collision_sprites), message, "")
            
            if hasattr(obj, "properties") and obj.properties.get("removable", False):
                sprite.can_be_removed = True
            else:
                sprite.can_be_removed = False
            

            self.interactables.append(sprite)
            print(self.interactables)
            
        for obj in self.current_map.get_layer_by_name("Entities"):
            if obj.name == "playerSpawn":
                print(obj.x, obj.y)
                self.player = Player((obj.x * zoom, obj.y * zoom), self.all_sprites, self.collision_sprites)
            elif obj.name == "enemy":
                Enemy((obj.x * zoom, obj.y * zoom), (self.all_sprites, self.enemy_sprites), self.collision_sprites, self.player)

            if hasattr(obj, "image") and obj.image:
                image = pygame.transform.scale(obj.image, (TILE_SIZE * zoom, TILE_SIZE * zoom))
            else:
                image = pygame.Surface((obj.width * zoom, obj.height * zoom), pygame.SRCALPHA)

            items = getattr(obj, "properties", {}).get("items", "")

            sprite = CollisionSprite((obj.x * zoom, obj.y * zoom), image, (self.all_sprites, self.collision_sprites),"", items)
            
            self.objectItems.append(sprite)
            
            
        for coll in self.current_map.get_layer_by_name("Collisions"):
            x = coll.x * zoom
            y = coll.y * zoom
            width = coll.width * zoom
            height = coll.height * zoom

            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            CollisionSprite((x, y), surface, (self.all_sprites, self.collision_sprites))

            
    def load_map(self, map_name, spawn_pos, saved_inventory):
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.interactables.clear()

        self.current_map = load_pygame(join("assets", "tmx", map_name))
        self.setup(self.current_map)
        self.player.inventory = saved_inventory
        self.player.rect.topleft = spawn_pos

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self.ui.draw_health_bar(self.display_surface, 10, 10, self.player.current_hp, self.player.max_hp)

            saved_inventory = self.player.inventory.copy()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        self.debug = not self.debug
                    elif event.key == pygame.K_e:
                        portal = self.teleporter.get_portal_at(self.player.rect)
                        if portal and portal["target_map"]:
                            self.load_map(
                                portal["target_map"],
                                (portal["target_x"] * self.teleporter.zoom, portal["target_y"] * self.teleporter.zoom),
                                saved_inventory
                            )


                        for obj in self.interactables:
                            if self.player.rect.colliderect(obj.rect.inflate(20, 20)):
                                if self.has_required_items(self.required_items):
                                    self.remove_required_items(self.required_items)
                                    self.player.add_item("épée")
                                    self.player.add_item("clef") 
                                    self.dialog_box.show_message("Merci ! Voici les items.")
                                else:
                                    self.dialog_box.show_message(obj.message)
                                
                        for item in self.objectItems: 
                            if self.player.rect.colliderect(item.rect.inflate(20, 20)):
                                self.player.add_item(item.items)
                                print(item.items,  "+ 1")
                                self.objectItems.remove(item)
                        
                        for sprite in list(self.collision_sprites):
                            if self.player.inventory.get("clef", 0)> 0 and self.player.inventory.get("épée", 0) > 0:
                                self.collision_sprites.remove(sprite)
                                self.all_sprites.remove(sprite)
                                self.dialog_box.show_message("Tu as deverouille le passage !")
                            else :
                                self.dialog_box.show_message(sprite.message)
                elif (event.type == pygame.MOUSEBUTTONDOWN) and (self.player.inventory.get("épée", 0) > 0):
                    self.player.attack(self.enemy_sprites)
                    # else:
                    #     self.dialog_box.show_message("Tu n'as pas d'epee pour attaquer!")
                                
            for portal in self.teleporter.portals:
                if self.player.rect.colliderect(portal["rect"]):
                    self.on_portal = True
                    self.current_portal = portal

            if not self.player.is_alive:
                font = pygame.font.Font(None, 100)  # Police par défaut, taille 100
                game_over_surf = font.render("GAME OVER", True, (255, 0, 0))  # Texte rouge
                game_over_rect = game_over_surf.get_rect(center=(WINDOW_WIDTH // 2,  WINDOW_HEIGHT // 2))
                self.display_surface.blit(game_over_surf, game_over_rect)
            
            
            # Update
            self.all_sprites.update(dt)
            self.enemy_sprites.update(dt)
            self.dialog_box.update()

            # Draw
            self.display_surface.fill((30, 30, 30))
            self.all_sprites.custom_draw(self.player)
            self.dialog_box.draw(self.display_surface)
            
            self.ui.draw_health_bar(self.display_surface, 10, 10, self.player.current_hp, self.player.max_hp)
            self.draw_inventory()

            
            # # message E on portail
            # if self.on_portal:
            #     font = pygame.font.SysFont(None, 24)
            #     text_surf = font.render("Appuyez sur E pour vous téléporter", True, (255, 255, 255))
            #     text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
            #     self.display_surface.blit(text_surf, text_rect)


            if self.debug:
                self.draw_debug()

            pygame.display.update()

        pygame.quit()
    
    def draw_debug(self):
        offset = self.all_sprites.offset

        # Hitbox du joueur
        pygame.draw.rect(self.display_surface, (255, 0, 0), self.player.hitbox_rect.move(-offset.x, -offset.y), 2)

        # Toutes les collisions
        for sprite in self.collision_sprites:
            pygame.draw.rect(self.display_surface, (0, 0, 255), sprite.rect.move(-offset.x, -offset.y), 2)
            
    def draw_inventory(self):
        if not self.player.inventory:
            return  

        font = pygame.font.SysFont(None, 24)
        inventory_list = [f"{item}: {count}" for item, count in self.player.inventory.items() if item != ""]

        inventory_text = "Inventaire: " + ", ".join(inventory_list)
        text_surf = font.render(inventory_text, True, (255, 255, 255))
        self.display_surface.blit(text_surf, (10, 40))  # un peu sous la barre de vie

    def has_required_items(self, required_items):
        for item, qty in required_items.items():
            if self.player.inventory.get(item, 0) < qty:
                return False
        return True

    def remove_required_items(self, required_items):
        for item, qty in required_items.items():
            self.player.inventory[item] -= qty
            if self.player.inventory[item] <= 0:
                del self.player.inventory[item]

        
    
    
if __name__ == '__main__':
    game = Game()
    game.run()