from settings import * 

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class CollisionSprite(pygame.sprite.Sprite) :
    def __init__(self, pos, surf, groups, message="", items=""):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.items = items

        self.message = message

