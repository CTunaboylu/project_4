import peer as a 
import random
import hashlib
import subprocess
# check for hash bit size and mod if it will only be int
def creation_test(IP:str, num:int): #IP as string, num:int as num of peers
	h_shake = hashlib.shake_128()
	i=0
	for i in range(num):
		random_id = random.randint(5000,6000)
	while random_id in a.id_array:
		random_id= random.randint(5000,6000)
	a.credentials(random_id) # add the pseudo-ID to credentials list to keep track of it - IP assigning starts with random_id 
	m_port = str(a.port + random_id)
	h_shake.update((a.IP+m_port).encode())
	random_id = h_shake.digest(128)
	print(random_id)
	i += 1

def create_peers(num:int):
	#subprocess.run(["python",sys.argv[0], IP+str(random_id), "first=FALSE"])
	for i in range(num):
		random_id = random.random(5000, 6000)
		while random_id in a.id_array:
			random_id = random.random(5000, 6000)
		port = str(a.port + random_id)
		command = 'python peer.py'
		subprocess.call(['python', 'peer.py', '127.0.01:'+port, 'first=FALSE']) 

create_peers(5)
print(a.id_array)
