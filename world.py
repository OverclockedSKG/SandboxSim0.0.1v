import pygame

class World:
    def __init__(self, ground_y):
        self.blocks = []
        self.ground_y = ground_y

    def add_block(self, block):
        self.blocks.append(block)

    def update(self, dt):
        for block in self.blocks:
            block.apply_physics(dt)

        for block in self.blocks:
            block.resolve_collisions(self.blocks, self.ground_y)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (90, 90, 90),
            (0, self.ground_y, screen.get_width(), screen.get_height())
        )

        for block in self.blocks:
            block.draw(screen)
