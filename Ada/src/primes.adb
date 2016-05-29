-- TODO --
-- Build a linked list of Integer types

with Ada.Text_IO;
with Ada.Numerics.Elementary_Functions;
with Ada.Strings.Unbounded;
use Ada.Text_IO;
use Ada.Numerics.Elementary_Functions;

procedure primes is

	package UString renames Ada.Strings.Unbounded;

	type linkedInteger;

	type nextLink is access linkedInteger;

	type linkedInteger is
		record
			value	: Integer;
			next 	: nextLink;	
		end record;

	function isPrime (testCase: Integer; foundPrimes : nextLink) return Boolean; -- Returns true if testCase is prime

	function isPrime (testCase: Integer; foundPrimes : nextLink) return Boolean  is
	begin -- isPrime
		declare
			prime : nextLink;
		begin
			prime := foundPrimes;

			while Float(prime.value) <= Sqrt(Float(testCase)) and prime.next /= null loop
				if testCase rem prime.value = 0 then
					return False;
				end if;

				prime := prime.next;
			end loop;

			return True;
		end;
	end isPrime;
begin -- primes
	declare
		wasPrime : Boolean := False;
		foundPrimes : nextLink := new linkedInteger;
		newPrime : nextLink;
		testCase : Integer;
		counter : Integer;
	begin
		foundPrimes.all.value := 2;

		testCase := 3;
		counter := 0;

		declare
			prime : nextLink;
		begin
			prime := foundPrimes;

			while testCase < 1000000000 loop
				wasPrime := isPrime(testCase, foundPrimes);
				if wasPrime then
					-- Append the newly found prime number to foundPrimes
					newPrime := new linkedInteger;
					newPrime.value := testCase;
					prime.next := newPrime;
					prime := newPrime;

					counter := counter + 1;

					if counter rem 10000 = 0 then
						Put_Line("Found" & Integer'image(counter) & " primes. Currently on:" & Integer'image(testCase));
					end if;
				end if;

				testCase := testCase + 2;
			end loop;
		end;
	end;
end primes;