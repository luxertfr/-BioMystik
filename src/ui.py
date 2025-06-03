from settings import *

class UI:
    def draw_health_bar(self, surface, x, y, current_hp, max_hp, width=200, height=20):
        ratio = current_hp / max_hp

        # Fond (barre vide)
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (60, 60, 60), bg_rect)

        # Barre de vie (rouge)
        fg_rect = pygame.Rect(x, y, width * ratio, height)
        pygame.draw.rect(surface, (200, 0, 0), fg_rect)

        # Bordure blanche
        pygame.draw.rect(surface, (255, 255, 255), bg_rect, 2)

