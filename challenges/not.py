x = "99939e988493cfcf8f8ca09e919ba087cf8d8ca09e919ba08d9a9e9b8ca090a09286a09ec9c79acacbcbc99d9ece9b82"


b = (bin(int(x, 16))[2:])
c = ""

for i in b:
	if i == "1":
		c += "0"
	else :
		c += "1"

hex(int(c, 2))
