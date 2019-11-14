#include<iostream>
#include<stack>
#include<bitset>
using namespace std;
//坐标类
struct Point
{
	int x;
	int y;
};
//地图类
template<int A, int B>
class Map
{
public:
	int(*p)[B];//1表示为障碍方格，0表示该方格可通
	bitset<4>(*around)[B];//记录每一个方格四周四个方法的可选标记
	int row;//行数
	int col;//列数
	Map()
	{
		p = new int[A][B];
		around = new bitset<4>[A][B];
	}
	Map(Map<A, B> & B1)
	{
		p = new int[A][B];
		around = new bitset<4>[A][B];
		row = B1.row;
		col = B1.col;
		for (int i = 0; i < row; i++)
		{
			for (int j = 0; j < col; j++)
			{
				p[i][j] = B1.p[i][j];
				around[i][j] = B1.around[i][j];
			}
		}
	}
	Map<A, B> & operator=(Map<A, B> & B1)
	{
		row = B1.row;
		col = B1.col;
		for (int i = 0; i < row; i++)
		{
			for (int j = 0; j < col; j++)
			{
				this->p[i][j] = B1.p[i][j];
				around[i][j] = B1.around[i][j];
			}
		}
		return *this;
	}
};

//start起始点， end终止点
template<int A, int B>
bool FindPath(Map<A, B> & map, Point & start, Point & end)
{
	const int N1 = A;
	const int N2 = B;

	const int M = 10;//每一轮中蚂蚁的个数
	const int RcMax = 20;//迭代次数
	const int IN = 1;//信息素的初始量

	double add[N1][N2];//每一段的信息素增量数组
	double phe[N1][N2];//每一段路径上的信息素
	double MAX = 0x7fffffff;

	double alphe, betra, rout, Q;//alphe信息素的影响因子，betra路线距离的影响因子，rout信息素的保持度，Q用于计算每只蚂蚁在其路迹留下的信息素增量
	double bestSolution = MAX;//最短距离
	stack<Point> Beststackpath;//最优路线

	//初始化变量参数和信息数组
	alphe = betra = 2;
	rout = 0.7;
	Q = 10;

	//先给图的外围加上障碍
	for (int i = 0; i < map.col; i++)
	{
		map.p[0][i] = map.p[map.row - 1][i] = 1;
	}
	for (int i = 0; i < map.row; i++)
	{
		map.p[i][0] = map.p[i][map.col - 1] = 1;
	}
	//初始化图中每一个方格的四周访问表示位，0表示可访问
	//初始化信息素数组
	for (int i = 0; i < N1; i++)
	{
		for (int j = 0; j < N2; j++)
		{
			phe[i][j] = IN;
			map.around[i][j].reset();//4个方向全部设为可选
		}
	}

	//用于方向选择的偏移量数组   按照顺时针的方向
	Point offset[4];
	offset[0].x = 0; offset[0].y = 1;//向右
	offset[1].x = 1; offset[1].y = 0;//向下
	offset[2].x = 0; offset[2].y = -1;//向左
	offset[3].x = -1; offset[3].y = 0;//向上

	//每轮M只蚂蚁，每一轮结束后才进行全局信息素更新
	stack<Point> stackpath[M];
	//拷贝障碍地图
	Map<A, B> Ini_map[M];
	//记录每一只蚂蚁的当前位置
	Point Allposition[M];

	int s = 0;
	while (s < RcMax)//一共RcMax轮
	{

		//先清空每一只蚂蚁的路线存储栈
		for (int i = 0; i < M; i++)
		{
			while (!stackpath[i].empty())
			{
				stackpath[i].pop();
			}
		}
		for (int i = 0; i < M; i++)
		{
			Ini_map[i] = map;
			//将起点初始化为障碍点
			Ini_map[i].p[start.x][start.y] = 1;
			//起点入栈
			stackpath[i].push(start);
			//初始化每一只蚂蚁的当前位置
			Allposition[i] = start;
		}

		//开启M只蚂蚁循环
		for (int j = 0; j < M; j++)
		{
			cout << "第" << j << "只蚂蚁" << endl;
			while (((Allposition[j].x) != (end.x) || (Allposition[j].y) != (end.y)))
			{
				cout << "<" << Allposition[j].x << "," << Allposition[j].y << ">" << endl;
				//选择下一步
				double psum = 0;
				for (int op = 0; op < 4; op++)
				{
					//计算下一个可能的坐标
					int x = Allposition[j].x + offset[op].x;
					int y = Allposition[j].y + offset[op].y;

					if ((Ini_map[j].around[Allposition[j].x][Allposition[j].y])[op] == 0 && Ini_map[j].p[x][y] != 1)
					{
						psum += pow(phe[x][y], alphe) * pow((10.0 / stackpath[j].size()), betra);
					}
				}
				//判断是否有选择
				//如找到了下一点
				if (psum != 0)
				{
					double drand = (double)(rand()) / (RAND_MAX + 1);
					double pro = 0;
					int re;
					int x, y;
					for (re = 0; re < 4; re++)
					{
						//计算下一个可能的坐标
						x = Allposition[j].x + offset[re].x;
						y = Allposition[j].y + offset[re].y;
						if ((Ini_map[j].around[Allposition[j].x][Allposition[j].y])[re] == 0 && Ini_map[j].p[x][y] != 1)
						{
							pro += (pow(phe[x][y], alphe) * pow((10.0 / stackpath[j].size()), betra)) / psum;
							if (pro >= drand)
							{
								break;
							}
						}
					}

					//入栈
					Allposition[j].x = x;
					Allposition[j].y = y;
					stackpath[j].push(Allposition[j]);
					//设置障碍
					Ini_map[j].p[Allposition[j].x][Allposition[j].y] = 1;

				}
				else//没找到了下一点
				{
					//向后退一步，出栈
					stackpath[j].pop();
					//消除入栈时设置的障碍
					Ini_map[j].p[Allposition[j].x][Allposition[j].y] = 0;
					if (stackpath[j].empty())
					{
						return false;
						//cout << "失败" << endl;
					}
					//设置回溯后的Allposition
					if (Allposition[j].x == stackpath[j].top().x)
					{
						if ((Allposition[j].y - stackpath[j].top().y) == 1)//向右
						{
							(Ini_map[j].around[stackpath[j].top().x][stackpath[j].top().y])[0] = 1;//标记该方向已访问
						}
						if ((Allposition[j].y - stackpath[j].top().y) == -1)//向左
						{
							(Ini_map[j].around[stackpath[j].top().x][stackpath[j].top().y])[2] = 1;//标记该方向已访问
						}
					}
					if (Allposition[j].y == stackpath[j].top().y)
					{

						if ((Allposition[j].x - stackpath[j].top().x) == 1)//向下
						{
							(Ini_map[j].around[stackpath[j].top().x][stackpath[j].top().y])[1] = 1;//标记该方向已访问
						}
						if ((Allposition[j].x - stackpath[j].top().x) == -1)//向上
						{
							(Ini_map[j].around[stackpath[j].top().x][stackpath[j].top().y])[3] = 1;//标记该方向已访问
						}
					}
					Allposition[j].x = stackpath[j].top().x;
					Allposition[j].y = stackpath[j].top().y;
				}

			}
		}

		//保存最优路线
		double solution = 0;
		for (int i = 0; i < M; i++)
		{
			solution = 0;
			solution = stackpath[i].size();
			if (solution < bestSolution)
			{
				Beststackpath = stackpath[i];
				bestSolution = solution;
			}
		}
		//计算每一只蚂蚁在其每一段路径上留下的信息素增量
		//初始化信息素增量数组
		for (int i = 0; i < N1; i++)
		{
			for (int j = 0; j < N2; j++)
			{
				add[i][j] = 0;
			}
		}

		for (int i = 0; i < M; i++)
		{
			//先算出每只蚂蚁的路线的总距离solu
			double solu = 0;
			solu = stackpath[i].size();
			double d = Q / solu;
			while (!stackpath[i].empty())
			{
				add[stackpath[i].top().x][stackpath[i].top().y] += d;
				stackpath[i].pop();
			}
		}
		//更新信息素
		for (int i = 0; i < N1; i++)
		{
			for (int j = 0; j < N2; j++)
			{
				phe[i][j] = phe[i][j] * rout + add[i][j];
				//为信息素设置一个下限值和上限值
				if (phe[i][j] < 0.0001)
				{
					phe[i][j] = 0.0001;
				}
				if (phe[i][j] > 20)
				{
					phe[i][j] = 20;
				}
			}
		}

		s++;
	}//轮

	//找到路径，并输出stackpath
	cout << "找到最优路径！" << endl;
	cout << "最短路线长度为： 共" << Beststackpath.size() << "个方格！" << endl;
	while (!Beststackpath.empty())
	{
		cout << "<" << Beststackpath.top().x << "," << Beststackpath.top().y << ">" << endl;
		Beststackpath.pop();
	}

	return true;
}

int main()
{
	//建立迷宫
	Map<10, 10> map;
	map.col = map.row = 10;
	int p[10][10];
	for (int i = 0; i < 10; i++)//初始化迷宫
	{
		for (int j = 0; j < 10; j++)
		{
			p[i][j] = 0;
		}
	}
	//为迷宫设置障碍
	p[1][3] = 1; p[1][7] = 1; p[2][3] = 1; p[2][7] = 1;
	p[3][5] = 1; p[3][6] = 0; p[4][2] = 1; p[4][3] = 1;
	p[4][4] = 1; p[5][4] = 1; p[6][2] = 1; p[6][6] = 1;
	p[7][2] = 1; p[7][3] = 1; p[7][4] = 1; p[7][6] = 1;
	p[8][1] = 1;
	map.p = p;
	Point start, end;
	start.x = start.y = 1;
	end.x = 8, end.y = 8;
	if (!FindPath<10, 10>(map, start, end))
	{
		cout << "该迷宫无解！" << endl;
	}
	getchar();
}