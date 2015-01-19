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
data Op = Add | Mul
data E = Vr V | Vl N | Ap E Op E

instance Show E where
	show (Vr v) = v
	show (Vl n) = show n
	show (Ap e0 Add e1) = show e0 ++ " + " ++ show e1
	show (Ap e0 Mul e1) = show e0 ++ " * " ++ show e1

testExp :: E
testExp = (Ap (Vr "x") Mul (Ap (Vr "y") Add (Vr "z")))

evaluate :: Assoc Int -> E -> Int
evaluate a (Vr v) = fetch v a
evaluate a (Vl n) = n
evaluate a (Ap x Add y) = (evaluate a x) + (evaluate a y)
evaluate a (Ap x Mul y) = (evaluate a x) * (evaluate a y)

simplify :: E -> E
simplify (Ap e Mul (Vl 0)) = Vl 0
simplify (Ap e Mul (Vl 1)) = simplify e
simplify (Ap (Vl 0) Mul e) = Vl 0
simplify (Ap (Vl 1) Mul e) = simplify e
simplify (Ap e Add (Vl 0)) = simplify e
simplify (Ap (Vl 0) Add e) = simplify e
simplify (Ap e0 Mul e1) = Ap (simplify e0) Mul (simplify e1)
simplify (Ap e0 Add e1) = Ap (simplify e0) Add (simplify e1)
simplify e = e

type Assoc a = [(String, a)]

test :: Assoc Int
test = [("x", 4), ("y", 2), ("z", 0)]

names :: Assoc a -> [String]
names [] = []
names (x:xs) = [fst x] ++ names xs

inAssoc :: String -> Assoc a -> Bool
inAssoc s a = elem s (names a)

fetch :: String -> Assoc a -> a
fetch s [] = error("Could not find value associated with " ++ s)
fetch s ((t,n):xs)
	| s == t = n
	| otherwise = fetch s xs

update :: String -> a -> Assoc a -> Assoc a
update s m [] = [(s, m)]
update s m ((t, n):xs)
	| s == t = [(t, m)] ++ xs
	| otherwise = [(t, n)] ++ update s m xs

tailT :: [a] -> Maybe [a]
tailT [] = Nothing
tailT xs = Just (tail xs)

lastT :: [a] -> Maybe a
lastT [] = Nothing
lastT xs = Just (last xs)

total :: (a -> b) -> (a -> Maybe b)
total  = 
