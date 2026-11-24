(MAIN)
    @KBD
    D=M
    @WHITE
    D;JEQ

    @0
    D=A-1
    @color
    M=D
    @START
    0;JMP

(WHITE)
    @color
    M=0

(START)
    @17952       // SCREEN (16384) + 32 * 49
    D=A
    @addr
    M=D

    @20          // 20 rows tall
    D=A
    @count
    M=D

(LOOP)
    @count
    D=M
    @MAIN
    D;JEQ

    @color
    D=M

    @addr
    A=M
    M=D          // first 16 pixels

    @addr
    A=M+1
    M=D          // next 16 pixels (total 32 pixels wide)

    @32
    D=A
    @addr
    M=D+M        // next row

    @count
    M=M-1

    @LOOP
    0;JMP