import Data.Maybe

type RegExp a = [a] -> (Maybe [a], [a])

nil :: RegExp a
nil s = (Just [], s)

range :: (a -> Bool) -> RegExp a
range r p@(x:xs)
	| r x == True = (Just [x], xs)
	| otherwise = (Nothing, p)

one :: Eq a => a -> RegExp a
one a = range (==a)

arb :: RegExp a
arb = range (const True)

alt, sqn :: Eq a => RegExp a -> RegExp a -> RegExp a
(r0 `alt` r1) s
	| isJust m = t
	| otherwise = r1 s
	where t@(m,rs) = r0 s
(r0 `sqn` r1) s
	| isJust m0 && isJust m1 = (Just (fromJust m0 ++ fromJust m1), rs1)
	| otherwise = (Nothing, s)
	where
		(m0, rs0) = r0 s
		(m1, rs1) = r1 rs0

sqns :: Eq a => [a] -> RegExp a
sqns = (foldl sqn nil).(map one)
