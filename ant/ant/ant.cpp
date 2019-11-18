
#include <iostream>
#include "Queue.h"
#define M 8
#define N 8

using namespace std;

int map[M + 2][N + 2] = {
{1,1,1,1,1,1,1,1,1,1},{1,0,0,1,0,0,0,1,0,1},{1,0,0,1,0,0,0,1,0,1},{1,0,0,0,0,1,1,0,0,1},{1,0,1,1,1,0,0,0,0,1},
{1,0,0,0,1,0,0,0,0,1},{1,0,1,0,0,0,1,0,0,1},{1,0,1,1,1,0,1,1,0,1},{1,1,0,0,0,0,0,0,0,1},{1,1,1,1,1,1,1,1,1,1}
};

void ShowPath(Queue *qu, int front)
{
	int p = front, p0;
	do
	{
		p0 = p;
		p = qu->data[p].pre;
		qu->data[p0].pre = -1;
	} while (p != 0); 
	cout << "最短路径：" << endl;
	for (int k = 0; k < MaxSize; k++)
	{
		if (qu->data[k].pre == -1)
		{
			cout << "(" << qu->data[k].i << "," << qu->data[k].j << ")";
			cout << "->";
		}
	}
}




bool Path(int x0, int y0, int x, int y) 
{
	int i, j, i0, j0;
	Box e;
	Queue * qu;
	InitQueue(qu);
	e.i = x0;
	e.j = y0;
	e.pre = -1;
	enQueue(qu, e);
	map[x0][y0] = -1; 

	while (!QueueEmpty(qu))

	{

		deQueue(qu, e);

		i = e.i;

		j = e.j;

		if (i == x && j == y)

		{

			ShowPath(qu, qu->front);

			DestroyQueue(qu);

			return true;

		}

		for (int circle = 0; circle < 4; circle++)

		{

			switch (circle)

			{

			case 0:

				i0 = i - 1;

				j0 = j;

				break;

			case 1:

				i0 = i;

				j0 = j + 1;

				break;

			case 2:

				i0 = i + 1;

				j0 = j;

				break;

			case 3:

				i0 = i;

				j0 = j - 1;

				break;

			}

			if (map[i0][j0] == 0)

			{

				e.i = i0;

				e.j = j0;

				e.pre = qu->front;

				enQueue(qu, e);

				map[i0][j0] = -1;

			}

		}

	}

	DestroyQueue(qu);

	return false;

}

int main()

{

	if (!Path(1, 1, 8, 8))

		cout << "迷宫无正确路径";
	getchar();
	return 0;

}