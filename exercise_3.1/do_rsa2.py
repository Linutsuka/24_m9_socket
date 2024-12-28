
import os.path as path
import sys
import rsa
import multiprocessing
import base64 as bs

#   Object description:
#   Agafa una Opcio: 'e,d', la ruta dels arxius .pem, i el plaintext/ciphertext.
#   Agafa una Opcio: 'g' i la ruta de la creació de les keys.
#   creation_keys() Crea una public.pem i una private.pem a la ruta destinada, si ja són creadas les torna a fer.
#   read_keys() Llegeix la public.pem i la private.pem a la ruta que s'ha donat.
#   encrypt_text()  Realitza read_keys(), i encripta el text 'utf-8'.
#   decrypt_text()  Realitza read_keys() i desencripta el text 'utf-8'.
#   b64_return()    Retorna el text encode o decode en base64, demana per entrada les varaibles opció i text.


#   main()  Demana 3 Arguments, si no son els proposats indica error.
#           Si es demana l'opció 'e', encripta i printeja a bytes.
#           Escriu per comanda de text el text encriptat.
#           Si es demana l'opicó 'd' desencripta el text passat.
#           Escriu per comanda de text el text desencriptat.
#           Si es demana l'opció 'g' crea les claus public.pem, private.pem.



class RSA_:
    def __init__(self,ops,pathKeys,text):
        option = {"e","d","g"}
        if ops.lower() not in option:
            print(f"Provide the right arguments._1")
            sys.exit()
        if ops == "e":
             self.ciphertxt = ''
             self.plaintxt = text
        if ops == "d":
             self.ciphertxt = text
             self.plaintxt = ""
        self.keys = pathKeys
        self.privateKey = None
        self.publicKey = None
    def get_ciphertext(self):
            return self.ciphertxt
    def get_plaintxt(self):
            return self.plaintxt
    def get_pathKeys(self):
            return self.keys
    def set_ciphertext(self,c):
            self.ciphertxt = c
    def set_plaintxt(self,c):
            self.plaintxt = c
    def self_pathKeys(self,c):
            self.keys = c

            #KEYS
    def get_publickey(self):
         return self.publicKey
    def set_publickey(self,c):
         self.publicKey = c
    def get_privatekey(self):
         return self.privateKey
    def set_privatekey(self,c):
         self.privateKey = c

    # Creation of public and private key rsa.
    def creation_keys(self):
        (pubkey, privkey) = rsa.newkeys(2048, poolsize=multiprocessing.cpu_count())
        

        pathK = self.get_pathKeys() + "/"

        self.set_publickey(pubkey)
        self.set_privatekey(privkey)

        if  not path.isfile(pathK + "private.pem") or path.isfile(pathK + "private.pem"): #   IF NO CREATED, create new key, if it exist rewrite
             with open(pathK + "private.pem","wb") as f:
                f.write(privkey.save_pkcs1("PEM"))


        if not path.isfile(pathK + "public.pem") or path.isfile(pathK + "public.pem"):
            with open(pathK + "public.pem","wb") as f:
                 f.write(pubkey.save_pkcs1("PEM"))


       

   #   Read the keys on the proposed path.
    def read_keys(self):
        pathK = self.get_pathKeys() + "/"
        
        if path.isfile(pathK + "private.pem"):
            with open(pathK + "private.pem","rb") as f:
                  line = f.read() 

            
            self.set_privatekey(rsa.PrivateKey.load_pkcs1(line))
        else:
            print(f"Not private.pem found.")
        if path.isfile(pathK + "public.pem"):
            with open(pathK + "public.pem","rb") as f:
                line = f.read()
            self.set_publickey(rsa.PublicKey.load_pkcs1(line))
        else:
             print(f"Not public.pem found.")

    #   Get the plaintext and encode, then modify the self.ciphertext var.
    def encrypt_txt (self):
        try:
            
            self.read_keys()
            #encrypt
            message = self.get_plaintxt().encode('utf-8')
            crypto = rsa.encrypt(message, self.get_publickey())
            
            #new
            self.set_ciphertext(crypto)


            
        except:
             print(f"Error encrypting.")
             
    #   Get self.ciphertext and decode, modify the self.ciphertext var.
    def decrypt_txt(self):
       

            self.read_keys()
            message = self.get_ciphertext()

            message = rsa.decrypt(message, self.get_privatekey() )
            self.set_ciphertext(message.decode('utf-8'))

      

    #   Encode or decode the text with base64.
    def b64_return (self,option,message):
        try:

            if option == 'e':
                try:

                    message = str(bs.b64encode(message))
                    
                    return message[2:-1]   #   quit the typeof on final output.
                    #return message
                
                except:
                    print("Error with the b64, import the package 'base64' and change name as bs.")
            else:
                try:

                    message = bs.b64decode(message)
                    return message
                
                except:
                    print("Error with the b64, import the package 'base64' and change name as bs.")

        except:
             print("Error with the function 'b64_return', provide the rights parametres, 'Mode: 'e','d' and text.\nImport the package 'base64' and rename as 'bs'.")


    # set plaintext >> para funcionar >> retorna ciphertxt
    def encryptb64(self):

        self.encrypt_txt()
        message = cript.b64_return('e',cript.get_ciphertext())
        return message
    # set ciphertxt >> para funcionar >> retorna ciphertxt
    def decrypt64(self):

        cript.set_ciphertext(cript.b64_return('d',cript.get_ciphertext()))
        self.decrypt_txt()
        return self.get_ciphertext()
         



if __name__ == "__main__":
    #   If they give you 4 arguments, encrypt or decrypt.
    if(len(sys.argv) >= 4): 
        cript = RSA_(sys.argv[1],sys.argv[2],sys.argv[3])
        if sys.argv[1] == "e":

            #cript.encrypt_txt()
            #test = cript.get_ciphertext()
            
            #print(f"DEVUELVE : {cript.b64_return('e',cript.get_ciphertext())}")

            #cript.decrypt_txt()
            #print(cript.get_ciphertext())
            print(cript.encryptb64())

        else:
            print(cript.decrypt64())
            #cript.set_ciphertext(cript.b64_return('d',cript.get_ciphertext()))
            #cript.decrypt_txt()
            #print(f"{cript.get_ciphertext()}")

    #   If the option is 'g' create the keys on given path.
    elif (len(sys.argv) >= 3):
         cript = RSA_(sys.argv[1],sys.argv[2],"")
         
         if sys.argv[1] == "g":
            cript.creation_keys()
    else:
        print(f"Provide the rights arguments. Option, PathOfKeys and plaintext or ciphertext.\nIf you want generate KEYS provide, Option(g) and path.")
        print(f"You provide: {len(sys.argv)} arguments. Make sure you put the rights.")
            