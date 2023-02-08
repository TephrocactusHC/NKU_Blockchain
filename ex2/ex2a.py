from sys import exit
from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinSecret
from utils import *
from config import my_private_key, my_public_key, my_address, faucet_address
from ex1 import send_from_P2PKH_transaction


cust1_private_key = CBitcoinSecret(
    'cVRoenyBCjuCbr97W95QLGmZV37Gjuio55hqegY2iRQMg5WVdZbf')
cust1_public_key = cust1_private_key.pub
cust2_private_key = CBitcoinSecret(
    'cP1vqG29g2ZeeuUZBpgcdfTuQVtesg6FqJ9wXR4qZyHFiprBW7rs')
cust2_public_key = cust2_private_key.pub
cust3_private_key = CBitcoinSecret(
    'cP1vqG29g2ZeeuUZBpgcdfTuQVtesg6FqJ9wXR4qZyHFiprBW7rs')
cust3_public_key = cust3_private_key.pub


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 2

# You can assume the role of the bank for the purposes of this problem
# and use my_public_key and my_private_key in lieu of bank_public_key and
# bank_private_key.

ex2a_txout_scriptPubKey = [my_public_key,     #银行公钥
OP_CHECKSIGVERIFY,
OP_1,
cust1_private_key.pub,
cust2_private_key.pub,
cust3_private_key.pub,       #三个客户的公钥
OP_3,
OP_CHECKMULTISIG]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.00007657
    txid_to_spend = (
        '445aba232e61ac913f1c24c29f2c5eb19bcc87ff81ae5d03260842a753de0736')
    utxo_index = 2
    ######################################################################

    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        ex2a_txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)
