import bitcoin
import mnemonic
import os
import hashlib
import hmac

hmac_hash = lambda key, data : hmac.new(key, data, hashlib.sha512).digest()

print "Generating seed..."
hex_seed_256 = os.urandom(32).encode('hex')
print "Initial seed (raw data): " + hex_seed_256
print "Electrum mnemonic:" + " ".join(mnemonic.mn_encode(hex_seed_256))

hex_seed_512 = hmac_hash("Bitcoin mnemonic", hex_seed_256).encode('hex')
print "derived seed (raw): " + hex_seed_512
# Master key, master chain, Master pubkey, Master pubkey (compressed format)
k, c, K, Kcomp = bitcoin.bip32_init(hex_seed_512)

def generate(path, key, chain):
	"""
	generate(path, key, chain) -> key2, chain2
	path is a list of tuples like [(index1, is_hardened),(index2, is_hardened)]
	key is the root private key
	chain is the root chain
	key2 and chain2 are the results of following this BIP32 derivation path
	"""
	(index, is_hardened), path2 = path[0], path[1:]
	bip32_i = index + bitcoin.BIP32_PRIME if is_hardened else index 
	key2, chain2 = bitcoin.CKD(key,chain, bip32_i)
	if len(path2) == 0:
		return key2, chain2
	else:
		return generate(path2, key2, chain2)

# An Array of (index,is_hardened) tuples
path = [(0, True),(0, False)] # Corresponds to /0h/0
main_key, main_chain = generate(path, k, c)

for is_change in [0,1]:
	receiving_key, receiving_chain = generate([(is_change,False)], main_key, main_chain)
	for path, i in [([(i,False)],i) for i in range(5)]:
		addr_key, _ = generate(path, receiving_key, receiving_chain)
		pubkey, pubkey_compressed = bitcoin.get_pubkeys_from_secret(addr_key)
		addr = bitcoin.hash_160_to_bc_address(bitcoin.hash_160(pubkey_compressed))
		print "m/0h/0/{}/{} = {}".format(is_change, i, addr)

main_pubkey, main_pubkey_compressed = bitcoin.get_pubkeys_from_secret(main_key)

print "Writing to file."
with open("bitcoin_config.txt","w") as config_file:
	config_file.write("master_pubkey: " + main_pubkey.encode('hex')  + "\n")
	config_file.write("master_chain: " + main_chain.encode('hex') + "\n")