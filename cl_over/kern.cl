

__kernel void	test(const int x, const int y, const int z, __global float *a, __global float *res)
{
	uint	i = get_global_id(0);
	uint	j = get_global_id(1);
	int		k, l, m;
	float	tmp;

	tmp = 0;
	for (k = 0; k < x * y; k ++)
	{
		l = k / y;
		m = k - l * y;
		tmp += a[l * y * z + m * z + i] * a[l * y * z + m * z + j];
	}
	res[i * z + j] = tmp;
}
