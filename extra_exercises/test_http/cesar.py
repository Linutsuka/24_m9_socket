frase = "abba"
dec = 2
abc = 'abcçdefghijklmnñopqrstuvwxyz'
encrypt = ''

for a in range(len(frase)):
    c = abc.find(frase[a])
    if c != -1:
        if (c + dec) > len(abc):
            c = (c + dec) % len(abc)
            encrypt += abc[c]
        else:
            encrypt += abc[c + dec]
print(encrypt)


