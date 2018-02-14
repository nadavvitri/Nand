// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


	@SCREEN
	D=A
	@addr
	M=D  // addr = 16384 (Screen's base address)
	
	@i  
	M=0  // set counter to 0
	
(BLACK)
	@KBD  // check if keyboard pressed
	D=M
	@WHITE  
	D;JEQ  // if no key pressed jump and white the screen
	
	@i
	D=M
	@8191  // number of cells in Screem memory map
	D=A-D
	@BLACK 
	D;JLT  // if we colored all the pixels in the screen
	
	@addr
	A=M
	M=-1  // RAM[addr]=1111111111111111
	@addr
	M=M+1 // addr = addr + 1 (move to the next pixel)
	@i
	M=M+1  // i++
	@BLACK
	0;JMP  // goto BLACK
	
(WHITE)
	@KBD  // check if keyboard pressed
	D=M
	@BLACK
	D;JNE  // if key pressed jump and black the screen
	
	@i
	D=M
	@WHITE
	D;JLT // if we colored all the pixels in the screen
	
	@addr
	A=M
	M=0  // RAM[addr]=0000000000000000
	@addr
	M=M-1  // addr = addr + 1 (move to the previous pixel)
	@i
	M=M-1  // i--
	@WHITE
	0;JMP  // goto WHITE
	