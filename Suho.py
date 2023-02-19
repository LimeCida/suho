import os
import pathlib
from cryptography.fernet import Fernet
import base64, hashlib
import sys
from getpass import getpass

"""
Hello!!! 
Thanks for taking your time to look through my code to see if I'm hiding anything from you.
I'm made to protect the thoughts of people like you!

I have a name, It's Suho. Pronounced "sue" and "hoh". It means "guardian" or "protector".
Feel free to modify my code and improve me in a way that suits you, thanks!

-수호
"""
 
class Suho():
	def __init__(self, path, mode):
		self.encrypt = True
		self.path = path
		self.verifyPath(path)
		self.verifyMode(mode)

		self.password = getpass("Password: ")

	def verifyPath(self, pathStr):
		if not os.path.dirname(os.path.abspath(__file__)) in pathStr:
			pathStr = os.path.dirname(os.path.abspath(__file__)) + "\\" +pathStr
			
		pathToFile = pathlib.Path(pathStr)
		if not pathToFile.is_file():
			raise Exception("Error, cannot find the file. Here's what I'm looking for: " + pathStr)
	
	def verifyMode(self, mode):
		if mode == "d" or mode == "decrypt":
			self.encrypt = False
		elif not mode == "e" and not mode == "encrypt":
			raise Exception("\nInvalid syntax! Please specify whether to encrypt to decrypt. \n[EG: Suho.py \"" + os.path.dirname(os.path.abspath(__file__)) + "\\plaintext.txt\" encrypt]")

	def perform(self):
		fileObject = open(self.path, "r")

		#I will encrypt/decrypt the data below...
		data = fileObject.read()
		bytepass = bytes(self.password, 'utf-8')
		key = self.gen_fernet_key(bytepass)
		fernet = Fernet(key)

		#Below will be my result file
		fileName = os.path.basename(self.path)

		if self.encrypt:
			encData = fernet.encrypt(data.encode())
			print("Data encrypted...")
			f = open("[ENCRYPTED]"+fileName, "wb")
			f.write(encData)
			f.close()
		else:
			print(data.encode())
			decData = fernet.decrypt(data.encode()).decode()
			print("Data decrypted...")
			if("[ENCRYPTED]" in fileName):
				fileName = fileName.replace("[ENCRYPTED]", "[DECRYPTED]")
			else:
				fileName = "[DECRYPTED]"+fileName
			f = open(fileName, "w")
			f.write(str(decData))
			f.close()

	def gen_fernet_key(self, passcode:bytes) -> bytes:
		assert isinstance(passcode, bytes)
		hlib = hashlib.md5()
		hlib.update(passcode)
		return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def main():
	if (len(sys.argv) != 3):
		""
		raise Exception("Invalid number of syntax! \n\n"+
		"USAGE --> Suho.py \"[PATH]\" \"[MODE]\" \n\n" +
		"Please tell me where the target file is, the password you want to use and whether I'm encrypting or decrypting. \nFor instance... \n" +
		"encrypting --> Suho.py \"" + os.path.dirname(os.path.abspath(__file__)) + "\\plaintext.txt\" encrypt \n" +
		"decrypting --> Suho.py \"" + os.path.dirname(os.path.abspath(__file__)) + "\\encrypted.txt\" decrypt \n\n" +
		"Note: you don't have to fret, I can tell whether you are using absolute or relative pathing. \nUse whichever you are comfortable with. =)\n\n")

	path = sys.argv[1]
	mode = sys.argv[2]

	suho = Suho(path, mode)

	suho.perform()

	print("Success!!!")


if __name__ == "__main__":
    main() #ONLY RUN main() if this file is called DIRECTLY.