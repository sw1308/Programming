-- Compile with:
-- ghc -o bin/PrimeGenerator -O -v src/PrimeGenerator.hs
-- from the Haskell/ directory

import System.Directory

readLines :: FilePath -> IO [String]
readLines = fmap lines . readFile

makeInteger :: [String] -> [Integer]
makeInteger = map read

makeStrings :: [Integer] -> [String]
makeStrings = map show

writeStrings :: [String] -> IO ()
writeStrings [] = appendFile "dat/primes.temp" "2\n2"
writeStrings [s] = appendFile "dat/primes.temp" s
writeStrings (s:ss) = do
	appendFile "dat/primes.temp" (s ++ "\n")
	writeStrings ss

permenantWrite permFile tempFile = do
	string <- readFile tempFile
	writeFile permFile string
	removeFile tempFile

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

getPrime :: Integer -> [Integer] -> [Integer]
getPrime 1 list = list
getPrime x (current:list) = do
	getPrime (x-1) (nextPrime (current+1) list)

primeList :: [Integer]
primeList = [2]

main = do
	putStrLn "How many more primes would you like?"
	n <- getLine
	fileList <- readLines "dat/primes.txt"
	--print $ makeInteger fileList
	let primeList = makeInteger fileList
	let prime = getPrime (read n::Integer) primeList
	putStrLn ("The " ++ n ++ "th next prime is: " ++ (show (last prime)))
	writeStrings (makeStrings prime)
	permenantWrite "dat/primes.txt" "dat/primes.temp"
