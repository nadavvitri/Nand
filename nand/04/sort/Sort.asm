// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/sort/Sort.asm

// The program should sort the array starting at the address in R14 with length specified in R15.

	@i
	M=0  	// init i == 0
	
(OUTSIDE LOOP)
	@i
	D=M
	@R15  // length of array
	D=D-M
	@i
	M=M+1 // i++
	@j
	M=0     // init j == 0
	@END
	D;JEQ   // if (i == R15) goto END
	
(INSIDE LOOP)
	@j
	D=M+1
	@R15  // length of array
	D=D-M
	@OUTSIDE LOOP
	D;JEQ   // if (j == R15) goto OUTSIDE LOOP
	
	@R14
	D=M
	@j
	A=D+M  // A = base addres(address in R14) + j
	D=M
	A=A+1
	D=D-M
	@j
	M=M+1  // j++
	@INSIDE LOOP
	D;JGE  // if (RAM[x] - RAM[x-1]) >= 0 goto INSIDE LOOP
	
	// swaping RAM[x] with RAM[x-1]
	@R14
	D=M
	@j
	D=D+M  // D = base addres(address in R14) + j
	@address
	M=D-1    // address contain the current address
	A=M
	D=M    // D = RAM[x-1]
	@temp
	M=D    // temp == D
	
	@address
	A=M+1    
	D=M    // D = RAM[x]
	A=A-1  
	M=D    // RAM[x-1] = RAM[x]
	
	@temp
	D=M
	@address
	A=M+1
	M=D    // RAM[x] = temp
	@INSIDE LOOP
	0;JMP   // repeat
	

(END)
