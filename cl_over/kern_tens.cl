

__kernel void	get_bij_v1(const int X, const int Y, const int Z, const int len, __global float *a, __global float *temp, __global int *l, __global float *bij)
{
	uint	ti = get_global_id(0);
	uint	nb_temp = get_global_id(1);
	float	tmp;
	int		x, y1, y2, k;
	int		t1, t2;

	tmp = 0;
	for (k = 0; k < X * Y; k++)
	{
		x = k / Y;
		y1 = k - x * Y;
		y2 = k - x * Y + l[ti] - Y / 2;
		t1 = x * Y * Z + y1 * Z;
		t2 = x * len + y2;
		tmp += a[t2] * temp[t1 + nb_temp];
	}
	bij[ti * Z + nb_temp] = tmp;
}


__kernel void	get_temp_x(const int X, const int Y, const int Z, __global float *temp, __global float *out)
{
	uint	nb_temp = get_global_id(0);
	float	tmp;
	int		x, y, k;
	int		t1;

	printf("lol %d\n", nb_temp);
	for (k = 0; k < X * Y; k++)
	{
		x = k / Y;
		y = k - x * Y;
		t1 = x * Y * Z + y * Z;
		out[k] = temp[t1 + 1];
	}
}

__kernel void	get_sig(const int X, const int Y, const int Z, __global float *a, __global float *out)
{
	uint	ti = get_global_id(0);
	int		x, y, k, y2;
	int		t2;
	int		len;
	int		s;

	printf("lol\n");
	len = 15;
	s = 7;
	t2 = 0;
	for (k = 0; k < X * Y; k ++)
	{
		x = k / Y;
		y = k - x * Y;
		y2 = y + 5 - 3;
		t2 = x * len + y2;
		out[k] = a[t2];	
		printf("%d %d %d %d %d\n", k, x, y, y2, t2);
	}
}
