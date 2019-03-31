def recurse (arg1, arg2, arg3) :
	var_1c = arg1
	var_20 = arg2
	var_24 = arg3
	rdx = var_1c
	rax = var_20
	rax_1 = rax + rdx
	var_c = rax_1
	if (var_24 == 16) :
		if (var_c == 116369) :
			return 1
	if (var_24 > 15):
		return 0
	else :
		rax_3 = var_24
		rdx_1 = rax_3 + 1
		rcx_1 = var_c
		rax_4 = var_20
		rsi = rcx_1
		rdi = rax_4
		return recurse(rdi, rsi, rdx_1)

print("numbers:")

for x in range(100) :
	for y in range(100) :
		if recurse(x, y, 0) != 0 :
			print("DONE", x, y)
