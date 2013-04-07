
CC=gcc
CFLAGS=-c -g -Wall -I/usr/include/gc

all:		nominine
		python test.py

nominine:	core.o utils.o main.o parser.o
		$(CC) main.o core.o utils.o parser.o -lgc -lm -o nominine

main.o:		core.o utils.h parser.h main.c utils.h
		$(CC) $(CFLAGS) main.c

parser.o:	core.o utils.h parser.h parser.c
		$(CC) $(CFLAGS) parser.c

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


