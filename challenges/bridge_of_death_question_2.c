#include <stdio.h>
#include <stdlib.h>

ulong func2(uint in1,uint param_2,uint param_3);


int main() {
	for (uint i = 0; i < 100; ++i) {
		for (ulong j = 0; j < 100; ++j) {
			if (func2(i, 0, 0x14) == j) {
				printf("%d\n", i);
				printf("%lu\n", j);
				break; 
			}
		}	
	}

	return 0;
}

ulong func2(uint in1,uint param_2,uint param_3)

{
  uint uVar1;
  ulong uVar2;
  
  // puts("kek");
  uVar1 = param_2 + ((int)((param_3 - param_2) + (param_3 - param_2 >> 0x1f)) >> 1);
  if ((int)in1 < (int)uVar1) {
    uVar2 = func2(in1,param_2,uVar1 - 1);
    uVar2 = (ulong)(uVar1 + (int)uVar2);
  }
  else {
    if ((int)uVar1 < (int)in1) {
      uVar2 = func2(in1,uVar1 + 1,param_3);
      uVar2 = (ulong)(uVar1 + (int)uVar2);
    }
    else {
      uVar2 = (ulong)uVar1;
    }
  }
  return uVar2;
}

