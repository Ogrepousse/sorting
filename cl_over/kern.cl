

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




void			mat_reduce_2(__const int len, __local float* dA, __local float* prods, __global float* dC)
{

	int		gid = get_global_id(0);
	int		tnum = get_local_id(0);
	int		wgNum = get_group_id(0);
	int		numItems = get_local_size(0);
	float	elem;
	float	accu = 0;

	while (gid < len)
	{
		elem = dA[gid];
		accu += elem;
		gid += get_global_size(0);
	}
	prods[tnum] = accu;
	barrier(CLK_LOCAL_MEM_FENCE);
	for (int offset = numItems / 2; offset > 0; offset /= 2)
	{
		if (tnum < offset)
		{
			prods[tnum] += prods[tnum + offset];
		}
		barrier(CLK_LOCAL_MEM_FENCE);
	}
	if (tnum == 0)
		dC[wgNum] = prods[0];
}

void			mat_reduce_1(__const int len, __global float* dA, __global float* dB, __local float* prods, __global float* dC)
{

	int		gid = get_global_id(0);
	int		tnum = get_local_id(0);
	int		wgNum = get_group_id(0);
	int		numItems = get_local_size(0);
	float	elem;
	float	accu = 0;

	while (gid < len)
	{
		elem = dA[gid] * dB[gid];
		accu += elem;
		gid += get_global_size(0);
	}
	prods[tnum] = accu;
	barrier(CLK_LOCAL_MEM_FENCE);
	for (int offset = numItems / 2; offset > 0; offset /= 2)
	{
		if (tnum < offset)
		{
			prods[tnum] += prods[tnum + offset];
		}
		barrier(CLK_LOCAL_MEM_FENCE);
	}
	if (tnum == 0)
		dC[wgNum] = prods[0];
}

__kernel void	reduce_part1(__const int len, __global float* dA, __global float* dB, __local float* prods, __global float* dC, __global float* dD)
{
	mat_reduce_1(len, dA, dB, prods, dC);
	mat_reduce_2(len, dC, prods, dD);
}


//////////////////////////////////


__kernel void	mat_reduce(__const int len, __global float* dA, __global float* dB, __local float* prods, __global float* dC)
{

	int		gid = get_global_id(0);
	int		tnum = get_local_id(0);
	int		wgNum = get_group_id(0);
	int		numItems = get_local_size(0);
	float	elem;
	float	accu = 0;

	while (gid < len)
	{
		elem = dA[gid] * dB[gid];
		accu += elem;
		gid += get_global_size(0);
	}
	prods[tnum] = accu;
	barrier(CLK_LOCAL_MEM_FENCE);
	for (int offset = numItems / 2; offset > 0; offset /= 2)
	{
		if (tnum < offset)
		{
			prods[tnum] += prods[tnum + offset];
		}
		barrier(CLK_LOCAL_MEM_FENCE);
	}
	if (tnum == 0)
		dC[wgNum] = prods[0];
}





////////////////////////////////////////////////////

__kernel void	mat_reduce2(__const int len, __global float* dA, __global float* dB, __local float* prods, __global float *dC)
{

	int		gid = get_global_id(0);
	int		tnum = get_local_id(0);
	int		wgNum = get_group_id(0);
	int		numItems = get_local_size(0);
	float	elem;
	float	accu = 0;

//	if (gid < len)
//		prods[tnum] = dA[gid] * dB[gid];
//	else
//		prods[tnum] = 0;


	while (gid < len)
	{
		elem = dA[gid] * dB[gid];
		accu += elem;
		gid += get_global_size(0);
	}
	prods[tnum] = accu;
	barrier(CLK_LOCAL_MEM_FENCE);

//	for (int offset = 1; offset < numItems; offset *= 2)
//	{
//		int	mask = 2 * offset - 1;
//		barrier(CLK_LOCAL_MEM_FENCE);
//		if ((tnum & mask) == 0)
//		{
//			prods[tnum] += prods[tnum + offset];
//		}
//	}

	for (int offset = numItems / 2; offset > 0; offset /= 2)
	{
//		barrier(CLK_LOCAL_MEM_FENCE);
		if (tnum < offset)
		{
			prods[tnum] += prods[tnum + offset];
		}
		barrier(CLK_LOCAL_MEM_FENCE);
	}
//	barrier(CLK_LOCAL_MEM_FENCE);
	if (tnum == 0)
		dC[wgNum] = prods[0];
}
