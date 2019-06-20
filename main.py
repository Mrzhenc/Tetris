# encoding=utf-8
import pygame
from sys import exit
from pygame.locals import *
from common import *
from block import *
score = 0


class MainWindow(object):
    def __init__(self):
        pygame.init()
        self.window_x = WINDOW_X
        self.window_y = WINDOW_Y
        self.main_window = None
        self.background = None
        self.font = None
        self.game_over_font = None
        self.cur_pos_x = BLOCK_NUM_X / 2
        self.cur_pos_y = 0  # 应该指在当前方块的最底部
        self.delay_time = 200
        # 保存当前已下落的块
        self.cur_blk_list = []
        self.cur_height = 0
        self.block_area_map = []
        for i in range(BLOCK_NUM_Y):
            self.block_area_map.append([])
            for j in range(BLOCK_NUM_X):
                self.block_area_map[i].append('.')

            if i == BLOCK_NUM_Y-1:
                self.block_area_map.append([])
                for k in range(BLOCK_NUM_X):
                    self.block_area_map[BLOCK_NUM_Y].append('0')

        # print(self.block_area_map)

    def print_text(self, text, pos_x, pos_y, text_color=WHITE):
        if text == f'Game Over':
            img_text = self.game_over_font.render(text, True, text_color)
        else:
            img_text = self.font.render(text, True, text_color)
        self.main_window.blit(img_text, (pos_x, pos_y))

    def draw_rect(self, pos_x, pos_y):
        pygame.draw.rect(self.main_window, BLOCK_COLOR, (pos_x, pos_y, BLOCK_X, BLOCK_Y))

    def init_game(self):
        self.font = pygame.font.SysFont('SimHei', 30)
        self.game_over_font = pygame.font.SysFont('SimHei', 60)
        self.main_window = pygame.display.set_mode([self.window_x, self.window_y])
        pygame.display.set_caption("俄罗斯方块")
        self.main_window.fill(BG_COLOR)
        font_x = TIP_WINDOW_X + 10
        font_y = int(self.font.size('得分')[1])
        pygame.draw.line(self.main_window, SPLIT_COLOR, (TIP_WINDOW_X, 0),
                         (TIP_WINDOW_X, WINDOW_Y), 3)
        self.background = pygame.image.load("./back.jpg")

        self.print_text(f'得分:', font_x, font_y)
        font_y += 30
        self.print_text(f'{score}', font_x, font_y)

        font_y += 50
        self.print_text(f'速度:', font_x, font_y)
        font_y += 30
        self.print_text(f'{score // 10}', font_x, font_y)

        # 画格子
        for i in range(BLOCK_NUM_X):
            pygame.draw.line(self.main_window, SPLIT_COLOR, (i*BLOCK_X, 0), (i*BLOCK_X, BLOCK_Y*BLOCK_NUM_Y), 1)

        for j in range(BLOCK_NUM_Y):
            pygame.draw.line(self.main_window, SPLIT_COLOR, (0, j*BLOCK_X), (BLOCK_X*BLOCK_NUM_X, j*BLOCK_X), 1)

    def run(self):

        # 设置背景
        # self.main_window.blit(self.background, (0, 0))

        cur_blk = None
        pause = False
        # move_left = False
        # move_right = False
        game_over_text = "Game Over"

        while True:
            if not cur_blk:
                cur_blk = get_block()
                for i in range(cur_blk.start_pos.pos_x, cur_blk.end_pos.pos_x + 1):
                    for j in range(cur_blk.start_pos.pos_y, cur_blk.end_pos.pos_y + 1):
                        if cur_blk.template[i][j] == '0':
                            self.draw_rect((j + self.cur_pos_x) * BLOCK_X, i * BLOCK_X)
            pygame.time.delay(self.delay_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # 暂停
                    pause = not pause
                    # cur_blk = get_next_block(cur_blk)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    # 加速键
                    self.delay_time -= 100
                elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    self.delay_time += 100
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    tmp_blk = get_next_block(cur_blk)
                    if (BLOCK_NUM_X - self.cur_pos_x) > tmp_blk.end_pos.pos_y+1:
                        cur_blk = tmp_blk
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    # 边界判断
                    if (BLOCK_NUM_X - cur_blk.end_pos.pos_y - 1) > self.cur_pos_x >= 0:
                        # 判断右边是否有块
                        if self.block_area_map[int(self.cur_pos_y)][int(self.cur_pos_x+cur_blk.end_pos.pos_y)] != '0':
                            self.cur_pos_x += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if self.cur_pos_x > 0:
                        self.cur_pos_x -= 1

            if pause:
                continue
            self.init_game()
            # 绘制当前下落方块
            if cur_blk:
                for i in range(cur_blk.start_pos.pos_x, cur_blk.end_pos.pos_x + 1):
                    for j in range(cur_blk.start_pos.pos_y, cur_blk.end_pos.pos_y+1):
                        if cur_blk.template[i][j] == '0':
                            self.draw_rect((j + self.cur_pos_x) * BLOCK_X, (i+self.cur_pos_y) * BLOCK_X)

            for idx_y, x_pos in enumerate(self.block_area_map):
                if idx_y == 41:
                    break
                if x_pos.count('0') == 0:
                    continue
                for idx_x, element in enumerate(x_pos):
                    if '0' == element:
                        self.draw_rect(idx_x*BLOCK_X, idx_y*BLOCK_Y)

            # print(self.cur_pos_y, self.cur_pos_x + cur_blk.end_pos.pos_x+1)

            for (x_pos, h) in zip(range(cur_blk.start_pos.pos_y, cur_blk.end_pos.pos_y+1), cur_blk.height):
                # print(self.cur_pos_y, h, self.cur_pos_x, x_pos)
                if self.block_area_map[int(self.cur_pos_y)+h][int(self.cur_pos_x+x_pos)] != '0':
                    continue

                # 无法下落时，判断是否结束游戏
                if self.cur_pos_y == 1:
                    pause = True
                    self.print_text(f'{game_over_text}', BLOCK_NUM_X/2*BLOCK_X-120, BLOCK_NUM_Y/2*BLOCK_X)

                for i in range(cur_blk.start_pos.pos_x, cur_blk.end_pos.pos_x + 1):
                    for j in range(cur_blk.start_pos.pos_y, cur_blk.end_pos.pos_y + 1):
                        # print(j, self.cur_pos_x)
                        if cur_blk.template[i][j] == '0':
                            self.block_area_map[int(self.cur_pos_y)+i][int(self.cur_pos_x)+j] = '0'

                cur_blk = None
                self.cur_pos_y = 0
                self.cur_pos_x = BLOCK_NUM_X / 2
                break
            # else:
            # 判断当时是否有可消除行
            tmp_score = 0
            for i in range(BLOCK_NUM_Y):
                if self.block_area_map[BLOCK_NUM_Y-1].count('0') == BLOCK_NUM_X:
                    # 得分 行数*10
                    tmp_score += 10*(i+1)
                    self.block_area_map.pop()
                    new_line = []
                    for i in range(BLOCK_NUM_X):
                        new_line.append('.')
                    self.block_area_map.insert(0, new_line)
                    print(len(self.block_area_map))

            global score
            score += tmp_score

            self.cur_pos_y += 1
            pygame.display.update()
            continue


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.init_game()
    main_window.run()
