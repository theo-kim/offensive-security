#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main() {
	printf("%lu\n", strtol("123 Hello", NULL, 10) + 100);
}
