import base64

def crypt_char(passwd,type):
	list_ascii=[51, 125, 69, 121, 80, 9, 22, 38, 61, 15, 67, 86, 118, 29, 26, 73, 106, 58, 115, 72, 83, 89, 78, 31, 100, 20, 44, 18, 79, 60, 77, 54, 109, 33, 21, 117, 56, 94, 114, 116, 71, 108, 23, 76, 127, 35, 27, 91, 112, 55, 11, 95, 82, 93, 105, 52, 24, 17, 42, 12, 49, 1, 74, 66, 14, 122, 53, 36, 32, 28, 97, 120, 65, 62, 110, 34, 90, 3, 64, 5, 46, 30, 0, 88, 48, 68, 7, 113, 96, 85, 16, 70, 37, 98, 81, 57, 6, 84, 8, 47, 13, 10, 99, 19, 25, 102, 4, 103, 87, 92, 126, 43, 2, 39, 124, 41, 101, 63, 111, 119, 59, 107, 50, 40, 45, 123, 104, 75]
	if type == 'en':
		en_passwd = ''
		for i in range (len(passwd)):
			char_ascii = ord(passwd[i])
			en_char = chr(list_ascii[char_ascii])
			en_passwd = en_passwd + en_char
		encode = base64.b64encode(en_passwd)
		return encode		
	else:
		decode_passwd = ''
		decode = base64.b64decode(passwd)
		for i in range (len(decode)):
			dechar_ascii = ord(decode[i])
			de_char = chr(list_ascii.index(dechar_ascii))
			decode_passwd = decode_passwd + de_char
		return decode_passwd