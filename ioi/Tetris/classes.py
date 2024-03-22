import enum
from typing import Literal
import pygame
import copy
from .constant import *
import array
import numpy as np


class BlockState(enum.Enum):
    Grounded, Falling = range(2)


class BlockShape(enum.Enum):
    I = line = 1
    L = corner = 3
    Z = stepped = 2
    O = square = 0


class RatateState(enum.Enum):
    CW0, CW90, CW180, CW270 = range(4)


block_image = pygame.Surface((UNIT, UNIT))
block_image.fill((94, 148, 253))
pygame.draw.line(block_image, (220, 182, 124), (0, 0), (UNIT, UNIT))
pygame.draw.line(block_image, (220, 182, 124), (0, UNIT), (UNIT, 0))
pygame.draw.rect(block_image, (220, 182, 124), (0, 0, UNIT, UNIT), 1)
K = 7
pygame.draw.rect(block_image, (220, 182, 124),
                 (int(UNIT/K), int(UNIT/K), int(UNIT/K)*(K-1), int(UNIT/K)*(K-1)), 1)
pygame.draw.rect(block_image, (94, 148, 253),
                 (int(UNIT/K)+1, int(UNIT/K)+1, int(UNIT/K)*(K-1)-2, int(UNIT/K)*(K-1)-2), 0)


# class Array:
#     def __init__(self, __typecode: array._IntTypeCode, _template: list[int]) -> None:
#         self._data = array.array(__typecode,)


class Block:

    def __init__(self):
        self.surface = pygame.Surface((UNIT*4, UNIT*4), pygame.SRCALPHA)
        self.ratation = RatateState.CW0
        self._row: int
        self._colume: int
        self.array = np.zeros([4,4],dtype=np.uint8)
    def rebuild(self, shape: Literal[0, 1, 2, 3] | BlockShape):
        self.state = BlockState.Falling
        self.shape: BlockShape
        self.surface.fill((100, 0, 0, 20))
        self._row = 0
        self._colume = 0

        shape_value = shape.value if isinstance(shape, BlockShape) else shape
        match shape_value:
            case BlockShape.Z.value:
                self.shape = BlockShape.Z
                self.array = np.array([
                    [1,1,0,0],
                    [0,1,1,0],
                    [0,0,0,0],
                    [0,0,0,0]],dtype=np.uint8)
            case BlockShape.L.value:
                self.shape = BlockShape.L
                self.array = np.array([
                    [1,0,0,0],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,0,0,0]],dtype=np.uint8)
            case BlockShape.I.value:
                self.shape = BlockShape.I
                self.array = np.array([
                    [1,0,0,0],
                    [1,0,0,0],
                    [1,0,0,0],
                    [1,0,0,0]],dtype=np.uint8)
            case BlockShape.O.value:
                self.shape = BlockShape.O
                self.array = np.array([
                    [1,1,0,0],
                    [1,1,0,0],
                    [0,0,0,0],
                    [0,0,0,0]],dtype=np.uint8)
            case _:
                raise ValueError()
        for r in range(self.array.shape[0]):
            for c in range(self.array.shape[1]):
                if self.array[r,c] == 1:
                    self.surface.blit(block_image, (c*UNIT, r*UNIT))

    def draw_on(self, screen: pygame.Surface):
        screen.blit(self.surface, (self.col*UNIT, self.row*UNIT))

    @property
    def row(self) -> int:
        return self._row

    @row.setter
    def row(self, v: int):
        if not isinstance(v, int):
            raise TypeError()

        if v+0 > ROW:
            self.state = BlockState.Grounded
        else:
            self._row = v

    @property
    def col(self) -> int:
        return self._colume
    
    
    @property
    def n_row(self):
        return len([True for colume in self.array if colume.any()])
