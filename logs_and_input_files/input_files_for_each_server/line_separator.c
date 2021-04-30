#include <stdio.h>
#include <stdlib.h>

int parser(int argc, char *argv[], int *lines, int *file_num)
{
	if(argc != 3)
	{
		fprintf(stderr, "Bad input args\n.");
		return 1;
	}
	char *fn = argv[1];	
	char *l = argv[2];	

	*lines = atoi(l);
	*file_num = atoi(fn);
	
	return 0;
}
int main(int argc, char *argv[])
{
	int lines = 0;
	int file_num = 0;
	int line_start = 0;
	char buff[2000] = {0};


	parser(argc, argv, &lines, &file_num);
	line_start = (lines * (file_num - 1)) + 2;
	fprintf(stderr,"file>%d lines>%d\n", file_num, lines);	
	//fprintf(stderr,"   line_start%d\n", line_start);	

	FILE *f = NULL;
	f = fopen("all_zbozi.cz_categories_url", "r");
	if (f == NULL)	
	{
		fprintf(stderr, "Cannot open file.\n");
		return 1;
	}	
	
	for(int i = 0; i <= line_start +1; i++)
	{
		fgets(buff, 2000, f);
	}
	
	fgets(buff, 2000, f);
	buff[0] = '\0';	

	for(int i = 0; i <= lines; i++)
	{
		if(i == 0)
		{
			fgets(buff, 2000, f);
			fprintf(stderr,"      %s",buff);
			continue;
		}
		fgets(buff, 2000, f);
		printf("%s",buff);
	}
		
	
	return 0;

}
