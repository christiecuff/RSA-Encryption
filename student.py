#import dependencies
import os, sys
try:
	import rsa
except:
	print("RSA module needed -- installing")
	os.system("pip3 install rsa")
	import rsa
	print("complete")

#load public key
if os.path.exists("public.pen"):
	with open("public.pen", 'rb') as f:
		public = rsa.PublicKey.load_pkcs1(f.read())
else:
	sys.exit('Inform Mr. Simonsen that the program could\'t find "public.pen"')

#prompt for relevant information
last = input("What is your last name as shown in Weber State's records?\n").title()
first_weber = input("What is your first name as shown in Weber State's records?\n").title()
first_nuames = ''
if input("Does your first name in Weber State's records match the first name in NUAMES's records?(Y/n)\n").lower() in("no","n"):
	first_nuames = input("What is your first name in NUAMES's records?\n").title()
else:
	pref = ''
confirm = False
while not confirm:
	weber = input("Enter you Weber State username (what comes before '@mail.weber.edu')\n").lower()
	print("Double check that your username has been entered correctly.")
	print(weber)
	if input("Is you Weber State username entered correctly?(Y/n)\n").lower() in ('y','yes'):
		confirm = True

valid = False
while not valid:
	try:
		period = int(input("What class period are you in?\n"))
	except ValueError:
		print("That wasn't a number.")
	if period not in range(1,9):
		print(f"{period} is not a valid class period.")
	else:
		valid = True
confirm = False
while not confirm:
	github = input("What's your GitHub username?\n")
	print("Double check that your username has been entered correctly.")
	print(github)
	if input("Is you GitHub username entered correctly?(Y/n)\n").lower() in ('y','yes'):
		confirm = True

#format text
data = f"{last},{first_weber},{first_nuames},{period},{weber}"
#encrypt text
code = rsa.encrypt(data.encode('ascii'), public)
#save encryption to file
with open(f"students/{github}.dat",'wb') as f:
	f.write(code)

print("encrypted file created")
