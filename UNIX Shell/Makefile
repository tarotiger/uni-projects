# Makefile for cowrie 

CC = dcc 

GCC = gcc -Wall -Werror -g

all: cowrie

cowrie: cowrie.c 
	$(CC) cowrie.c -o cowrie 

gcc_cowrie: cowrie.c 
	$(GCC) -o cowrie cowrie.c 

clean: 
	rm -f cowrie 
