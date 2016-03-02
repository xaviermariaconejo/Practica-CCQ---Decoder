import math

def factorization(n):
	factors = []

	while (n%2 == 0):
		factors.append(2)
		n = n/2

	# n must be odd at this point.  So we can skip one element (Note i = i +2)
	i = 3
	while i <= math.sqrt(n):
		# While i divides n, store i and divide n
		while (n%i == 0):
			factors.append(i)
			n = n/i
		i = i + 2    

	# This condition is to handle the case whien n is a prime number
	# greater than 2
	if (n > 2):
		factors.append(n);

	return factors;

def aux(a, b):
	x = 0
	y = 1
	u = 1
	v = 0
	while (a != 0):
		q = b / a
		r = b % a
		m = x - u*q
		n = y - v*q
		b = a
		a = r
		x = u
		y = v
		u = m
		v = n
	return [x, y]

def modpow(base, exp, mod):
	res = 1
	base = base % mod
	while (exp > 0):
		if (exp & 1):
			res = (res * base) % mod
		exp = exp >> 1
		base = (base * base) % mod
	return res

def main():
	n = 297045209
	e = 31273
	L = 9

	# factorize n
	factors = factorization(n);

	if (len(factors) != 2):
		print "Wrong public key"
		return 

	p = factors[0]
	q = factors[1]
	print "Factors de n: "
	print "p = " + str(p) + "\n"
	print "q = " + str(q) + "\n \n"

	totient_n = (p - 1) * (q - 1)

	# Llave privada
	p_key = aux(e, totient_n)[0];
	print "private key = " + str(p_key) + "\n \n"

	# Leer archivo
	file = open("xifratfinal.txt", 'r+b')    
	if (not file):
		print "Unable to open the file"
		return 

	buff = file.read()
	file.seek (0, 2)
	length = file.tell()
	file.close()

	print "Encoded message = " + buff + "\n \n"
	
	num_blocks = length/9
	D = []
	for i in range (0, num_blocks):
		# Partir
		num = int(buff[(i*9) : (i*9 + 9)])

		# Decodificar
		num = modpow(num, p_key, n)

		# Unir
		dnum = str(num)
		while (len(dnum) < 8):
			dnum = "0" + dnum
		D.append(dnum)

	# Imprimir
	B = "".join(D)
	print"Decoded message = ",
	i = 0
	s = ""
	while (i < len(B) - 3):
		s += chr(int(B[i])*100 + int(B[i+1])*10 + int(B[i+2]))
		i+=3
	print s

main()
