NEXT_ENTITY_ID = 1


class Entity:
    def __init__(self):
        global NEXT_ENTITY_ID
        self.id = NEXT_ENTITY_ID
        NEXT_ENTITY_ID += 1
        self.components = {}


class Transform:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Sprite:
    def __init__(self, name):
        self.name = name


class Render:
    def __init__(self, screen):
        self.sprites = {}
        self.screen = screen

    def run(self, entities):
        for entity in entities:
            sprite = get_component(entity, Sprite)
            transform = get_component(entity, Transform)
            self.sprites[sprite.name].render(self.screen, transform)


def add_component(entity, component):
    entity.components[component.__class__.__name__] = component


def get_component(entity, component_class):
    return entity.components[component_class.__name__]
