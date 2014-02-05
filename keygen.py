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


print "Generating master branch 0..."
k0, c0 = bitcoin.CKD(k, c, 0 + bitcoin.BIP32_PRIME) # K0 can't be derived from K
K0, Kc0 = bitcoin.get_pubkeys_from_secret(k0)

for branch_number in [0]:
	k0_n, c0_n = bitcoin.CKD(k0, c0, branch_number) # K0_n can be derived from K0
	K0_n, Kc0_n= bitcoin.get_pubkeys_from_secret(k0_n)

	is_change = 0
	k0_n_m_a, c0_n_m_a = bitcoin.CKD(k0_n, c0_n, is_change) # K0_n_m_a can be derived from K0_n_m
	K0_n_m_a, Kc0_n_m_a= bitcoin.get_pubkeys_from_secret(k0_n_m_a)
	for i in range(0,5):
		k0_n_m_b, c0_n_m_b = bitcoin.CKD(k0_n_m_a, c0_n_m_a, i) # K0_n_m_b can be derived from K0_n_m_a
		K0_n_m_b, Kc0_n_m_b= bitcoin.get_pubkeys_from_secret(k0_n_m_b)
		addr0_n_m_b = bitcoin.hash_160_to_bc_address(bitcoin.hash_160(Kc0_n_m_b))
		print "Addr 0_{}_{}: ".format(branch_number, i) + addr0_n_m_b

	is_change = 1
	k0_n_m_a, c0_n_m_a = bitcoin.CKD(k0_n, c0_n, is_change) # K0_n_m_a can be derived from K0_n_m
	K0_n_m_a, Kc0_n_m_a= bitcoin.get_pubkeys_from_secret(k0_n_m_a)
	for i in range(0,5):
		k0_n_m_b, c0_n_m_b = bitcoin.CKD(k0_n_m_a, c0_n_m_a, i) # K0_n_m_b can be derived from K0_n_m_a
		K0_n_m_b, Kc0_n_m_b= bitcoin.get_pubkeys_from_secret(k0_n_m_b)
		addr0_n_m_b = bitcoin.hash_160_to_bc_address(bitcoin.hash_160(Kc0_n_m_b))
		print "Change Addr 0_{}_{}: ".format(branch_number, i) + addr0_n_m_b

# print "Signature of \"foobar\":"
# ec_key = bitcoin.regenerate_key(bitcoin.SecretToASecret(k_n, True))
# #Message, whether the privkey (k_n) is compressed, and the address
# print ec_key.sign_m_aessage("foobar", bitcoin.is_compressed(ec_key), addr_n)


print "Writing to file."
with open("bitcoin_config.txt","w") as config_file:
	config_file.write("master_pubkey: " + K0_n.encode('hex')  + "\n")
	config_file.write("master_chain: " + c0_n.encode('hex') + "\n")