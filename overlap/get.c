#include "test.h"
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>

void	print_tab(double **t, int l1, int l2)
{
	int		i, j;

	i = 0;
	while (i < l1)
	{
		j = 0;
		while (j < l2)
		{
			printf("%1.10f ", t[i][j]);
			j++;
		}
		printf("\n");
		i++;
	}
}

void	print_re(double ***t)
{
	int		i, j, k;

	i = 0;
	while (i < X)
	{
		j = 0;
		while (j < Y)
		{
			k = 0;
			while (k < Z)
			{
				printf("%1.10f ", t[i][j][k]);
				k++;
			}
			printf("\n");
			j++;
		}
		printf("\n\n");
		i++;
	}
}

void	init(double ***t, int l1, int l2)
{
	int		i = 0;

	*t = (double**)malloc(sizeof(**t) * l1);
	while (i < l1)
	{
		(*t)[i] = (double*)malloc(sizeof(***t) * l2);
		i++;
	}
}

void	fill_row(double ***t, char *s, int r)
{
	char	*tok;
	char	del[] = " ";
	int		i = 0;
	double	n;

	tok = strtok(s, del);
	while (tok)
	{
		n = atof(tok);
		(*t)[r][i] = n;
		i++;
		tok = strtok(NULL, del);
	}
}

void	del_tab(double ***t)
{
	int		i = 0;

	while (i < X)
	{
		free((*t)[i]);
		i++;
	}
	free(*t);
}

double	***reshape(double **t)
{
	double	***new;
	int		i, j, k;

	new = (double***)malloc(sizeof(*new) * X);
	i = 0;
	while (i < X)
	{
		new[i] = (double**)malloc(sizeof(**new) * Y);
		j = 0;
		while (j < Y)
		{
			new[i][j] = (double*)malloc(sizeof(***new) * Z);
			k = 0;
			while (k < Z)
			{
				new[i][j][k] = t[i][j * k];
				k++;
			}
			j++;
		}
		i++;
	}
	return (new);
}
