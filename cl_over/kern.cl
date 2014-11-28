
//version1
__kernel void	test_v1(const int X, const int Y, const int Z, __global float *a, __global float *res)
{
	uint	i = get_global_id(0);
	uint	j = get_global_id(1);
	int		x, y, z;
	float	tmp;

	tmp = 0;
	for (z = 0; z < X * Y; z++)
	{
		//decompostion des coordonnees
		x = z / Y;
		y = z - x * Y;
		tmp += a[x * Y * Z + y * Z + i] * a[x * Y * Z + y * Z + j];
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

__kernel void	lol(__global float* a, __local float* l)
{
	uint i = get_local_id(0);

	l[i] = a[i];
}
