from settings import *
from pytmx.util_pygame import load_pygame


class Portal:
    def __init__(self, portals_data, zoom):
        self.zoom = zoom
        self.portals = []

        for obj in portals_data:
            rect = pygame.Rect(obj.x * zoom, obj.y * zoom, obj.width * zoom, obj.height * zoom)
            properties = getattr(obj, "properties", {})
            self.portals.append({
                "rect": rect,
                "target_map": properties.get("target_map"),
                "target_x": float(properties.get("target_x", 0)),
                "target_y": float(properties.get("target_y", 0))
            })

    def get_portal_at(self, player_rect):
        # Retourne le portail sous le joueur ou None
        for portal in self.portals:
            if player_rect.colliderect(portal["rect"]):
                return portal
        return None
