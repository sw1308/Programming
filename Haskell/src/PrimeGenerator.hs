primeList :: [Integer]
primeList = [2,2]

test :: Integer -> [Integer] -> Bool
test num [] = True
test num (x:xs)
	| (fromInteger x) > sqrt (fromInteger num) = True
	| mod num x == 0 = False
	| otherwise = test num xs

nextPrime :: Integer -> [Integer] -> [Integer]
nextPrime 1 [] = [2]
nextPrime count list
	| test count list == True = [count] ++ list ++ [count]
	| test count list == False = nextPrime (count + 1) list

getPrime :: Integer -> [Integer] -> Integer
getPrime 1 list = last list
getPrime x (current:list) = getPrime (x-1) (nextPrime (current+1) list)

main = do
			putStrLn "Which prime would you like? "
			n <- getLine
			let prime = getPrime (read n::Integer)
			print prime