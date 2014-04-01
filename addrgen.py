# Wyager's simple BIP32 public generation script
# https://github.com/wyager/Bitcoin-HD-wallet-generator

import bitcoin
import sys

pubkey = None
chain = None
addresses = None
with open("bitcoin_config.txt") as config_file:
	desc, pubkey = config_file.readline().split()
	if(desc != "master_pubkey:"):
		print "Error reading pubkey"
	main_pubkey = pubkey.decode('hex')

	desc, chain = config_file.readline().split()
	if(desc != "master_chain:"):
		print "Error reading chain"
	main_chain = chain.decode('hex')


if (pubkey == None) or (chain == None):
	print "Error loading config."
	sys.exit(0)

def generate_from_pub(path, pubkey, chain):
	"""
	generate_from_pub(path, pubkey, chain) -> pubkey2, pubkey2_compressed, chain2
	path is a list of tuples like [(index1, is_hardened),(index2, is_hardened)]
	pubkey is the root pubkey
	chain is the root chain
	pubkey2, pubkey2_compressed, and chain2 are the results of following this BIP32 derivation path
	Because this is a pubkey-based generation, none of the path elements may be hardened.
	"""
	(index, is_hardened), path2 = path[0], path[1:]
	if is_hardened:
		raise Exception("Error: Trying to derive a hardened address using the pubkey")
	bip32_i = index
	key2, key2_comp, chain2 = bitcoin.CKD_prime(pubkey,chain, bip32_i)
	if len(path2) == 0:
		return key2, key2_comp, chain2
	else:
		return generate(path2, key2, chain2)

for is_change in [0,1]:
	receiving_pubkey, receiving_pubkey_compressed, receiving_chain = generate_from_pub([(is_change,False)], main_pubkey, main_chain)
	for path, i in [([(i,False)],i) for i in range(5)]:
		_, addr_pubkey_compressed, _ = generate_from_pub(path, receiving_pubkey, receiving_chain)
		addr = bitcoin.hash_160_to_bc_address(bitcoin.hash_160(addr_pubkey_compressed))
		print "m/{}/{} = {}".format(is_change, i, addr)
