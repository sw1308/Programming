d2n :: Char -> Int
d2n '0' = 0
d2n '1' = 1
d2n '2' = 2
d2n '3' = 3
d2n '4' = 4
d2n '5' = 5
d2n '6' = 6
d2n '7' = 7
d2n '8' = 8
d2n '9' = 9
d2n _ = error("Must input a character of a number (0,1,2,3,4,5,6,7,8,9)")

s2n :: String -> Int
s2n = (foldl1 f).(map d2n)
	where f x y = (10*x) + y

whitespace :: Char -> Bool
whitespace c = elem c [' ','\n','\r','\t']

dropWhitespace :: String -> String
dropWhitespace = dropWhile whitespace

type V = String
type N = Int
data E = Var V | Val N | Plus E E | Mult E E

instance Show E where
	show (Var v) = v
	show (Val n) = show n
	show (Plus e0 e1) = show e0 ++ " + " ++ show e1
	show (Mult e0 e1) = show e0 ++ " * " ++ show e1

evaluate :: E -> Int
evaluate (Var v) = error("error on input Var " ++ show v)
evaluate (Val n) = n
evaluate (Plus x y) = (evaluate x) + (evaluate y)
evaluate (Mult x y) = (evaluate x) * (evaluate y)

simplify :: E -> E
simplify (Mult e (Val 0)) = Val 0
simplify (Mult e (Val 1)) = simplify e
simplify (Mult (Val 0) e) = Val 0
simplify (Mult (Val 1) e) = simplify e
simplify (Plus e (Val 0)) = simplify e
simplify (Plus (Val 0) e) = simplify e
simplify (Mult e0 e1) = Mult (simplify e0) (simplify e1)
simplify (Plus e0 e1) = Plus (simplify e0) (simplify e1)
simplify e = e

type Assoc a = [(String, a)]

test :: Assoc Int
test = [("x", 4), ("y", 2), ("z", 0)]

names :: Assoc a -> [String]
names [] = []
names (x:xs) = [fst x] ++ names xs
