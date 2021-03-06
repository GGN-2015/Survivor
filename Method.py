import math
import pygame
import random
import time

import Config

def distance(pointA, pointB): # 计算两点之间的距离
    dx = pointA[0] - pointB[0]
    dy = pointA[1] - pointB[1]
    return (dx ** 2 + dy ** 2) ** 0.5

def length(vec): # 计算向量长度
    return distance(vec, (0, 0))

def normalize(vec): # 取单位向量
    vec_len = length(vec)
    if vec_len == 0:
        return (0, 0)
    return (vec[0]/vec_len, vec[1]/vec_len)

def vec_add(vecA, vecB):
    return (vecA[0] + vecB[0], vecA[1] + vecB[1])

def vec_sub(vecA, vecB):
    return (vecA[0] - vecB[0], vecA[1] - vecB[1])

def vec_mul(vec, p):
    return (vec[0] * p, vec[1] * p)

def round(p): # 四舍五入
    if p >= 0:
        return int(p + 0.5)
    else:
        return int(p - 0.5)

def get_block_xy(x, y):
    return (round(x / Config.BLOCK_SIZE), round(y / Config.BLOCK_SIZE)) # 四舍五入找到最近的 block

def in_sight(pos_now, pos_player, dxdy, safe_span = 100): # 检查一个物品是否在玩家的视线范围内，也就是是否需要在屏幕上显示
    px, py = pos_now
    nx, ny = pos_player
    dx, dy = dxdy
    dx += safe_span
    dy += safe_span # 从屏幕外的一段距离就开始加载，放置突然闪入的情况
    xmin = nx - dx # xmin, xmax, ymin, ymax 是玩家可见的矩形区域
    xmax = nx + dx
    ymin = ny - dy
    ymax = ny + dy
    return xmin <= px and px <= xmax and ymin <= py and py <= ymax

def get_screen_pos(pos_xy, player_xy): # 将地图坐标映射到屏幕坐标
    block_x, block_y = pos_xy
    pos_x, pos_y = player_xy
    o_x, o_y = pos_x - Config.SCREEN_SIZE[0] // 2, pos_y - Config.SCREEN_SIZE[1] // 2
    vec = vec_sub((block_x, block_y), (o_x, o_y)) # 得到相对于左上角的坐标
    return vec

def get_pos_in_map(pos_on_screen, player_xy):   # 根据屏幕上的坐标计算玩家的坐标
    dW = Config.SCREEN_SIZE[0] // 2
    dH = Config.SCREEN_SIZE[1] // 2             # 玩家在屏幕上的位置
    vec = vec_sub(pos_on_screen, (dW, dH))      # 相对玩家的位移
    return vec_add(player_xy, vec)              # 得到游戏地图中的坐标

def circle_crash(pos1, R1, pos2, R2):
    return distance(pos1, pos2) <= R1 + R2 # 两个圆有相交部分

def not_in_screen(pos_xy, player_xy, R = 50): # 判断点在不在屏幕上
    pos = get_screen_pos(pos_xy, player_xy)
    dW = Config.SCREEN_SIZE[0] // 2 + R
    dH = Config.SCREEN_SIZE[1] // 2 + R # R 是对生物半径的修正
    return abs(pos[0] - dW) > dW and abs(pos[1] - dH) > dH

def random_near_position(xnow, ynow, Rmin, Rmax):
    """随机生成一个附近的点"""
    r = random.randint(Rmin, Rmax)
    theta = random.randint(-180, 179) / 360 * 2 * math.pi # rad
    dx = r * math.cos(theta)
    dy = r * math.sin(theta)
    x = xnow + dx
    y = ynow + dy
    return (x, y) # 返回一个附近的随机点

def average(lis1, lis2, alpha = 0.5):
    newlis = []
    for i in range(0, len(lis1)):
        newlis.append(lis1[i] * alpha + lis2[i] * (1-alpha))
    return tuple(newlis) # 将 list 打包成元组

def L1_dis(pos1, pos2): # 计算曼哈顿距离
    ans = 0
    for i in range(0, len(pos1)):
        ans += abs(pos1[i] - pos2[i]) # 每个维度计算差值的绝对值
    return ans

def get_mid_of_block(block_xy): # 根据网格坐标计算网格中点的地图坐标
    block_x, block_y = block_xy
    px, py = block_x * Config.BLOCK_SIZE, block_y * Config.BLOCK_SIZE
    half_block =  Config.BLOCK_SIZE // 2
    return (px + half_block, py + half_block) # 左上角坐标然后再加半个格子的坐标

def in_midddle(monster_pos):
    block_xy = get_block_xy(*monster_pos)
    mid = get_mid_of_block(block_xy)
    return distance(mid, monster_pos) < Config.POSITION_EPS # 离中心很近

def get_sec_in_game():
    """计算游戏开始到 现在/游戏结束 时所经过的秒数"""
    if Config.GAME_RUNNING:
        TIM = time.time() - Config.BEGIN_TIME
    else:
        TIM = Config.GAME_OVER_TIME - Config.BEGIN_TIME
    return int(TIM)

def get_game_time():
    TIM = get_sec_in_game()
    if TIM < 60:
        return str(TIM) + " sec"
    elif TIM >= 60 and TIM < 3600:
        return str(TIM // 60) + " min " + str(TIM % 60) + " sec"
    else:
        return str(TIM // 3600) + " hr " + str((TIM % 3600) // 60) + " min " + str(TIM % 60) + " sec"
