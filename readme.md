# Background
蚁群算法&广度优先算法求解迷宫最优路径问题(附带GUI)<br>
视频地址：[bilibili:【算法】蚁群算法&广度优先求解迷宫最短路径](https://www.bilibili.com/video/BV1gJ411G7Xi)<br>
# Install
##### step1.clone该Repository到你的本地路径
##### step2.解压缩
项目结构：
>aco-bfs-for-Maze-GUI   `根目录`<br>
>>GUI.exe               `打包的exe文件`<br>
>>readme.md             `readme文件`<br>
>>src                   `源代码文件`<br>
>>>GUI.py               `GUI代码文件`<br>
>>>aco.py               `蚁群算法代码文件`<br>
>>>bfs.py               `广度优先算法代码文件`<br>
##### step3.安装项目运行时所需要的外部库
wxpython:GUI图形库<br>
[安装教程](https://www.cnblogs.com/icelee1218/p/8127670.html)<br>
# Usage
使用任意python代码编辑器或IDE打开`src`文件<br>
运行`GUI.py`<br>
![image](https://github.com/zifeiyu0531/readme-imgs/blob/master/aco-bfs-for-Maze-GUI/start.png)<br>
选择`迷宫尺寸`<br>
点击`生成迷宫`<br>
![image](https://github.com/zifeiyu0531/readme-imgs/blob/master/aco-bfs-for-Maze-GUI/maze.png)<br>
点击`蚁群算法`执行蚁群算法动画，点击`广度优先算法`执行广度优先算法动画<br>
# Pack
可使用[PyInstaller](http://www.pyinstaller.org/)将该项目打包成exe格式。<br>
`PyInstaller`安装：
```
pip install pyinstaller
```
使用：
```
pyinstaller -F -w GUI.py
```
在`GUI.py`相同目录下会新增`dist`文件夹，内部放有`GUI.exe`文件
