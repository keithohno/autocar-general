
all: prog.cpp
	g++ -g -Wall -o prog prog.cpp

clean: 
	$(RM) prog
