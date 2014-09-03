#include "test.h"
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>

int		main(void)
{
	double	**buf;
	FILE	*fd, *fd2;
	int		i, j;

//	ouverture();
	fd = fopen("../omeg3", "r");
	init(&buf, X, Y * Z);
	fill_buf(&buf, fd);
	fclose(fd);
	fd2 = fopen("recup", "wb");
	i = 0;
	while (i < X)
	{
		j = 0;
		while (j < Y * Z)
		{
			fwrite(buf[i] + j, sizeof(double), 1, fd2);
			j++;
		}
		i++;
	}
	printf("fini\n");
	return (0);
}
