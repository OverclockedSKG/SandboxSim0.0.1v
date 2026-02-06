import pygame
import random

class Block:
    def __init__(self, x, y, size=50):
        self.size = size

        # Float position (single source of truth)
        self.x = float(x)
        self.y = float(y)

        self.rect = pygame.Rect(x, y, size, size)

        self.color = (
            random.randint(60, 255),
            random.randint(60, 255),
            random.randint(60, 255),
        )

        self.weight = round(random.uniform(0.6, 2.0), 2)

        self.vel_x = random.uniform(-10, 10)
        self.vel_y = 0.0

        self.dragging = False

    def apply_physics(self, dt, gravity=1400, air_drag=0.99):
        if self.dragging:
            return

        # Gravity (weight-scaled)
        self.vel_y += gravity * self.weight * dt

        # Drag
        self.vel_x *= air_drag

        # ---- X AXIS ----
        self.x += self.vel_x * dt
        self.rect.x = int(self.x)

        # ---- Y AXIS ----
        self.y += self.vel_y * dt
        self.rect.y = int(self.y)

    def resolve_collisions(self, blocks, ground_y):
        # Ground
        if self.rect.bottom > ground_y:
            self.rect.bottom = ground_y
            self.y = self.rect.y
            self.vel_y = 0
            self.vel_x *= 0.85

        for other in blocks:
            if other is self:
                continue

            if not self.rect.colliderect(other.rect):
                continue

            # Calculate overlap
            overlap_x1 = self.rect.right - other.rect.left
            overlap_x2 = other.rect.right - self.rect.left
            overlap_y1 = self.rect.bottom - other.rect.top
            overlap_y2 = other.rect.bottom - self.rect.top

            min_overlap = min(overlap_x1, overlap_x2, overlap_y1, overlap_y2)

            # ---- Vertical resolution ----
            if min_overlap == overlap_y1 and self.vel_y > 0:
                self.rect.bottom = other.rect.top
                self.y = self.rect.y
                self.vel_y = 0

            elif min_overlap == overlap_y2 and self.vel_y < 0:
                self.rect.top = other.rect.bottom
                self.y = self.rect.y
                self.vel_y = 0

            # ---- Horizontal pushing (position-based, weight-aware) ----
            elif min_overlap == overlap_x1:
                push = overlap_x1 * (1 / self.weight)
                self.rect.right = other.rect.left
                self.x = self.rect.x

                other.x += push
                other.rect.x = int(other.x)

            elif min_overlap == overlap_x2:
                push = overlap_x2 * (1 / self.weight)
                self.rect.left = other.rect.right
                self.x = self.rect.x

                other.x -= push
                other.rect.x = int(other.x)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
