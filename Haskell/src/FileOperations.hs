import System.Directory

readLines :: FilePath -> IO [String]
readLines = fmap lines . readFile

makeInteger :: [String] -> [Int]
makeInteger = map read

makeStrings :: [Integer] -> [String]
makeStrings = map show

writeStrings :: [String] -> IO ()
writeStrings [] = do writeFile " " "dat/primes.temp"
writeStrings (s:ss) = do
	writeFile "dat/primes.temp" (s ++ " ")
	writeStrings ss

permenantWrite permFile tempFile = do
	closeFile permFile
	string <- readFile tempFile
	putStrLn ("Writing to file: " ++ string)
	writeFile permFile (string)
	removeFile tempFile

main = do
	content <- readLines "dat/primes.txt"
	writeStrings (makeStrings [1, 2, 3, 4, 5, 6, 7, 8, 9])
	permenantWrite "dat/primes.txt" "dat/primes.temp"
	return (content)