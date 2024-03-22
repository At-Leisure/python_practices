import pygame
from .classes import Block, BlockState, BlockShape

def make_background(n_row, n_col, unit) -> pygame.Surface:
    bg = pygame.Surface((n_col*unit, n_row*unit))
    bg.fill((100, 100, 100))

    line_color = (50, 100, 100)
    for c in range(n_col+1):
        pygame.draw.line(bg, line_color, [c*unit, 0], [c*unit, n_row*unit], 1)

    for r in range(n_row+1):
        pygame.draw.line(bg, line_color, [0, r*unit], [n_col*unit, r*unit], 1)
    return bg
