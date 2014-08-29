#ifndef TEST_H
# define TEST_H

# include "libft/libft.h"
# include <stdio.h>

# define X 252
# define Y 129
# define Z 382

void	print_tab(double **t, int l1, int l2);
void	print_re(double ***t);
void	init(double ***t, int l1, int l2);
void	fill_row(double ***t, char *s, int r);
void	del_tab(double ***t);
double	***reshape(double **t);
void	ouverture(void);

#endif
