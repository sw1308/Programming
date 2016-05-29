double :: Integer -> Integer
double x = x * 2

isEven :: Int -> Bool
isEven x = x `mod` 2 == 0

doubleSecondNumber :: [Integer] -> [Integer]
doubleSecondNumber [] = []
doubleSecondNumber [x] = [x]
doubleSecondNumber (x:y:xs)
    | isEven (length xs) = double x : y : doubleSecondNumber xs
    | otherwise          = x : double y : doubleSecondNumber xs

getDigits :: Integer -> [Integer]
getDigits 0 = []
getDigits x = getDigits (x `div` 10) ++ [x `mod` 10]

splitToList :: Integer -> [Integer]
splitToList 0 = [0]
splitToList x = getDigits x

sumDigits :: Integer -> Integer
sumDigits x= foldl1 (+) xs
    where
        xs = splitToList x

sumListDigits :: [Integer] -> Integer
sumListDigits [] = 0
sumListDigits (x:xs) = sumDigits x + sumListDigits xs

checkSum :: [Integer] -> Integer
checkSum xs = (sumListDigits xs') `mod` 10
    where
        xs' = doubleSecondNumber xs

isValidCard :: Integer -> Bool
isValidCard x
    | checkSum x' == 0 = True
    | otherwise = False
    where
        x' = splitToList x

boolToYes :: Bool -> String
boolToYes t = if t then "yes" else "no"

main = do
    putStrLn "Please input your credit card number: "
    cardNum <- getLine
    let result = isValidCard (read cardNum :: Integer)
    putStrLn ("Is " ++ cardNum ++ " valid? " ++ boolToYes result)
