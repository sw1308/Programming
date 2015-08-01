#lang racket
(define (visit-doctor name) (begin (print (list 'hello name)) (print '(what seems to be the trouble?)) (doctor-driver-loop name)))

(define (doctor-driver-loop name) (begin (newline) (display '**) (let ((user-response (read))) (if (equal? user-response '(goodbye)) (begin (print (list 'goodbye name)) (print '(see you next week))) (begin (print (reply user-response)) (doctor-driver-loop name))))))

(define (reply user-response) (if (fifty-fifty)(append (qualifier) (change-person user-response)) (hedge)))

(define (fifty-fifty) (= (random 2) 0))

(define (qualifier) (pick-random '((you seem to think) (you feel that) (why do you believe) (why do you say) (what makes you feel that) (why do you think that))))

(define (hedge) (pick-random '((please go on) (many people have the same sorts of feelings) (many of my patients have told me the same thing) (please continue) (why do you think you feel this way?)(why do you think that?))))

(define (replace replacements x) (cond ((null? replacements) x) ((equal? (car (car replacements)) x) (cadr (car replacements))) (else (replace (cdr replacements) x))))

(define (many-replace replacements lst) (if (null? lst) nil (cons (replace replacements (car lst)) (many-replace replacements (cdr lst)))))

(define (change-person phrase) (many-replace '((you i) (are am) (your my) (i you) (me you) (am are) (my your)) phrase))

(define (pick-random lst) (list-ref lst (random (length lst))))
