// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// The program works by adding R0 to itself R1 times.
@R1
	// load R1 into D
    D = M

    // store R1 in i
    @i
    M = D

    // store R0 in product
    @product
    M = 0

// loop to add R0 to 'product' i times
(LOOP)
    @i
    D = M

    // if i == 0, jump to END
    @END
    D;JEQ

    @R0
    D = M

    // store R0 in D
    @product
    M = D + M

    // decrement i
    @i
    M = M - 1	

    // jump to LOOP
    @LOOP
    0;JMP

(END)
    // store product in D
    @product
    D = M
  
    // store D in R2
    @R2
    M = D

    // infinite loop
    @END
    0;JMP