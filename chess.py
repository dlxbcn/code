import pygame # 导入包

# 初始化
pygame.init()

# 设置标题
pygame.display.set_caption("五子棋")

# 设置图标
icon = pygame.image.load("./images/wzq.png")
pygame.display.set_icon(icon)

# 背景图片
bg = pygame.image.load("./images/chessboard.png") # 加载背景图片
调整尺寸的图片 = pygame.transform.scale(bg, (800, 600)) # 调整背景图片的大小
# 定义窗口大小
screen = pygame.display.set_mode((800,700))

黑棋 = 1
白棋 = 2
当前棋子 = 黑棋
棋盘地图 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

单元格长度 = 40
单元格数量 = 14
总长度 = 单元格长度 * 单元格数量
起始点_x = 100
起始点_y = 50
黑色 = (0,0,0)
白色 = (255, 255, 255)
def 画棋盘():
    # 画横线
    for i in range(15):
        # draw: 画   line:线
        # 画线函数参数 pygame.draw.line(窗口, 颜色, 起始位置, 结束位置, 线条宽度) 
        # 画线函数举例 pygame.draw.line(screen, 黑色, (100, 100), (500, 100), 1)
        x0 = 起始点_x
        y0 = 起始点_y + 单元格长度 * i
        x1 = x0 + 总长度
        y1 = y0
        pygame.draw.line(screen, 黑色, (x0 , y0), (x1, y1), 1)

    # 画竖线
    for j in range(15):
        x0 = 起始点_x + 单元格长度 * j
        y0 = 起始点_y 
        x1 = x0
        y1 = y0 + 总长度
        pygame.draw.line(screen, 黑色, (x0 , y0), (x1, y1), 1)

    # 画中心圆点
    x0 = 起始点_x + 总长度/2
    y0 = 起始点_y + 总长度/2
    pygame.draw.circle(screen, 黑色, (x0, y0), 4)


def 画棋子():
    # 画棋子
    for 行号 in range(15):
        for 列号 in range(15):
            if 棋盘地图[行号][列号] == 黑棋:
                x = 起始点_x + 列号 * 单元格长度
                y = 起始点_y + 行号 * 单元格长度
                pygame.draw.circle(screen, 黑色, (x, y), 18)
            elif 棋盘地图[行号][列号] == 白棋:
                x = 起始点_x + 列号 * 单元格长度
                y = 起始点_y + 行号 * 单元格长度
                pygame.draw.circle(screen, 白色, (x, y), 18)


def 下棋(鼠标点击位置):
    # 坐标转换为下标，并修改棋盘地图
    pass

            

def check_winner(row, col, chess):
    # row行 col列 chess黑棋或白棋
    #检查是否连接成5子
    count = 1
    # 向右检查
    for i in range(1, 5):
        if col+i <= 单元格数量 and 棋盘地图[row][col+i] == chess:
            count += 1
    # # 向左检查
    for i in range(1, 5):
        if col-i>=0 and 棋盘地图[row][col-i] == chess:
            count += 1
    print(count)
    if count >= 5:
        return chess

    # # 向上检查
    # count = 1
    # for i in range(1, 5):
    #     if col-i>=0 and 棋盘地图[row-i][col] == chess:
    #         count += 1
    # # 向下检查
    # for i in range(1, 5):
    #     if col+i <= 单元格数量 and 棋盘地图[row+i][col] == chess:
    #         count += 1
    # if count >= 5:
    #     return chess
    return None

def 坐标转换为下标(pos):
    for 行号 in range(15):
        for 列号 in range(15):
            x = 起始点_x + 列号 * 单元格长度
            y = 起始点_y + 行号 * 单元格长度
            if (x - 20 <= 鼠标点击位置[0] <= x + 20) \
                and (y - 20 <= 鼠标点击位置[1] <= y + 20) \
                and 棋盘地图[行号][列号] == 0:
                    return 行号, 列号
    return None, None

# 运行循环
while True:
    事件列表 = pygame.event.get() # 读取消息列表
    for 事件 in 事件列表:  # 循环读取消息列表中的每一个消息
        if 事件.type == pygame.QUIT: # 判断消息类型是否为退出消息
            pygame.quit() # pygame 退出 
            exit() # python 退出
        elif 事件.type == pygame.MOUSEBUTTONDOWN: # 判断是否是鼠标点击事件
            if 事件.button == pygame.BUTTON_LEFT: # 判断是否是鼠标左键
                鼠标点击位置 = pygame.mouse.get_pos() # 得到鼠标当前的位置
                print(鼠标点击位置)
                row, col = 坐标转换为下标(鼠标点击位置)
                if row is not None and col is not None:
                    棋盘地图[row][col] = 当前棋子
                    if check_winner(row, col, 当前棋子) != None:
                        print("有人赢了")
                    当前棋子 = 黑棋 if 当前棋子==白棋 else 白棋 # 黑白切换
                # for 行号 in range(15):
                #     for 列号 in range(15):
                #         x = 起始点_x + 列号 * 单元格长度
                #         y = 起始点_y + 行号 * 单元格长度
                #         # 判断当前位置偏移值小于20，并且当前位置没有棋子
                #         if (x - 20 <= 鼠标点击位置[0] <= x + 20) \
                #             and (y - 20 <= 鼠标点击位置[1] <= y + 20) \
                #             and 棋盘地图[行号][列号] == 0:
                #                 棋盘地图[行号][列号] = 当前棋子
                #                 if check_winner(行号, 行号, 当前棋子) != None:
                #                     print("有人赢了")
                #                 当前棋子 = 黑棋 if 当前棋子==白棋 else 白棋 # 黑白切换


    # 填充背景图片
    screen.blit(bg, bg.get_rect())

    画棋盘()
    
    画棋子()

    # screen.fill((255,255,255))  # 窗口填充白色
    pygame.display.flip() # 窗口全部刷新
    # pygame.display.update() # 窗口全部刷新(可以局部刷新)
