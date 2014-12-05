

__kernel void	get_bij_v1(const int X, const int Y, const int Z, __global float *a, __global float *temp, __global int *l, __global float *bij)
{
	uint	ti = get_global_id(0);
	uint	nb_temp = get_global_id(1);
	float	tmp;
	int		x, y, z;
	int		t1, t2;

	tmp = 0;
	for (z = 0; z < X * Y; z++)
	{
		x = z / Y;
		y = z - x * Y;
		t1 = x * Y * Z + y * Z;
		t2 = (l[ti] - 64 + x) * Y + y;
		tmp += a[t2] * temp[t1 + nb_temp];
	}
	bij[ti + nb_temp * 3] = tmp;
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
	int		x, y, k;
	int		t2;

	printf("lol\n");
	for (k = 0; k < X * Y; k ++)
	{
		x = k / Y;
		y = k - x * Y + x * 3;
		t2 = (5 - 3) + x * Y + y;
		printf("%d %d %d %d\n", k, x, y, t2);
		out[k] = a[t2];
	}
}
