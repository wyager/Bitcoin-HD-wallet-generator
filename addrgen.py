import bitcoin
import sys

pubkey = None
chain = None
addresses = None
with open("bitcoin_config.txt") as config_file:
	desc, pubkey = config_file.readline().split()
	if(desc != "master_pubkey:"):
		print "Error reading pubkey"
	pubkey = pubkey.decode('hex')

	desc, chain = config_file.readline().split()
	if(desc != "master_chain:"):
		print "Error reading chain"
	chain = chain.decode('hex')


if (pubkey == None) or (chain == None):
	print "Error loading config."
	sys.exit(0)

is_change = 0
K0_n_m_a, Kc0_n_m_a, c0_n_m_a = bitcoin.CKD_prime(pubkey, chain, is_change) # K0_n_m_a can be derived from K0_n_m
for i in range(0,5):
	K0_n_m_b, Kc0_n_m_b, c0_n_m_b = bitcoin.CKD_prime(K0_n_m_a, c0_n_m_a, i) # K0_n_m_b can be derived from K0_n_m_a
	addr0_n_m_b = bitcoin.hash_160_to_bc_address(bitcoin.hash_160(Kc0_n_m_b))
	print "Addr 0_0_{}: ".format(i) + addr0_n_m_b

is_change = 1
K0_n_m_a, Kc0_n_m_a, c0_n_m_a = bitcoin.CKD_prime(pubkey, chain, is_change) # K0_n_m_a can be derived from K0_n_m
for i in range(0,5):
	K0_n_m_b, Kc0_n_m_b, c0_n_m_b = bitcoin.CKD_prime(K0_n_m_a, c0_n_m_a, i) # K0_n_m_b can be derived from K0_n_m_a
	addr0_n_m_b = bitcoin.hash_160_to_bc_address(bitcoin.hash_160(Kc0_n_m_b))
	print "Change Addr 0_0_{}: ".format(i) + addr0_n_m_b