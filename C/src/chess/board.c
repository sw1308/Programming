#include "chess.h"

short board[8][8] = {
	{BLACK_ROOK,	BLACK_KNIGHT,	BLACK_BISHOP,	BLACK_KING,		BLACK_QUEEN,	BLACK_BISHOP,	BLACK_KNIGHT,	BLACK_ROOK},
	{BLACK_PAWN,	BLACK_PAWN,		BLACK_PAWN,		BLACK_PAWN,		BLACK_PAWN,		BLACK_PAWN,		BLACK_PAWN,		BLACK_PAWN},
	{0,				0,				0,				0,				0,				0,				0,				0},
	{0,				0,				0,				0,				0,				0,				0,				0},
	{0,				0,				0,				0,				0,				0,				0,				0},
	{0,				0,				0,				0,				0,				0,				0,				0},
	{WHITE_PAWN,	WHITE_PAWN,		WHITE_PAWN,		WHITE_PAWN,		WHITE_PAWN,		WHITE_PAWN,		WHITE_PAWN,		WHITE_PAWN},
	{WHITE_ROOK,	WHITE_KNIGHT,	WHITE_BISHOP,	WHITE_KING,		WHITE_QUEEN,	WHITE_BISHOP,	WHITE_KNIGHT,	WHITE_ROOK}
}
