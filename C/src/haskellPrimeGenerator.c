#include <HsFFI.h>
#ifdef __GLASGOW_HASKELL__
#include "CPrimes_stub.h"
extern void __stdinit_CPrimes(void);
#endif
#include <stdio.h>

int main(int argc, char *argv[])
{
	hs_init(&argc, &argv);
#ifdef __GLASGOW_HASKELL__
	hs_add_root(__stginit_CPrimes);
#endif
	// This is where the main operations would go for prime generation
	hs_exit();
	return 0;
}
