#This must be run though the actual RSA repo,
#but not till everyone has made their pull request
import os, rsa

def extract():
	if os.path.exists("private.pen"):
		with open("private.pen", 'rb') as f:
			private = rsa.PrivateKey.load_pkcs1(f.read())
	else:
		print("Could not locate 'private.pen' file")
		return
	students = []
	os.chdir('students')
	#create a list of files that have the extension .txt
	files = [f for f in os.listdir() if os.path.isfile(f) and ".dat" in f]
	for f in files:
		with open(f,'rb') as t:
			msg = t.read()
		decoded = rsa.decrypt(msg, private).decode('ascii')
		data = decoded.split(',')
		data.append(f.replace('.dat',''))
		students.append(','.join(data)+'\n')
	os.chdir('..')
	record_students(students)

def record_students(students):
	os.system("git pull")
	with open("students.txt", 'w') as f:
		f.write("last, first_weber, first_nuames, period, weber, github\n")
		f.writelines(students)
	print("Student record created")

def pr_check():
	#return all open PR from repo
	os.system(f"gh pr --repo nuames-cs/RSA-Encryption list --limit 100 --state open > all.txt")
	#os.system("gh pr list --limit 1 --state open > next.txt")
	with open("all.txt", 'r') as f:
		data = f.readlines()
	os.system("rm all.txt")
	return data

def pr_next(all):
	try:
		data = all.pop()
		pr = int(data.split('\t')[0])
		return pr
	except IndexError:
		return False
	except ValueError:
		return False

def pr_code(pr):
	#access get access the the PRs changed files
	#return the files?
	os.system(f"gh pr --repo nuames-cs/RSA-Encryption diff {pr} --name-only > files.txt")
	with open("files.txt", 'r') as f:
		data = f.readlines()
	os.system("rm files.txt")
	for i in range(len(data)):
		data[i] = data[i].strip()
	return data

def pr_validate(files):
	#validate changes in PR to only be new encoded message.
	#delete any other changes
	bad = False
	dat_found = False
	for f in files:
		if f[:9] == 'students/' and f[-4:] == '.dat':
			dat_found = True
		elif f != 'student.py' and f != 'settings.json':
			bad = True
	if not dat_found:
		bad = True
	return not bad

def pr_merge(pr, valid):
	#merge the current open
	#print(f"{pr}: {valid}")
	if valid:
		os.system(f"gh pr merge {pr} -m")

def main():
	all = pr_check()
	next = pr_next(all)
	bad = []
	while next:
		valid = pr_validate(pr_code(next))
		pr_merge(next, valid)
		next = pr_next(all)
	extract()

if __name__ == "__main__":
	main()
