Run `python keygen.py` to create a random seed, and then from that seed generate addresses m/0h/0/[0-1]/[0-4].

This will create a file `bitcoin_config.txt`, which contains the pubkey and chain code corresponding to m/0h/0.

Then, you can run `python addrgen.py`, which will also generate m/0h/0/[0-1]/[0-4], but without knowing any private keys.