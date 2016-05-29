#include "song1.h"

float genNotePos(int wavePosition, float frequency, char volume)
{
    return (((sinf(frequency * ((float) wavePosition / SAMPLE_RATE) * 2 * M_PI) + 1) * (1<<volume)));
}

float calcFrequency(float note)
{
    return (BASE_FREQUENCY * ( pow(2, (note / 12) ) ));
}

int main(int argc, char const *argv[])
{
    int wavepos = 0;
    short waveform = 0;
    int noteOffset = 0;
    Notes note = A;
    int octave = 0;

    while(1)
    {

        waveform = (unsigned short) genNotePos(wavepos, calcFrequency((float) noteOffset), 15);
        waveform = MERGE_WAVE(waveform, (unsigned short) genNotePos(wavepos, calcFrequency((float) noteOffset+12), 8));
        waveform = MERGE_WAVE(waveform, (unsigned short) genNotePos(wavepos, calcFrequency((float) noteOffset+24), 4));

        fwrite(&waveform, sizeof(short), sizeof(short), stdout);
        wavepos++;

        if( wavepos % (SAMPLE_RATE/4) == 0)
        {
            note++;
            note%=12;

            if( note == 0 )
            {
                octave++;

                // Sine wave doesn't work well above 6 octaves
                // We wrap the octaves around -6 and +6
                octave+=4;
                octave%=8;
                octave-=4;
            }

            noteOffset = GET_OFFSET(octave, note);
        }
        // printf("Note: %d | Frequency: %f\n", noteOffset, calcFrequency((float) noteOffset));
    }

    return 0;
}
