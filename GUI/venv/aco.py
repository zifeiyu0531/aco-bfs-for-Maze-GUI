import copy
import math
import random
import wx
import time
from queue import Queue

temp_map = [[]]

class Stack(object):
    def __init__(self):
        self.stack = []

    def push(self, value):    # 进栈
        self.stack.append(value)

    def pop(self):  #出栈
        return self.stack.pop()

    def empty(self): # 如果栈为空
        if len(self.stack) == 0:
            return True
        else:
            return False

    def top(self):
        #取出目前stack中最新的元素
        return self.stack[-1]

    def size(self):
        return len(self.stack)

#坐标类
class Point:
    x = 0
    y = 0

#地图类
class Map:
    p = [[]]
    around = [[[]]]
    row = 0#行数
    col = 0#列数
    def __init__(self,A, B):
        self.p = [[0 for y in range(B)] for x in range(A)] #1表示为障碍方格，0表示该方格可通
        self.around = [[[0 for z in range(4)] for y in range(B)] for x in range(A)]  #记录每一个方格四周四个方法的可选标记

def init_map(maze_size):
    return [[0 for y in range(maze_size+2)] for x in range(maze_size+2)]


#start起始点， end终止点
def FindPath(map: Map, start: Point, end: Point, A: int, B: int, w, h, dc, temp_phe):
    N1 = A
    N2 = B

    M = 10#每一轮中蚂蚁的个数
    RcMax = 10#迭代次数
    IN = 1.0#信息素的初始量

    add = [[0.0 for j in range(N2)] for i in range(N1)]#每一段的信息素增量数组
    phe = [[0.0 for j in range(N2)] for i in range(N1)]#每一段路径上的信息素
    MAX = 0x7fffffff

    bestSolution = MAX#最短距离
    Beststackpath = Stack()#最优路线

    # alphe信息素的影响因子，betra路线距离的影响因子，rout信息素的保持度，Q用于计算每只蚂蚁在其路迹留下的信息素增量
    #初始化变量参数和信息数组
    alphe, betra = 2.0, 2.0
    rout = 0.7
    Q = 10.0

    #先给图的外围加上障碍
    for i in range(map.col):
        map.p[0][i] = map.p[map.row - 1][i] = 1

    for i in range(map.row):
        map.p[i][0] = map.p[i][map.col - 1] = 1

    print(map.p)
    #初始化图中每一个方格的四周访问表示位，0表示可访问
    #初始化信息素数组
    for i in range(N1):
        for j in range(N2):
            phe[i][j] = IN

    #用于方向选择的偏移量数组   按照顺时针的方向
    offset = [Point() for i in range(4)]
    offset[0].x = 0
    offset[0].y = 1#向右
    offset[1].x = 1
    offset[1].y = 0#向下
    offset[2].x = 0
    offset[2].y = -1#向左
    offset[3].x = -1
    offset[3].y = 0#向上

    #每轮M只蚂蚁，每一轮结束后才进行全局信息素更新
    stackpath = [Stack() for i in range(M)]
    #拷贝障碍地图
    Ini_map = [Map(A, B) for i in range(M)]
    #记录每一只蚂蚁的当前位置
    Allposition = [Point() for i in range(M)]

    s = 0
    while s < RcMax:#一共RcMax轮
        #先清空每一只蚂蚁的路线存储栈
        for i in range(M):
            while stackpath[i].empty() is False:
                stackpath[i].pop()

        for i in range(M):
            Ini_map[i] = copy.deepcopy(map)
            #将起点初始化为障碍点
            Ini_map[i].p[start.x][start.y] = 1
            #起点入栈
            stackpath[i].push(start)
            #初始化每一只蚂蚁的当前位置
            Allposition[i] = copy.deepcopy(start)

        #开启M只蚂蚁循环
        for j in range(M):
            print("第" + str(j) +"只蚂蚁")
            while (Allposition[j].x) != (end.x) or (Allposition[j].y) != (end.y):
                print("<" + (str)(Allposition[j].x) + "," + (str)(Allposition[j].y) + ">")
                if temp_phe.full():
                    white_point = temp_phe.get()
                    dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                    dc.DrawRectangle(white_point[0], white_point[1], w, h)
                temp_phe.put([(Allposition[j].x-1) * w, (Allposition[j].y-1) * h])
                dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
                dc.DrawRectangle((Allposition[j].x-1) * w, (Allposition[j].y-1) * h, w, h)

                #选择下一步
                psum = 0.0
                for op in range(4):
                    #计算下一个可能的坐标
                    x = Allposition[j].x + offset[op].x
                    y = Allposition[j].y + offset[op].y
                    if (Ini_map[j].around[Allposition[j].x][Allposition[j].y])[op] == 0 and Ini_map[j].p[x][y] != 1:
                        psum += math.pow(phe[x][y], alphe) * math.pow((10.0 / stackpath[j].size()), betra)
                #判断是否有选择
                #如找到了下一点
                if psum != 0.0:
                    drand = random.uniform(0, 1)
                    pro = 0.0
                    re = 0
                    x, y = 0, 0
                    for re in range(4):
                        #计算下一个可能的坐标
                        x = Allposition[j].x + offset[re].x
                        y = Allposition[j].y + offset[re].y
                        if (Ini_map[j].around[Allposition[j].x][Allposition[j].y])[re] == 0 and Ini_map[j].p[x][y] != 1:
                            pro += (pow(phe[x][y], alphe) * pow((10.0 / stackpath[j].size()), betra)) / psum
                            if pro >= drand:
                                break
                    #入栈
                    Allposition[j].x = x
                    Allposition[j].y = y
                    temp_Point = copy.deepcopy(Allposition[j])
                    stackpath[j].push(temp_Point)
                    #设置障碍
                    Ini_map[j].p[Allposition[j].x][Allposition[j].y] = 1
                else:#没找到了下一点
                    #向后退一步，出栈
                    p = stackpath[j].pop()
                    dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                    dc.DrawRectangle((Allposition[j].x - 1) * w, (Allposition[j].y - 1) * h, w, h)
                    #消除入栈时设置的障碍
                    Ini_map[j].p[Allposition[j].x][Allposition[j].y] = 0
                    if stackpath[j].empty() == True:
                        return False
                    #设置回溯后的Allposition
                    if Allposition[j].x == stackpath[j].top().x:
                        if (Allposition[j].y - stackpath[j].top().y) == 1:#向右
                            (Ini_map[j].around[stackpath[j].top().x][stackpath[j].top().y])[0] = 1#标记该方向已访问
                        if (Allposition[j].y - stackpath[j].top().y) == -1:#向左
                            (Ini_map[j].around[stackpath[j].top().x][stackpath[j].top().y])[2] = 1#标记该方向已访问
                    if Allposition[j].y == stackpath[j].top().y:
                        if (Allposition[j].x - stackpath[j].top().x) == 1:#向下
                            (Ini_map[j].around[stackpath[j].top().x][stackpath[j].top().y])[1] = 1#标记该方向已访问
                        if (Allposition[j].x - stackpath[j].top().x) == -1:#向上
                            (Ini_map[j].around[stackpath[j].top().x][stackpath[j].top().y])[3] = 1#标记该方向已访问

                    Allposition[j].x = stackpath[j].top().x
                    Allposition[j].y = stackpath[j].top().y
        #保存最优路线
        solution = 0
        for i in range(M):
            solution = 0
            solution = stackpath[i].size()
            if solution < bestSolution:
                Beststackpath = copy.deepcopy(stackpath[i])
                bestSolution = solution

        #计算每一只蚂蚁在其每一段路径上留下的信息素增量
        #初始化信息素增量数组
        for i in range(N1):
            for j in range(N2):
                add[i][j] = 0

        for i in range(M):
            #先算出每只蚂蚁的路线的总距离solu
            solu = stackpath[i].size()
            d = Q / solu
            while stackpath[i].empty() == False:
                add[stackpath[i].top().x][stackpath[i].top().y] += d
                stackpath[i].pop()

        #更新信息素
        for i in range(N1):
            for j in range(N2):
                phe[i][j] = phe[i][j] * rout + add[i][j]
                #为信息素设置一个下限值和上限值
                if phe[i][j] < 0.0001:
                    phe[i][j] = 0.0001
                if phe[i][j] > 20:
                    phe[i][j] = 20
        s += 1
    #轮
    dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
    while not temp_phe.empty():
        white_point = temp_phe.get()
        dc.DrawRectangle(white_point[0], white_point[1], w, h)

    dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))

    #找到路径，并输出stackpath
    print("找到最优路径！")
    print("最短路线长度为： 共" + (str)(Beststackpath.size()) + "个方格！")
    while Beststackpath.empty() == False:
        print("<" + (str)(Beststackpath.top().x) + "," + (str)(Beststackpath.top().y) + ">")
        dc.DrawRectangle((Beststackpath.top().x - 1) * w, (Beststackpath.top().y - 1) * h, w, h)
        Beststackpath.pop()
    return True

def start(maze_size, w, h, dc):
    temp_phe = Queue(maxsize = maze_size*2)
    map = Map(maze_size+2, maze_size+2)
    map.col, map.row = maze_size+2, maze_size+2

    map.p = temp_map
    start, end = Point(), Point()
    start.x, start.y = 1, 1
    end.x, end.y = maze_size, maze_size
    return FindPath(map, start, end, map.col, map.row, w, h, dc, temp_phe)
