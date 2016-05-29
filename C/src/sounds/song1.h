#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <unistd.h>

#define SAMPLE_RATE 48000
#define BASE_FREQUENCY 440

#define GET_OFFSET(OCTAVE, NOTE) (OCTAVE * 12) + NOTE
#define MERGE_WAVE(WAVEPOS, NEWPOS) ((WAVEPOS - 32768) + (NEWPOS - 32768)) + 32768

float genNotePos(int wavePosition, float frequency, char volume);
float calcFrequency(float note);


typedef enum
{
    A=  0,
    As= 1,
    B=  2,
    C=  3,
    Cs= 4,
    D=  5,
    Ds= 6,
    E=  7,
    F=  8,
    Fs= 9,
    G=  10,
    Gs= 11
}Notes;
