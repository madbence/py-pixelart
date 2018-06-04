NEXT_ENTITY_ID = 1


class Entity:
    def __init__(self):
        global NEXT_ENTITY_ID
        self.id = NEXT_ENTITY_ID
        NEXT_ENTITY_ID += 1
        self.components = {}


class Component:
    pass


class System:
    pass


def add_component(entity, component):
    entity.components[component.__class__.__name__] = component


def get_component(entity, component_class):
    return entity.components[component_class.__name__]
