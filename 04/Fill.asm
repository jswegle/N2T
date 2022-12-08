// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Initialize limit and index, reset KBD
@kbd
M=0
@index
M=0
@8191 //don't want an off by one error here!
D=A
@limit
M=D //the number of words, total, which refer to the screen.

//check keyboard. If the value there is 0, we paintwhite. Else, we paintblack.
(Listen)
@KBD
D=M
@paintwhite
D;JEQ

@paintblack
0;JMP

//paint the current pixel white
(paintwhite)
@index
D=M
@SCREEN
A=A+D
M=0
@moveback
0;JMP

//advance our currentpixel backwards, unless we are already at the base address
(moveback)
@index
D=M
@Listen
D;JEQ
@index
M=M-1
@Listen
0;JMP

//paint the current pixel black
(paintblack)
@index
D=M
@SCREEN
A=A+D
M=-1
@moveforward
0;JMP

//Moves the current pixel forward, unless we are at the last word we can use
(moveforward)
@limit
D=M
@index
D=D-M
@Listen
D;JEQ
@index
M=M+1
@Listen
0;JMP
