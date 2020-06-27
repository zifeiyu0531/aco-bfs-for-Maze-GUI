from collections import deque
import wx
import time

MAX_VALUE = 0x7fffffff

temp_map = [[]]

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def init_map(maze_size):
    temp_map = [[0 for y in range(maze_size + 2)] for x in range(maze_size + 2)]
    for i in range(len(temp_map)):
        temp_map[i][0] = temp_map[i][len(temp_map)-1] = 1
    for i in range(len(temp_map[0])):
        temp_map[0][i] = temp_map[len(temp_map[0]) - 1][i] = 1
    return temp_map

def bfs(maze, begin, end, w, h, dc):
    n, m = len(maze), len(maze[0])
    dist = [[MAX_VALUE for _ in range(m)] for _ in range(n)]
    pre = [[None for _ in range(m)] for _ in range(n)]  # 当前点的上一个点,用于输出路径轨迹

    dx = [1, 0, -1, 0]  # 四个方位
    dy = [0, 1, 0, -1]
    sx, sy = begin.x, begin.y
    gx, gy = end.x, end.y

    dist[sx][sy] = 0
    queue = deque()
    queue.append(begin)

    while queue:
        curr = queue.popleft()
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        dc.DrawRectangle((curr.y - 1) * w, (curr.x - 1) * h, w, h)
        find = False
        for i in range(4):
            nx, ny = curr.x + dx[i], curr.y + dy[i]
            if 0 <= nx < n and 0 <= ny < m and maze[ny][nx] != 1 and dist[nx][ny] == MAX_VALUE:
                dist[nx][ny] = dist[curr.x][curr.y] + 1
                pre[nx][ny] = curr
                queue.append(Point(nx, ny))
                dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
                dc.DrawRectangle((ny-1) * w, (nx-1) * h, w, h)
                time.sleep(0.05)
                if nx == gx and ny == gy:
                    find = True
                    break
        if find:
            while queue:
                curr = queue.popleft()
                dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                dc.DrawRectangle((curr.y - 1) * w, (curr.x - 1) * h, w, h)

            stack = []
            curr = end
            while True:
                stack.append(curr)
                if curr.x == begin.x and curr.y == begin.y:
                    break
                prev = pre[curr.x][curr.y]
                curr = prev
            while stack:
                curr = stack.pop()
                dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
                dc.DrawRectangle((curr.y - 1) * w, (curr.x - 1) * h, w, h)
            return True

    return False

def start(maze_size, w, h, dc):
    maze = temp_map
    begin = Point(1, 1)
    print(maze)
    end = Point(maze_size, maze_size)
    return bfs(maze, begin, end, w, h, dc)