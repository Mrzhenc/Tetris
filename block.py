# encoding = utf-8
from collections import namedtuple
import random


Point = namedtuple('Point', 'pos_x pos_y')
Height = namedtuple('Height', 'h1 h2 h3')
Block = namedtuple('Block', 'template start_pos end_pos  height name next')


Z_BLOCK = [Block(['00.',
                  '.00',
                  '...'], Point(0, 0), Point(1, 2), Height(1, 2, 2), 'Z', 1),
           Block(['.00',
                  '00.',
                  '...'], Point(0, 0), Point(1, 2), Height(2, 2, 1), 'Z', 2),
           Block(['0..',
                  '00.',
                  '.0.'], Point(0, 0), Point(2, 1), Height(2, 3, 0), 'Z', 3),
           Block(['..0',
                  '.00',
                  '.0.'], Point(0, 1), Point(2, 2), Height(3, 2, 0), 'Z', 0)]


T_BLOCK = [Block(['000',
                  '.0.',
                  '...'], Point(0, 0), Point(1, 2), Height(1, 2, 1), 'T', 1),
           Block(['.0.',
                  '.00',
                  '.0.'], Point(0, 1), Point(2, 2), Height(3, 2, 0), 'T', 2),
           Block(['.0.',
                  '000',
                  '...'], Point(0, 0), Point(1, 2), Height(2, 2, 2), 'T', 3),
           Block(['.0.',
                  '00.',
                  '.0.'], Point(0, 0), Point(2, 1), Height(2, 3, 0), 'T', 0)]


I_BLOCK = [Block(['.0.',
                  '.0.',
                  '.0.'], Point(0, 1), Point(2, 1), Height(3, 0, 0), 'I', 1),
           Block(['...',
                  '000',
                  '...'], Point(1, 0), Point(1, 2), Height(2, 2, 2), 'I', 0)]

J_BLOCK = [Block(['0..',
                  '000',
                  '...'], Point(0, 0), Point(1, 2), Height(2, 2, 2), 'J', 1),
           Block(['.00',
                  '.0.',
                  '.0.'], Point(0, 1), Point(2, 2), Height(3, 1, 0), 'J', 2),
           Block(['...',
                  '000',
                  '..0'], Point(1, 0), Point(2, 2), Height(2, 2, 3), 'J', 3),
           Block(['.0.',
                  '.0.',
                  '.00'], Point(0, 1), Point(2, 2), Height(3, 3, 0), 'J', 0)]

O_BLOCK = [Block(['.00',
                  '.00',
                  '...'], Point(0, 1), Point(1, 2), Height(2, 2, 0), 'O', 0)]


BLOCKS = {"Z": Z_BLOCK,
          "T": T_BLOCK,
          "I": I_BLOCK,
          "J": J_BLOCK,
          "O": O_BLOCK}


def get_block():
    block_name = random.choice('ZTIJO')
    b = BLOCKS[block_name]
    idx = random.randint(0, len(b)-1)
    return b[idx]


def get_next_block(block):
    b = BLOCKS[block.name]
    return b[block.next]


class CurrentBlock:
    block = None
    pos_x = 0
    pos_y = 0
