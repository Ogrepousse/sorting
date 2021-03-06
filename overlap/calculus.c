#include "test.h"
#include <stdlib.h>
#include <string.h>

void	fill_buf(double ***buf, FILE *fd)
{
	int		ret;
	char	*s;
	size_t	n = 0;
	int		i = 0;

	s = NULL;
	while ((ret = getline(&s, &n, fd)) > 0)
	{
		fill_row(buf, s, i);
		i++;
		free(s);
		s = NULL;
	}
	free(s);
	s = NULL;
}

double	***overlap_init(void)
{
	double	***overlap;
	int		i, j;

	overlap = (double***)malloc(sizeof(double**) * Z * 2);
	i = 0;
	while (i < Z * 2)
	{
		overlap[i] = (double**)malloc(sizeof(double*) * Z * 2);
		j = 0;
		while (j < Z * 2)
		{
			overlap[i][j] = (double*)malloc(sizeof(double*) * (Y * 2 - 1));
			j++;
		}
		i++;
	}
	return (overlap);
}

double	**tempon_init(void)
{
	double	**t;
	int		i;

	t = (double**)malloc(sizeof(double*) * X);
	i = 0;
	while (i < X)
	{
		t[i] = (double*)malloc(sizeof(double) * Y);
		i++;
	}
	return (t);
}

void	get_tempon1(double ***at1, double ***temp)
{

}

void	overlap(double ****tab)
{
	double	***temp, ***temp2, ***comp, ***comp2;
	double	***overlap;
	int		i, j, k;
	double	**t1, **t2;

	temp = tab[0];
	temp2 = tab[1];
	comp = tab[2];
	comp2 = tab[3];
	overlap = overlap_init();
	t1 = tempon_init();
	t2 = tempon_init();
	memset(t1, 0, sizeof(**t1) * X * Y);
	memset(t2, 0, sizeof(**t2) * X * Y);
	i = 0;
	while (i < Z * 2)
	{
		
	//	printf("%d\n", j);
	//	if (j < Z)
i++;
	}
}

void	ouverture(void)
{
	double	**buf;
	char	*list[] = {"../temp", "../temp2", "../comp", "../comp2", NULL};
//	char	*list[] = {"recup", "recup", "recup", "recup", NULL};
	int		i;
	FILE	*fd;
	double	****tab;

	tab = (double****)malloc(sizeof(double***) * 4);
	i = 0;
	while (list[i])
	{
		fd = fopen(list[i], "r");
		init(&buf, X, Y * Z);
		fill_buf(&buf, fd);
		tab[i] = reshape(buf);
		fclose(fd);
	//	print_re(tab[i]);
		printf("\n");
		del_tab(&buf);
		i++;
	}
}
