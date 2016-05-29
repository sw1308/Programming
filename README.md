Programming Documentation
=========================

#Contents
[TOC]

#Introduction

This is a repository for all of my personal projects and programming, it includes a brief overview of each of the projects and an in-depth description of what they do and how they work.

#Ada

##src
###GravitySimulator
This will be the backend for the implementation of [PhysicsPrototype](#PhysicsPrototype) in Ada

###ObjectOrientedPractice
This is my initial attempt at using the object oriented paradigm in Ada, it's a bit more complicated than in Java or C++ so I haven't got very far with it yet.

###physicsBackend
This was my initial attempt at making the Ada version of [PhysicsPrototype](#PhysicsPrototype), it did not go very well.

###Makefile
Takes all ada source files it can see in the current directory and builds them separately, outputting them into the bin/ directory.

###func.adb
Example of how to make and use functions in Ada.

###hello.adb
Simple hello world program.

###primes.adb
Single-threaded prime generator written in Ada, goes up to 1,000,000,000 and then stops.

#Bash

##soundTest.sh
This is a project I was trying to write to output a wave representation of whatever you piped into the function.

```bash
while read -rs -n 1 char
do
    printf "%$(ord $char)s\n" "|"
done < "${1:-/dev/stdin}"
```
The loop above looks fairly simple, and it sort of is. It takes a string, file, or whatever, and parses it line-by-line.
Then for each character it will print out `|` after the number of spaces that corresponds to the ascii number of the character that has been read in.

#C

##dat
Data folder, just a store for any file information that's accessed by the C programs.

###gengine.frag
Fragment shader for my attempt at using OpenGL in raw C.

###gengine.vert
Vertex shader for my attempt at using OpenGL in raw C.

##src

###chess
This is the beginning of the chess program I wanted to write, it was meant to be low level and very space/processor time efficient.

Eventually it will have an API that can be used to interact with the game board and then I would begin writing some game clients for it.

###concurrencyGateTest
This is an attempt at writing a simple concurrency gate in C.
I needed it for my implementation of threadedPrimes so that I could controll the threads I had running in order to pause them while I populated the main primes list.

###sounds
This is an experimental project to mathematically define a song, not got very far yet but I've managed to make some basic utility macros for creating a sine wave from a note and merging two sound waves.

###threadedPrimes
This was intended to be a program that finds all prime numbers using multi-threading. Unfortunately I'm having some trouble figuring out how to make a concurrency gate work, there isn't really one in the standard C library so I tried [making my own](#concurrencyGateTest "Concurrency Gate Implementation").
Rather frustratingly, although it looks like it works fine on it's own it doesn't really seem to work properly with threadedPrimes.

###SYAC1.c
One of the SYAC practicals, didn't get very far. I think it was intended to be a rudimentary shell but it was stupid.

###ackermann.c
A C implementation of Ackermann's function, in theory it would take until the heat death of the universe to complete but it causes a segmentation fault after a couple of minutes so I think it breaks the stack it's running on or something.

###fileTest.c
This was a test program to read in from a hard-coded file path and populate a character array with it's contents.

###haskellPrimeGenerator.c
This was my first attempt at a multi-language program. It would use Haskell to generate a list of primes, and interact with a C program to output them into a file and interact with the user.

###hello_world.c
What programming repo would be complete without hello world. (Yeah this probably shouldn't be here either)

###matrixOps.c
This was an earlier implementation of [math_3d.h](#math_3d.h) that didn't really use pre-defined structs, you hand it some arrays and it does stuff with them.

###prime_generator.c
This is the single-threaded prime generator. It doesn't really work using RAM, instead it stores everything it's done so far in a file and picks up where it left off when you start it next.
That means it's a little slower in-between test cases but you also can't really lose more than a couple of seconds of work in the event of a power failure or whatever.

###sudokuSolver.c
This is the beginning of a low-overhead and low-RAM implementation of the java sudoku solver. You give it an incomplete sudoku and it will solve it for you (provided the puzzle is possible).

#C++

##dat
Simple data folder for the C++ programs, this one is sorted on a per-program basis.
###GLTutorial
Folder for the GLTutorial project.

####shader.frag
This is the fragment shader for GLTutorial, currently it just sets the colour to whatever you give it (the colour input is worked out based on the fragment's position earlier in the pipeline).

####shader.vert
This is the vertex shader for GLTutorial, it handles 3D world projection and uses that position to evenly blend the colours for each fragment.

##src

###OpenGL

####GLTutorial.cpp
The main (and most successful) attempt at learning OpenGL so far.
It renders a spinning pyramid on a black background where the colour of each face is dependant on where the pixels are in world space.

####GLTutorial.h
Header file for GLTutorial.cpp

####Makefile
This Makefile gathers all cpp files and bundles them into one list before using g++ to compile and link them all in one binary, which then gets output into the bin/ directory of the C++ folder.

####math_3d.cpp
This is the implementation for a lot of the 3D maths that is needed in OpenGL, it contains the implementations for vectors, 3x3 and 4x4 matrices, and contains some functions that perform operations on those structures.

####math_3d.h
Header file for math_3d.cpp

####pipeline.cpp
This file contains some useful functions for setting up the transformation matrices that need to be fed into the GPU in order to render the world space properly.

####pipeline.h
Header file for pipeline.cpp

####types.h
This contains some generic typedefs for uint, uchar, and ushort.

####utils.cpp
Utility file for things like reading information from a file, printing error messages, and getting current time in milliseconds.

####utils.h
Header for utils.cpp

#HTML

##ripple.html
This is just a test page for some simple animations based on Google's Material Design philosophy.
I haven't done much more than just make it work so far.

#Haskell

##dat

###primes.txt
Storage for all the primes that PrimeGenerator.hs finds.

##src

###CPrimes.hs

###FileOperations.hs
Simple implemention for reading from and writing to files.
It's primary use is to read in all of the information in primes.txt and return them in a list of numbers to the user.

###Makefile
Compiles each individual *.hs file it finds in the current directory and outputs it into it's own folder in the bin/ directory.

###Practical1.hs
Boring Haskell practical is boring.

###Practical2.hs
See [above](#Practical1.hs).

###PrimeGenerator.hs
This is your standard prime generation algorithm written in Haskell.
It isn't quite as robust as the [C implementation](#prime_generator.c) because it only saves to file at the end of it's generation phase.
It also only runs up to whatever number you give it at the start so that you actually get the chance to see the results (and because I couldn't figure out a way to make it run forever while also writing to file).

#Java

##dat


##src
###PhysicsSystem
This is my attempt at building a Java library for allowing you to seamlessly create any unit and convert between them.
For example you could say that you had an object of mass m(kg) and acceleration a(m/s^2) and multiplying them together would give you the force, but this library would also resolve the units.
It would also auto-convert units, so you could add 10lbs to 50kg and multiply by 20 troy ounces, and it would resolve all of the conversions automatically, giving you the correct result in kg.

###sudoku_solver.java
This is an implementation of an algorithm that solves an arbitratily large sudoku puzzle, unfortunately this is not quite as efficient as I would like.
I'm keeping it around so that I have a basis for the algorithm to implement a C version when I have time.

#Python
##PhysicsPrototype
This is a prototype for a project I'd like to some-day implement in C and Ada. It's a rudimentary 2D simulation for n-body gravitational interactions.

##XMLPerm.py
This was an idea for quickly being able to tell if two XML files were permutations of one another, it didn't work out because it gets extremely complicated as you traverse down each tree.
It would probably need slight re-write so that it does a depth-first search and marks each complete branch before moving on instead of the breadth-first approach it currently uses.

##arrayPerm.py
Checks if two arrays are permutations of each other, this is used by XMLPerm.py as part of it's checking process.

#Conf
##Overview
This is actually just a backup for my basic /home folder in a fresh linux install. It has some simple functions, aliases, and configs for i3wm.

##.i3

###config
Just a configuration file for /etc/i3.

It sets my standard keybindings:
 - mod = win-key
 - altArrows = ijkl (instead of jkl;)

It also sets borderless windows, sets the bar colour to #212121 and sets a background image using feh

##i3

###config
Standard file for i3 (with the same keybindings as above).

###config.keycodes
This likely isn't necessary, it's the keybindings for i3

##.Xresources
Sets the colour scheme for xterm, it's useful for making sure that all of my terminal emulators (based on xterm) have the same colours without me having to re-write it every time.

##.bash_aliases
Sets up some simple aliases that I use a lot:

 - lanssh - ssh into my server (only works over LAN)
 - autoupdate - uses apt-get to update, installe all updates, and autoremove redundant packages

##.bash_functions
Exports current directory to my PATH variable for convenience.
Some useful functions that are a little to complex for aliases:

 - cls - Prints out the debian logo to the top of the screen (after formatting it based on the size of the terminal window)

##.bashrc
The standard debian bashrc file, it also:

 - Sets up colour prompt
 - Assigns some standard aliases like la, ll, vdir etc.
 - Adds /sbin to PATH (yeah I know it's mostly sudo stuff but tab completion is handy even if you can't run the program)
 - Starts thefuck (for better completion estimation when I need it)

