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

// Start
(START)
    // Screen address
    @SCREEN
    D = A
    @addr
    M = D

    // Number of pixels
    @8192
    D = A
    @pixels
    M = D

// Get user input
(CHECK)
    // Check if there are any pixels left to paint
    @pixels
    D = M
    // If no pixels left, go back to start
    @START
    D;JEQ

    // Check if a key is pressed at RAM[24576]
    @KBD
    D = M

    // If key is pressed, go to BLACKSC
    @BLACKSC
    D;JNE

    // If no key is pressed, go to BLANKSC
    @BLANKSC
    D;JEQ

    (BLACKSC)	
    // Set the pixel at addr to -1
	@addr
	A = M
	M = -1

    // Increment the pixel counter
	@addr
	M = M + 1

    // Decrement the pixel counter
	@pixels
	M = M - 1
	
    // Go back to CHECK
	@CHECK
	0;JMP

    (BLANKSC)	
    // Set the pixel at addr to 0
	@addr
	A = M
	M = 0

    // Increment the pixel counter
	@addr
	M = M + 1

    // Decrement the pixel counter
	@pixels
	M = M - 1
	
    // Go back to CHECK
	@CHECK
	0;JMP