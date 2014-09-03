#ifndef TEST_H
# define TEST_H

# include <stdio.h>

# define X 764
# define Y 764
# define Z 257

void	print_tab(double **t, int l1, int l2);
void	print_re(double ***t);
void	init(double ***t, int l1, int l2);
void	fill_row(double ***t, char *s, int r);
void	del_tab(double ***t);
double	***reshape(double **t);
void	ouverture(void);
void	fill_buf(double ***buf, FILE *fd);

#endif
