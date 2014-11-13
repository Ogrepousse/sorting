

__kernel void	mat_dot(__global float* t1, __global float* t2, __global float* res)
{
	unsigned int	i;

	i = get_global_id(0);
	res[i] = t1[i] * t2[i];
}

__kernel void	mat_sum(__global float* t1, __global float* res)
{
	unsigned int	i;

	i = get_global_id(0);
	res[0] += t1[i];
}

__kernel void	init(__global float* buf)
{
	unsigned int	i;

	i = get_global_id(0);
	buf[i] = 0;
}


void			mat_dot2(__global float* t1, __global float* t2, __global float* res)
{
	unsigned int	i;

	i = get_global_id(0);
	res[i] = t1[i] * t2[i];
}


void			mat_sum2(float* a, __global float* res)
{
	unsigned int	i;

	i = get_global_id(0);
	res[0] += a[i];
}


__kernel void	mat_dot_and_sum(const int X, const int Y, __global float* t1, __global float* t2, __global float* dot,  __global float* res)
{


	mat_dot2(t1, t2, dot);
	mat_sum2(dot, res);
}

__kernel void	mat_reduce(__global float* dA, __global float* dB, __local float* prods, __global float *dC)
{

	int	gid = get_global_id(0);
	int	tnum = get_local_id(0);
	int	wgNum = get_group_id(0);
	int	numItems = get_local_size(0);

	prods[tnum] = dA[gid] * dB[gid];
	for (int offset = 1; offset <= numItems; offset *= 2)
	{
		int	mask = 2 * offset - 1;
		barrier(CLK_LOCAL_MEM_FENCE);
		if ((tnum & mask) == 0)
		{
			prods[tnum] += prods[tnum + offset];
		}
	}
	barrier(CLK_LOCAL_MEM_FENCE);
	if (tnum == 0)
		dC[wgNum] = prods[0];
}
