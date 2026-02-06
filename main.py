import pygame
from block import Block
from world import World

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Physics Sandbox")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

GROUND_Y = 540
world = World(GROUND_Y)

selected_block = None
hovered_block = None
offset_x = 0
offset_y = 0

BG_COLOR = (25, 25, 25)

running = True
while running:
    dt = clock.tick(60) / 1000.0
    mx, my = pygame.mouse.get_pos()

    hovered_block = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            selected_block = None

            for block in reversed(world.blocks):
                if block.rect.collidepoint(mx, my):
                    selected_block = block
                    block.dragging = True
                    offset_x = block.x - mx
                    offset_y = block.y - my
                    block.vel_x = 0
                    block.vel_y = 0
                    break

            if selected_block is None:
                world.add_block(Block(mx - 25, my - 25))

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if selected_block:
                selected_block.dragging = False
                selected_block = None

    if selected_block and selected_block.dragging:
        selected_block.x = mx + offset_x
        selected_block.y = my + offset_y
        selected_block.rect.x = int(selected_block.x)
        selected_block.rect.y = int(selected_block.y)

    for block in reversed(world.blocks):
        if block.rect.collidepoint(mx, my):
            hovered_block = block
            break

    world.update(dt)

    screen.fill(BG_COLOR)
    world.draw(screen)

    if hovered_block:
        text = font.render(
            f"Weight: {hovered_block.weight}",
            True,
            hovered_block.color
        )
        screen.blit(text, (10, 10))
        pygame.draw.rect(screen, hovered_block.color, (10, 35, 30, 15))

    pygame.display.flip()

pygame.quit()
