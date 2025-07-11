# PySource engine

PySource is an MIT open source game engine developed by As an 11 year old coder male like i know PHP  DART GML Python X86 assembly vbscript fortran java javascript C++/C C# ruby RUST R and LUA scratch (scratch and adacraft) Who loves old tech and anime girl wearing a towel and also a GTA minecraft portal and RollerCoaster Tycoon fan boy who does know wiring

Yes a 7th grader made this engine 

You can see his itch.io page at https://saturn-computing-topic.itch.io/ 
# Games made with it
not much the developer uses this game engine to make his proprietary game YandereSourceEngine.exe and he btoh coded the game and the engine in python and assembly language

# Installation

To use it install all the files and remove the 2 files README.md and LICENSE

After that install NASM from https://www.nasm.us/pub/nasm/releasebuilds/?C=M;O=D and use GoLink to convert the .asm into a .obj
If aiming as .so library then use gcc

command to convert .asm to .obj
if for windows
nasm -f win64 SourcePLayer_win.asm - SourcePLayer_win.obj
If for linux
If aiming as Linux then do
nasm -f elf64 SourcePlayer_Linux.asm -o SourcePlayer_Linux.obj

after that use GoLink
GoLink.exe /dll /entry _DllMainCRTStartup SourcePLayer_win.obj _start


why not for linux as .so
IDK how to use gcc



