-- Compile with:
-- ghc -o ../C/bin/CPrimes -O -v src/CPrimes.hs
-- from the Haskell/ directory

module HaskellPrimeFunc where

import Foreign.C.Types

testNum :: Integer -> [Integer] -> Bool
testNum num [] = True
testNum num (x:xs)
	| (fromInteger x) > sqrt (fromInteger num) = True
	| mod num x == 0 = False
	| otherwise = testNum num xs

nextPrime :: CInt -> [CInt] -> CInt
nextPrime 1 [] = [2]
nextPrime count list
	| testNum count list == True = count
	| testNum count list == False = nextPrime (count + 1) list

foreign export ccall nextPrime :: CInt -> [CInt] -> CInt
