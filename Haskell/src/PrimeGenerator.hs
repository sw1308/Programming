primeList :: [Integer]
primeList = [2]

test :: Integer -> [Integer] -> Bool
test num [] = True
test num [x:xs]
	| x > sqrt num = True
	| mod num x == 0 = False
	| otherwise = test num xs

nextPrime :: [Integer] -> Integer
nextPrime 1 [] = 2
nextPrime count list
	| test count list == True = count
	| test count list == False = nextPrime count + 1 list

main :: [Integer] -> [Integer]
main = primeList ++ [nextPrime last primeList + 1 primeList]
