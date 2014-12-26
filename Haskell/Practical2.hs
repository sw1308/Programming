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
alt r0 r1 s
	| isJust m = t
	| otherwise r1 s
	where t@(m, rs) = r0 s

sqn :: Eq a => RegExp a -> RegExp a -> RegExp a
sqn r0 r1 s
	| isJust m0 && isJust m1 = (Just (fromJust m0 ++ fromJust m1), rs)
	| otherwise = t
	where
		(m0, ts) = r0 s
		(m1, rs) = r1 ts
