from do_rsa2 import RSA_
import sys


try:
    if len(sys.argv) >= 3:
        crypt = RSA_(sys.argv[1],sys.argv[2],"")
        if sys.argv[1] == "g":
            crypt.creation_keys()
except:
    print(f"Error generating keys.")