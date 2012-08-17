
CC=gcc
CFLAGS=-c -Wall -I/usr/include/gc

all:		nominine makefile

nominine:	core.o utils.o main.o
		$(CC) main.o core.o utils.o -lgc -lm -o nominine

main.o:		core.o utils.h main.c utils.h
		$(CC) $(CFLAGS) main.c

utils.o:	core.o utils.h utils.c
		$(CC) $(CFLAGS) utils.c

core.o:		utils.h meta.py core.py
		python core.py
		$(CC) $(CFLAGS) core.c

clean:
		rm *.o
		rm core.c core.h
		rm *.pyc
		rm nominine


