from math import sin

F = lambda x, y, z: (x & y) | (~x & z)
G = lambda x, y, z: (x & z) | (~z & y)
H = lambda x, y, z: x ^ y ^ z
I = lambda x, y, z: y ^ (~z | x)
T = [ int(2 ** 32 * abs(sin(i + 1))) for i in range(64) ]
p1 = [ (0 + i * 1) % 16 for i in range(16) ] + \
		[ (1 + i * 5) % 16 for i in range(16) ] + \
		[ (5 + i * 3) % 16 for i in range(16) ] + \
		[ (0 + i * 7) % 16 for i in range(16) ]
p2 = [ [ 7, 12, 17, 22 ],
		[ 5, 9, 14, 20 ],
		[ 4, 11, 16, 23 ],
		[ 6, 10, 15, 21 ] ]
funcs = [ F, G, H, I ]

def loopshift(x, s):
	return ((x << s) | ((x & 0xFFFFFFFF) >> (32 - s))) & 0xFFFFFFFF # 32 bit

def transform(a, b, c, d, k, s, i, f, X):
	return (b + loopshift((a + f(b, c, d) + int.from_bytes(X[4 * p1[k]:4 * p1[k] + 4], "little") + T[i - 1]), s)) & 0xFFFFFFFF # 32 bit

def md5(string):
	M = bytearray(string) # в БАЙТАХ
	L = (8 * len(string)) & 0xFFFFFFFFFFFFFFFF # 64 bit
	# шаг 1
	M.append(128) # 128 = 1000 0000 (1 байт)
	while (len(M) - 56) % 64 != 0: # в оригинале в БИТАХ 448 = 56 * 8; 512 = 64 * 8
		M.append(0)
	# шаг 2
	M += L.to_bytes(8, "little")
	# шаг 3
	A = 0x67452301; B = 0xEFCDAB89
	C = 0x98BADCFE; D = 0x10325476
	# шаг 4
	for i in range(len(M) // 64): # len(M) * 8 // 32 // 16
		X = M[i * 64:(i + 1) * 64]

		AA = A; BB = B
		CC = C; DD = D

		cnt = 1
		for rnd in range(4):
			for row in range(4):
				A = transform(A, B, C, D, p1[cnt - 1], p2[rnd][0], cnt + 0, funcs[rnd], X)
				D = transform(D, A, B, C, p1[cnt - 0], p2[rnd][1], cnt + 1, funcs[rnd], X)
				C = transform(C, D, A, B, p1[cnt + 1], p2[rnd][2], cnt + 2, funcs[rnd], X)
				B = transform(B, C, D, A, p1[cnt + 2], p2[rnd][3], cnt + 3, funcs[rnd], X)
				cnt += 4

		A = A + AA; A &= 0xFFFFFFFF
		B = B + BB; B &= 0xFFFFFFFF
		C = C + CC; C &= 0xFFFFFFFF
		D = D + DD; D &= 0xFFFFFFFF

	# шаг 5
	A = int.from_bytes(A.to_bytes(4, "little"), "big")
	B = int.from_bytes(B.to_bytes(4, "little"), "big")
	C = int.from_bytes(C.to_bytes(4, "little"), "big")
	D = int.from_bytes(D.to_bytes(4, "little"), "big")
	print("{0:X} {1:X} {2:X} {3:X}".format(A, B, C, D))

if __name__ == "__main__":
	#with open("test_picture.jpg", "rb") as f:
	#	message = f.read()
	#	print(message)
	#	md5(message)
	md5(b"md5")