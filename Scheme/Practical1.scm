#lang racket
(define noun-list (list 'dog 'cat 'student 'professor 'book 'computer))
(define verb-list (list 'ran 'ate 'slept 'drank 'exploded 'decomposed))
(define adjective-list (list 'red 'slow 'dead 'pungent 'over-paid 'drunk))
(define adverb-list (list 'quickly 'slowly 'wickedly 'majestically))
(define (sentence)
	(append (noun-phrase) (verb-phrase))
	)
(define (pick-random lst)
	(list-ref lst (random (length lst)))
	)
(define (a-noun)
	(list (pick-random noun-list))
	)
(define (a-verb)
	(list (pick-random verb-list))
	)
(define (an-adjective)
	(list (pick-random adjective-list))
	)
(define (an-adverb)
	(list (pick-random adverb-list))
	)
(define (either a b)
	(if (=(random 2) 0) a b)
	)
(define (noun-phrase)
	(append (list 'the) (either (a-noun) (adjective-noun)))
	)
(define (verb-phrase)
	(either (a-verb) (verb-adverb))
	)
(define (adjective-noun)
	(append (an-adjective) (a-noun))
	)
(define (verb-adverb)
	(append (a-verb) (an-adverb))
	)
