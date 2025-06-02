from settings import *

class DialogBox:
    def __init__(self, width, height):
        self.font = pygame.font.Font("assets/police/SDS_6x6.ttf", 24)  
        self.box_rect = pygame.Rect(50, height - 100, width - 100, 80)
        self.message = ""
        self.visible = False

    def show_message(self, message):
        self.message = message
        self.visible = True
        self.start_time = pygame.time.get_ticks()

    def hide(self):
        self.visible = False

    def update(self):
        if self.visible and pygame.time.get_ticks() - self.start_time > 6000:
            self.hide()

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, (0, 0, 0), self.box_rect)
            pygame.draw.rect(surface, (255, 255, 255), self.box_rect, 3)
            text_surf = self.font.render(self.message, True, (255, 255, 255))
            surface.blit(text_surf, self.box_rect.move(10, 10))
