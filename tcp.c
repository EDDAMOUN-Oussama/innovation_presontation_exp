#include <stdio.h>
#include <stdlib.h>

# define N 9

char *cite[N] = { "Tétouan", "Tanger", "Chefchaouen", "Larache", "Ouazzane", "Kenitra", "Rabat", "FES", "OUJDA" };

void ft_init_dest(int dest[N][N])
{
    for (int i = 0; i < 9; i++)
    {
        for (int j = 0; j < 9; j++)
            if (i == j)
                dest[i][j] = -1;
            else
                dest[i][j] = -1;
    }
    //from Tétouan to:
    dest[0][1] = 61; //Tanger
    dest[0][2] = 63; //Chefchaouen
    dest[0][3] = 144; // Larache
    dest[0][4] = 128; // Ouazzane

    //from Tanger to:
    dest[1][3] = 64;

    // from Chefchaouen to:
    dest[2][4] = 70; // Chefchaouen
    dest[2][5] = 168; // Kenitra

    // from Larache to:
    dest[3][4] = 82; // Ouazzane
    dest[3][5] = 122; // Kenitra
    dest[3][7] = 225; // FES

    // from Ouazzane to:
    dest[4][5] = 130; // Kenitra
    dest[4][7] = 146; // FES

    // from Kenitra to:
    dest[5][6] = 39; // Rabat
    dest[5][7] = 148; // FES
    dest[5][8] = 523; // OUJDA

    // from Rabat to:
    dest[6][7] = 201; // FES

    // from FES to:
    dest[7][8] = 331; // OUJDA

    // the destence from Tétouan to OUJDA egual the destence from OUJDA to Tétouan so: dest[i][j] = dest[j][i];

}

int get_next_city(int corent_city, int dest[N][N], int *new_dest)
{
    int last_dest = -1;
    int best_city = -1;
    for (int i = 0; i < N; i++)
    {
        if (last_dest <= 0 || (dest[corent_city][i] < last_dest && dest[corent_city][i] > 0) || (dest[i][corent_city] < last_dest && dest[i][corent_city] > 0))
        {
            best_city = i;
            last_dest = dest[corent_city][i] * dest[i][corent_city] * -1;
        }
    }
    *new_dest = last_dest;
    dest[corent_city][best_city] = -1;
    dest[best_city][corent_city] = -1;
    return (best_city);
}


void ft_calcul_total_dest(int corent_city, int dest[N][N])
{
    int best_city;
    int new_dest = 0;
    int total_dest = 0;
    printf("We start from : (%s):\n", cite[corent_city]);
    printf("%s", cite[corent_city]);

    best_city = corent_city;
    while (best_city != -1 && new_dest != -1)
    {
        best_city = get_next_city(corent_city, dest, &new_dest);
        if (best_city != -1 && new_dest != -1)
        {
            printf("==(%d)==>%s", new_dest, cite[best_city]);
            total_dest += new_dest;
        }
        corent_city = best_city;
    }
    printf("\nthe total dest: %d\n", total_dest);
}

int main(int ac, char **av)
{
    int dest[N][N];

    if (ac != 2)
        return (1);
    ft_init_dest(dest);
    ft_calcul_total_dest(atoi(av[1]), dest);
    return (0);
}