
//version1
__kernel void	test_v1(const int X, const int Y, const int Z, __global float *a, __global float *res)
{
	uint	i = get_global_id(0);
	uint	j = get_global_id(1);
	int		x, y, z;
	int		t;
	float	tmp;

	tmp = 0;
	for (z = 0; z < X * Y; z++)
	{
		//decompostion des coordonnees
		x = z / Y;
		y = z - x * Y;
		t = x * Y * Z + y * Z;
		tmp += a[t + i] * a[t + j];
	}
	res[i * Z + j] = tmp;
}

//version2 en cours de dev
__kernel void	test_v2(const int X, const int Y, const int Z, __global float *a, __global float *res, __local float *t1, __local float *t2)
{
	uint	i = get_global_id(0);
	uint	j = get_global_id(1);
	int		x, y, z;
	float	tmp;

	tmp = 0;
	for (z = 0; z < X * Y; z++)
	{
		x = z / Y;
		y = z - x * Y;
		tmp += a[x * Y * Z + y * Z + i] * a[x * Y * Z + y * Z + j];
	}
	res[i * Z + j] = tmp;
}

__kernel void	lol(void)
{
	uint i = get_local_id(0);
	uint i2 = get_local_id(1);
	uint j = get_global_id(0);
	uint j2 = get_global_id(1);
	uint k = get_group_id(0);
	uint size = get_local_size(0);

	printf("%d %d %d %d %d %d\n", j, j2, i, i2, k, size);
	barrier(CLK_GLOBAL_MEM_FENCE);
}
