# encoding=utf-8
import pygame
from sys import exit
from pygame.locals import *
from common import *
from block import *
import threading
import time
score = 0

#
# class MoveThread(threading):
#     def __init__(self):
#         super(MoveThread.self).__init__()
#         self.pos_x = 0
#
#     def run(self):
#         pass


class MainWindow(object):
    def __init__(self):
        pygame.init()
        self.window_x = WINDOW_X
        self.window_y = WINDOW_Y
        # self.main_window = None
        self.main_window = pygame.display.set_mode([self.window_x, self.window_y])
        pygame.display.set_caption("俄罗斯方块")
        self.background = None
        self.font = None
        self.game_over_font = None
        self.cur_pos_x = BLOCK_NUM_X / 2
        self.cur_pos_y = 0
        self.delay_time = DELAY_TIME
        self.cur_height = 0
        # 保存当前已下落的块
        self.block_area_map = []
        self.next_blk = None
        self.cur_blk = None
        self.start = False
        self.pause = False
        self.is_end = False
        self.speed_up = 0
        self.status = "暂停"
        self.btn_press_time = 0
        self.is_move = False
        self.btn_map = {"start": [], "restart": [], "stop": []}
        for i in range(BLOCK_NUM_Y):
            self.block_area_map.append([])
            for j in range(BLOCK_NUM_X):
                self.block_area_map[i].append('.')

            if i == BLOCK_NUM_Y-1:
                self.block_area_map.append([])
                for k in range(BLOCK_NUM_X):
                    self.block_area_map[BLOCK_NUM_Y].append('0')

    def print_text(self, text, pos_x, pos_y, text_color=WHITE):
        if text == f'Game Over':
            img_text = self.game_over_font.render(text, True, RED)
        else:
            img_text = self.font.render(text, True, text_color)
        self.main_window.blit(img_text, (pos_x, pos_y))

    def draw_rect(self, pos_x, pos_y, btn=False):
        if btn:
            pygame.draw.rect(self.main_window, BTN_COLOR, (pos_x, pos_y, BTN_WIDTH, BTN_HEIGHT))
        else:
            pygame.draw.rect(self.main_window, BLOCK_COLOR, (pos_x, pos_y, BLOCK_X, BLOCK_Y))

    def init_game(self):
        self.font = pygame.font.SysFont('SimHei', 30)
        self.game_over_font = pygame.font.SysFont('SimHei', 60)
        self.main_window.fill(BG_COLOR)
        font_x = TIP_WINDOW_X + 50
        font_y = int(self.font.size('得分')[1])
        pygame.draw.line(self.main_window, SPLIT_COLOR, (TIP_WINDOW_X, 0),
                         (TIP_WINDOW_X, WINDOW_Y), 3)
        self.background = pygame.image.load("./back.jpg")

        self.print_text(f'得分:', font_x, font_y)
        font_y += 30
        self.print_text(f'{score}', font_x, font_y)

        font_y += 60
        self.print_text(f'速度:', font_x, font_y)
        font_y += 30
        self.print_text(f'{score // 10}', font_x, font_y)

        font_y += 60
        self.print_text(f'下一个:', font_x, font_y)
        font_y += 30
        if self.cur_blk:
            if not self.next_blk:
                self.next_blk = get_block()
            self.draw_block(self.next_blk, font_x, font_y)

        font_y += 200
        self.draw_rect(font_x, font_y, btn=True)
        self.print_text(f'开始', font_x+10, font_y+5)
        self.btn_map['start'].append(font_x+10)
        self.btn_map['start'].append(font_y+5)

        font_y += 100
        self.draw_rect(font_x, font_y, btn=True)
        self.print_text(f'{self.status}', font_x+10, font_y+5)
        self.btn_map['stop'].append(font_x+10)
        self.btn_map['stop'].append(font_y+5)

        font_y += 100
        self.draw_rect(font_x, font_y, btn=True)
        self.print_text(f'重开', font_x+10, font_y+5)
        self.btn_map['restart'].append(font_x+10)
        self.btn_map['restart'].append(font_y+5)

        # 画格子
        for i in range(BLOCK_NUM_X):
            pygame.draw.line(self.main_window, SPLIT_COLOR, (i*BLOCK_X, 0), (i*BLOCK_X, BLOCK_Y*BLOCK_NUM_Y), 1)

        for j in range(BLOCK_NUM_Y):
            pygame.draw.line(self.main_window, SPLIT_COLOR, (0, j*BLOCK_X), (BLOCK_X*BLOCK_NUM_X, j*BLOCK_X), 1)

    def draw_block(self, blk, pos_x, pos_y):
        for i in range(blk.start_pos.pos_x, blk.end_pos.pos_x + 1):
            for j in range(blk.start_pos.pos_y, blk.end_pos.pos_y + 1):
                if blk.template[i][j] == '0':
                    self.draw_rect((pos_x+j*BLOCK_X), (pos_y+i*BLOCK_X))

    def restart_game(self):
        del self.block_area_map[:]
        for i in range(BLOCK_NUM_Y):
            self.block_area_map.append([])
            for j in range(BLOCK_NUM_X):
                self.block_area_map[i].append('.')

            if i == BLOCK_NUM_Y-1:
                self.block_area_map.append([])
                for k in range(BLOCK_NUM_X):
                    self.block_area_map[BLOCK_NUM_Y].append('0')
        self.cur_blk = None
        self.next_blk = None
        self.start = False
        self.is_end = False
        self.cur_pos_x = BLOCK_NUM_X/2
        self.cur_pos_y = 0
        self.delay_time = DELAY_TIME
        global score
        score = 0

    def run(self):
        self.cur_blk = None
        game_over_text = "Game Over"
        pygame.key.set_repeat(1, 1)

        while True:
            if self.is_move:
                pygame.time.delay(100)

            if not self.cur_blk:
                if self.next_blk:
                    self.cur_blk = self.next_blk
                    self.next_blk = None
                else:
                    self.cur_blk = get_block()
                for i in range(self.cur_blk.start_pos.pos_x, self.cur_blk.end_pos.pos_x + 1):
                    for j in range(self.cur_blk.start_pos.pos_y, self.cur_blk.end_pos.pos_y + 1):
                        if self.cur_blk.template[i][j] == '0':
                            self.draw_rect((j + self.cur_pos_x) * BLOCK_X, i * BLOCK_X)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        tmp_blk = get_next_block(self.cur_blk)
                        if (BLOCK_NUM_X - self.cur_pos_x) > tmp_blk.end_pos.pos_y+1:
                            self.cur_blk = tmp_blk
                    elif event.key == pygame.K_RIGHT:
                        if self.is_end or self.pause or not self.start:
                            break
                        # 边界判断
                        if (BLOCK_NUM_X - self.cur_blk.end_pos.pos_y - 1) > self.cur_pos_x >= 0:
                            # 判断右边是否有块
                            if self.block_area_map[int(self.cur_pos_y)][int(self.cur_pos_x+self.cur_blk.end_pos.pos_y)] != '0':
                                self.cur_pos_x += 1
                                if 0 == self.btn_press_time:
                                    self.btn_press_time = int(round(time.time() * 1000))
                                self.is_move = True
                    elif event.key == pygame.K_LEFT:
                        if self.is_end or self.pause or not self.start:
                            break
                        if self.cur_pos_x > 0:
                            self.cur_pos_x -= 1
                            if 0 == self.btn_press_time:
                                self.btn_press_time = int(round(time.time()*1000))
                            self.is_move = True
                    elif event.key == pygame.K_SPACE:
                        # 暂停
                        if self.pause:
                            self.status = "暂停"
                        else:
                            self.status = '继续'
                        self.pause = not self.pause
                    elif event.key == pygame.K_DOWN:
                        if self.speed_up == 0:
                            self.speed_up += 500
                    else:
                        pass

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.speed_up = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        self.is_move = False
                        self.btn_press_time = 0

                if event.type == pygame.MOUSEBUTTONDOWN and self.btn_map['start'][0] < event.pos[0] < \
                        self.btn_map['start'][0]+BTN_WIDTH and self.btn_map['start'][1] < event.pos[1] < \
                        self.btn_map['start'][1]+BTN_HEIGHT:
                    self.start = True
                elif event.type == pygame.MOUSEBUTTONDOWN and self.btn_map['restart'][0] < event.pos[0] < \
                        self.btn_map['restart'][0]+BTN_WIDTH and self.btn_map['restart'][1] < event.pos[1] < \
                        self.btn_map['restart'][1]+BTN_HEIGHT:
                    self.restart_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.btn_map['stop'][0] < event.pos[0] < \
                        self.btn_map['stop'][0]+BTN_WIDTH and self.btn_map['stop'][1] < event.pos[1] < \
                        self.btn_map['stop'][1]+BTN_HEIGHT:
                    if self.pause:
                        self.status = "暂停"
                    else:
                        self.status = '继续'
                    self.pause = not self.pause

            if not self.cur_blk:
                continue
            self.init_game()

            # 绘制当前下落方块
            if self.cur_blk:
                for i in range(self.cur_blk.start_pos.pos_x, self.cur_blk.end_pos.pos_x + 1):
                    for j in range(self.cur_blk.start_pos.pos_y, self.cur_blk.end_pos.pos_y+1):
                        if self.cur_blk.template[i][j] == '0':
                            self.draw_rect((j + self.cur_pos_x) * BLOCK_X, (i+self.cur_pos_y) * BLOCK_X)

            # 绘制已下落的方块
            for idx_y, x_pos in enumerate(self.block_area_map):
                if idx_y == 41:
                    break
                if x_pos.count('0') == 0:
                    continue
                for idx_x, element in enumerate(x_pos):
                    if '0' == element:
                        self.draw_rect(idx_x*BLOCK_X, idx_y*BLOCK_Y)

            if self.is_end:
                self.print_text(f'{game_over_text}', BLOCK_NUM_X / 2 * BLOCK_X - 120, BLOCK_NUM_Y / 2 * BLOCK_X)
                pygame.display.update()
                continue

            pygame.display.update()

            if self.pause:
                continue

            if not self.start:
                continue

            for (x_pos, h) in zip(range(self.cur_blk.start_pos.pos_y, self.cur_blk.end_pos.pos_y+1), self.cur_blk.height):
                # print(self.cur_pos_y, h, self.cur_pos_x, x_pos)
                if self.block_area_map[int(self.cur_pos_y)+h][int(self.cur_pos_x+x_pos)] != '0':
                    continue

                # 无法下落时，判断是否结束游戏
                if self.cur_pos_y == 1:
                    self.print_text(f'{game_over_text}', BLOCK_NUM_X/2*BLOCK_X-120, BLOCK_NUM_Y/2*BLOCK_X)
                    self.is_end = True

                for i in range(self.cur_blk.start_pos.pos_x, self.cur_blk.end_pos.pos_x + 1):
                    for j in range(self.cur_blk.start_pos.pos_y, self.cur_blk.end_pos.pos_y + 1):
                        if self.cur_blk.template[i][j] == '0':
                            self.block_area_map[int(self.cur_pos_y)+i][int(self.cur_pos_x)+j] = '0'

                self.cur_blk = None
                self.cur_pos_y = 0
                self.cur_pos_x = BLOCK_NUM_X / 2
                break

            # 判断当时是否有可消除行
            tmp_score = 0
            for i in range(BLOCK_NUM_Y):
                if self.block_area_map[BLOCK_NUM_Y-1-i].count('0') == BLOCK_NUM_X:
                    # 得分 行数*10
                    tmp_score += 10*(i+1)
                    self.delay_time -= 50
                    self.block_area_map.pop(BLOCK_NUM_Y-1-i)
                    new_line = []
                    for j in range(BLOCK_NUM_X):
                        new_line.append('.')
                    self.block_area_map.insert(0, new_line)

            if self.is_move:
                cur_time = int(round(time.time()*1000))
                if cur_time - self.btn_press_time >= self.delay_time:
                    self.btn_press_time = int(round(time.time()*1000))
                else:
                    continue

            global score
            score += tmp_score
            self.cur_pos_y += 1
            if not self.is_move:
                pygame.time.delay(self.delay_time-self.speed_up)

            # continue


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.init_game()
    main_window.run()
