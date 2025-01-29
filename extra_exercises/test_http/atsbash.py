
frase = "abba"
abc = 'abcçdefghijklmnñopqrstuvwxyz'
encrypt = ''
for a in range(len(frase)):
    b = abc.find(frase[a])
    if b != -1:
        encrypt += abc[::-1][b]
print(encrypt)
