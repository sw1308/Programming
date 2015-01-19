type RegExp a :: [a] -> (Maybe [a], [a])

nil :: RegExp a
nil s = (Just [], s)

range :: (a -> Bool) -> RegExp a
range r a
	| r p@(x:xs) == True = (Just [x], xs)
	| otherwise = (Nothing, p)

one :: Eq a => a -> RegExp a
one a = range (==a)

arb :: RegExp a
arb a = range (const True)

alt :: Eq a => RegExp a -> RegExp a -> RegExp a
alt r0 r1
	| 
