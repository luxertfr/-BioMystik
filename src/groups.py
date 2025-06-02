from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def custom_draw(self, target):
        # Centrer la caméra sur le joueur
        self.offset.x = target.rect.centerx - WINDOW_WIDTH // 2
        self.offset.y = target.rect.centery - WINDOW_HEIGHT // 2

        # Dessiner tous les sprites avec l'offset
        for sprite in self:
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
