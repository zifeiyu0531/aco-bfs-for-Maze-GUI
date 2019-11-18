# -*- coding: utf-8 -*-

import wx
import sys, os
import random
import aco
import bfs

APP_TITLE = u'蚁群&广度优先迷宫问题演示'


class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''

    maze_init = False
    maze_size = 0
    w = 0
    h = 0

    def __init__(self):
        '''构造函数'''

        wx.Frame.__init__(self, None, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        # 默认style是下列项的组合：wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN 

        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((800, 600))
        self.Center()


        # 以下可以添加各类控件
        self.preview = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
        self.preview.SetBackgroundColour(wx.Colour(0, 0, 0))
        aco = aco_btn = wx.Button(self, -1, u'蚁群算法', size=(100, -1))
        bfs = bfs_btn = wx.Button(self, -1, u'广度优先算法', size=(100, -1))
        maze = maze_btn = wx.Button(self, -1, u'生成迷宫', size=(100, -1))
        self.tip1 = wx.StaticText(self, -1, u'', pos=(145, 110), size=(150, -1), style=wx.ST_NO_AUTORESIZE)
        self.tip2 = wx.StaticText(self, -1, u'选择迷宫尺寸', pos=(145, 110), size=(150, -1), style=wx.ST_NO_AUTORESIZE)
        self.check1 = wx.RadioButton(self, -1, "10", pos=(50, 20), size=(50, 10))
        self.check2 = wx.RadioButton(self, -1, "20", pos=(100, 20), size=(50, 10))
        self.check3 = wx.RadioButton(self, -1, "50", pos=(150, 20), size=(50, 10))
        self.tip3 = wx.StaticText(self, -1, u'起点为左上角红色块\n终点为右下角红色块', pos=(145, 110), size=(150, -1), style=wx.ST_NO_AUTORESIZE)

        sizer_right = wx.BoxSizer(wx.VERTICAL)
        sizer_right.Add(aco_btn, 0, wx.ALL, 20)
        sizer_right.Add(bfs_btn, 0, wx.ALL, 20)
        sizer_right.Add(maze_btn, 0, wx.ALL, 20)
        sizer_right.Add(self.tip1, 0, wx.ALL, 20)
        sizer_right.Add(self.tip2, 0, wx.ALL, 20)
        sizer_right.Add(self.check1, 0, wx.ALL, 20)
        sizer_right.Add(self.check2, 0, wx.ALL, 20)
        sizer_right.Add(self.check3, 0, wx.ALL, 20)
        sizer_right.Add(self.tip3, 0, wx.ALL, 20)


        sizer_max = wx.BoxSizer()
        sizer_max.Add(self.preview, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 5)
        sizer_max.Add(sizer_right, 0, wx.EXPAND | wx.ALL, 0)

        self.SetAutoLayout(True)
        self.SetSizer(sizer_max)
        self.Layout()

        aco.Bind(wx.EVT_BUTTON, self.btn_click)
        bfs.Bind(wx.EVT_BUTTON, self.btn_click)
        maze.Bind(wx.EVT_BUTTON, self.btn_click)
        self.check1.Bind(wx.EVT_RADIOBUTTON, self.check_size)
        self.check2.Bind(wx.EVT_RADIOBUTTON, self.check_size)
        self.check3.Bind(wx.EVT_RADIOBUTTON, self.check_size)

    def btn_click(self, evt):

        dc = wx.ClientDC(self.preview)
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))

        event = evt.GetEventObject()
        if event.GetLabel() == '蚁群算法' or event.GetLabel() == '广度优先算法':
            if not self.maze_init:
                dlg = wx.MessageDialog(None, u'迷宫未建立', u'操作提示')
                dlg.ShowModal()
                self.tip1.SetLabel(u'迷宫未建立')
            else:
                if event.GetLabel() == '蚁群算法':
                    self.tip1.SetLabel(u'蚁群算法开始')
                    if not aco.start(self.maze_size, self.w, self.h, dc):
                        dlg = wx.MessageDialog(None, u'迷宫无解', u'操作提示')
                        dlg.ShowModal()
                    dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                else:
                    self.tip1.SetLabel(u'广度优先算法开始')
                    if not bfs.start(self.maze_size, self.w, self.h, dc):
                        dlg = wx.MessageDialog(None, u'迷宫无解', u'操作提示')
                        dlg.ShowModal()
                    dc.SetBrush(wx.Brush(wx.Colour(255, 0, 255)))
        else:
            if self.maze_size == 0:
                dlg = wx.MessageDialog(None, u'请先选择迷宫尺寸', u'操作提示')
                dlg.ShowModal()
                return

            aco.temp_map = aco.init_map(self.maze_size)
            bfs.temp_map = bfs.init_map(self.maze_size)

            self.tip1.SetLabel(u'迷宫建立')
            self.maze_init = True

            self.w, self.h = self.preview.GetSize()
            self.w /= self.maze_size
            self.h /= self.maze_size

            for i in range(self.maze_size):
                for j in range(self.maze_size):
                    dc.DrawRectangle(i*self.w, j*self.h, self.w, self.h)

            dc.SetBrush(wx.Brush(wx.Colour(255, 0, 0)))
            dc.DrawRectangle(0, 0, self.w, self.h)
            dc.DrawRectangle((self.maze_size - 1) * self.w, (self.maze_size - 1) * self.h, self.w, self.h)

            dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0)))

            for index in range((int)((self.maze_size**2) * 0.3)):
                i = random.randint(0,self.maze_size-1)
                j = random.randint(0,self.maze_size-1)
                if i + j > 0 and i * j != (self.maze_size-1)**2:
                    aco.temp_map[i+1][j+1] = 1
                    bfs.temp_map[i+1][j+1] = 1
                    dc.DrawRectangle(i*self.w, j*self.h, self.w, self.h)
            print(aco.temp_map)


    def check_size(self, evt):
        event = evt.GetEventObject()
        if event.GetLabel() == '10':
            self.maze_size = 10
        elif event.GetLabel() == '20':
            self.maze_size = 20
        elif event.GetLabel() == '50':
            self.maze_size = 50
        print(self.maze_size)

class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame()
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
