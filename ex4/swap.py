import time
import alice
import bob

######################################################################
#                                                                    #
#                                                                    #
#              CS251 Project 2: Cross-chain Atomic Swap              #
#                                                                    #
#                                                                    #
#                                                                    #
#              Written by:  #
#              December 12, 2022                                     #
#              Version 1.0.1                                         #
#                                                                    #
######################################################################
#
# In this assignment we will implement a cross-chain atomic swap
# between two parties, Alice and Bob.
#
# Alice has bitcoin on BTC Testnet3 (the standard bitcoin testnet).
# Bob has bitcoin on BCY Testnet (Blockcypher's Bitcoin testnet).
# They want to trade ownership of their respective coins securely,
# something that can't be done with a simple transaction because
# they are on different blockchains.
#
# This method also works between other cryptocurrencies and altcoins,
# for example trading n Bitcoin for m Litecoin.
# 
# The idea here is to set up transactions around a secret x, that
# only one party (Alice) knows. In these transactions only H(x) 
# will be published, leaving x secret. 
# 
# Transactions will be set up in such a way that once x is revealed,
# both parties can redeem the coins sent by the other party.
#
# If x is never revealed, both parties will be able to retrieve their
# original coins safely, without help from the other.
#
#
#
######################################################################
#                           BTC Testnet3                             #     
######################################################################
#
# Alice ----> UTXO ----> Bob (with x)
#               |
#               |
#               V
#             Alice (after 48 hours)
#
######################################################################
#                            BCY Testnet                             #
######################################################################
#
#   Bob ----> UTXO ----> Alice (with x)
#               |
#               |
#               V
#              Bob (after 24 hours)
#
######################################################################

######################################################################
#
# Configured for your addresses
# 
# TODO: Fill in all of these fields
#

alice_txid_to_spend     = "c19e590d49cbcd6c0822809d7cc17f0fe92431b4a2875ea34d9518ead8cdb96a"
alice_utxo_index        = 0
alice_amount_to_send    = 0.01150585

bob_txid_to_spend       = "af412981894bfa66c9e784703fb53fc3e7af5e7f6e70ff072849db6180863044"
bob_utxo_index          = 0
bob_amount_to_send      = 0.01

# Get current block height (for locktime) in 'height' parameter for each blockchain (and put it into swap.py):
#  curl https://api.blockcypher.com/v1/btc/test3
btc_test3_chain_height  = 2409410

#  curl https://api.blockcypher.com/v1/bcy/test3
bcy_test_chain_height   = 570576

# Parameter for how long Alice/Bob should have to wait before they can take back their coins
## alice_locktime MUST be > bob_locktime
alice_locktime = 5
bob_locktime = 3

tx_fee = 0.001

broadcast_transactions = True
alice_redeems = True

#
#
######################################################################


######################################################################
#
# Read the following function.
# 
# There's nothing to implement here, but it outlines the structure
# of how Alice and Bob will communicate to perform this cross-
# chain atomic swap.
#
# You will run swap.py to test your code.
#
######################################################################

def atomic_swap(broadcast_transactions=False, alice_redeems=True):
    # Alice reveals the hash of her secret x but not the secret itself
    hash_of_secret = alice.hash_of_secret()

    # Alice creates a transaction redeemable by Bob (with x) or by Bob and Alice
    alice_swap_tx, alice_swap_scriptPubKey = alice.alice_swap_tx(
        alice_txid_to_spend,
        alice_utxo_index,
        alice_amount_to_send - tx_fee,
    )

    # Alice creates a time-locked transaction to return coins to herself
    alice_return_coins_tx = alice.return_coins_tx(
        alice_amount_to_send - (2 * tx_fee),
        alice_swap_tx,
        btc_test3_chain_height + alice_locktime,
        alice_swap_scriptPubKey,
    )

    # Alice asks Bob to sign her transaction
    bob_signature_BTC = bob.sign_BTC(alice_return_coins_tx, alice_swap_scriptPubKey)

    # Alice broadcasts her first transaction, only after Bob signs this one
    if broadcast_transactions:
        alice.broadcast_BTC(alice_swap_tx)

    # The same situation occurs, with roles reversed
    bob_swap_tx, bob_swap_scriptPubKey = bob.bob_swap_tx(
        bob_txid_to_spend,
        bob_utxo_index,
        bob_amount_to_send - tx_fee,
        hash_of_secret,
    )
    bob_return_coins_tx = bob.return_coins_tx(
        bob_amount_to_send - (2 * tx_fee),
        bob_swap_tx,
        bcy_test_chain_height + bob_locktime,
    )

    alice_signature_BCY = alice.sign_BCY(bob_return_coins_tx, bob_swap_scriptPubKey)

    if broadcast_transactions:
        bob.broadcast_BCY(bob_swap_tx)

    if broadcast_transactions:
        print('Sleeping for 20 minutes to let transactions confirm...')
        time.sleep(60 * 20)

    if alice_redeems:
        # Alice redeems her coins, revealing x publicly (it's now on the blockchain)
        alice_redeem_tx, alice_secret_x = alice.redeem_swap(
            bob_amount_to_send - (2 * tx_fee),
            bob_swap_tx,
            bob_swap_scriptPubKey,
        )
        if broadcast_transactions:
            alice.broadcast_BCY(alice_redeem_tx)

        # Once x is revealed, Bob may also redeem his coins
        bob_redeem_tx = bob.redeem_swap(
            alice_amount_to_send - (2 * tx_fee),
            alice_swap_tx,
            alice_swap_scriptPubKey,
            alice_secret_x,
        )
        if broadcast_transactions:
            bob.broadcast_BTC(bob_redeem_tx)
    else:
        
        # Bob and Alice may take back their original coins after the specified time has passed
        completed_bob_return_tx = bob.complete_return_tx(
            bob_return_coins_tx,
            bob_swap_scriptPubKey,
            alice_signature_BCY,
        )
        completed_alice_return_tx = alice.complete_return_tx(
            alice_return_coins_tx,
            alice_swap_scriptPubKey,
            bob_signature_BTC,
        )
        if broadcast_transactions:
            print('Sleeping for bob_locktime blocks to pass locktime...')
            time.sleep(10 * 60 * bob_locktime)
            bob.broadcast_BCY(completed_bob_return_tx)

            print('Sleeping for alice_locktime blocks to pass locktime...')
            time.sleep(10 * 60 * max(alice_locktime - bob_locktime, 0))
            alice.broadcast_BTC(completed_alice_return_tx)

if __name__ == '__main__':
    atomic_swap(broadcast_transactions, alice_redeems)

# 所使用的账户信息如下所示：
# btc

# Alice

# Private key: cSrgj3nTUvPDUCAFoLMqYNspaYiogjJs5PaA2fSFWyrqCVwZ9cpL
# Address: mypxELiC9GaRWGMfAN4Z6R1KuQUYYPorDr
# 9853dc71aa4e107f5a38f494d9a9a5a77c55affbc4513fa8b7924fd5928d85ef

# Bob

# Private key: cW9wKQUqt5mH6KvusfCwdzL9BedBHEkCvXVbWdKSHxovixfJEbcE
# Address: n2HPJf8kDPSnEAyeKzLNBxkMfk3RESGfsF
# a6e4540ff5998788654ace194368ba54a873a970f766e6ce6cc3c1e0e7906b46




# token


# token
# alice
# Token 76cee1ed3c9b4e6aa021f8e01188bdc9
# bob
# Token b99fc91632a54040a7c1f2b8092fbef4




# bcy

# alice


# {
#   "private": "0af98ccef7c16a7d5deed650efeba2859255f40cd33b6854f18d7eb78a80c2fd",
#   "public": "02d8bc58354405ec3fe6045894688fbad84b281d7fd1038f857790eecba6e7dec1",
#   "address": "C9ybksHoqvxdZ4iFYmt1fVm4rpMwnJitw4",
#   "wif": "BohN5y2GaWhDX5KYjjHQi7sFpMNgTkw8fcVDR3JrhV9jf9N2c9sJ"
# }

# bob

# {
#   "private": "c9751710788a24008f8fea6f11229749f307bea84f2b08e70173a5f459b738b3",
#   "public": "0264daac5800b1ce8806a0184a416c6af82b32a876b98ed5186f4a32e9c935081e",
#   "address": "CGNfUxki6Mj28N5eycVTALqCZKwt4BjJky",
#   "wif": "Bv5dw9erqoUuTNv6MBQFVUF2S3a4Bx1b4r2ypcgUshK89xUGSfRL"
# }


# txid_to_spend

# alice

# c19e590d49cbcd6c0822809d7cc17f0fe92431b4a2875ea34d9518ead8cdb96a

# bob

# {
#   "tx_ref": "af412981894bfa66c9e784703fb53fc3e7af5e7f6e70ff072849db6180863044"
# }

# 交易最终输出如下所示：

# Alice swap tx (BTC) created successfully!
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "5f741528c6ce9e0efb5df3f1a4dd7d55040b158c2534e4d10dafa38e6793aa34",
#     "addresses": [
#       "mypxELiC9GaRWGMfAN4Z6R1KuQUYYPorDr"
#     ],
#     "total": 1050585,
#     "fees": 100000,
#     "size": 266,
#     "vsize": 266,
#     "preference": "high",
#     "relayed_by": "2001:250:401:6554:2440:5517:f3ca:6229",
#     "received": "2022-12-02T10:36:02.47123685Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "c19e590d49cbcd6c0822809d7cc17f0fe92431b4a2875ea34d9518ead8cdb96a",
#         "output_index": 0,
#         "script": "4830450221008b2ed3a700b230a9ea515c06e0e435809f72959750a854b54d16a2425ceb512b022039f7c09f476490d19afe0dceaec2c80bff93675bb2d67877f70c2e190e579fcf012103f67eca8c6ab04112e58b2d9ff24fa0639a716a81b39d3a5719b7afd47d81c342",
#         "output_value": 1150585,
#         "sequence": 4294967295,
#         "addresses": [
#           "mypxELiC9GaRWGMfAN4Z6R1KuQUYYPorDr"
#         ],
#         "script_type": "pay-to-pubkey-hash",
#         "age": 2349919
#       }
#     ],
#     "outputs": [
#       {
#         "value": 1050585,
#         "script": "21039a06ed497a075b86f181ee14b05b30f61f9b2f4a10e0816a14052f3274336990ad762103f67eca8c6ab04112e58b2d9ff24fa0639a716a81b39d3a5719b7afd47d81c342ac63755167a914853b775079232503df966e626618e1d388a957208768",
#         "addresses": null,
#         "script_type": "unknown"
#       }
#     ]
#   }
# }
# Bob swap tx (BCY) created successfully!
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "59e33ce64833d1faaa42598811585d426854b07cbd54d99d8486b0e8d175f5a6",
#     "addresses": [
#       "CGNfUxki6Mj28N5eycVTALqCZKwt4BjJky"
#     ],
#     "total": 900000,
#     "fees": 100000,
#     "size": 266,
#     "vsize": 266,
#     "preference": "high",
#     "relayed_by": "2001:250:401:6554:2440:5517:f3ca:6229",
#     "received": "2022-12-02T10:36:02.878079071Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "af412981894bfa66c9e784703fb53fc3e7af5e7f6e70ff072849db6180863044",
#         "output_index": 0,
#         "script": "483045022100a2ef3bd466aab9da1a6e82ed0c400f48b14e691c4e2e0023648318ee363bf531022049defb1a978ed3ff8526cc8577c8a606be5eaaf7d3aa7e1d97ae5c3c5b743cfb01210264daac5800b1ce8806a0184a416c6af82b32a876b98ed5186f4a32e9c935081e",
#         "output_value": 1000000,
#         "sequence": 4294967295,
#         "addresses": [
#           "CGNfUxki6Mj28N5eycVTALqCZKwt4BjJky"
#         ],
#         "script_type": "pay-to-pubkey-hash",
#         "age": 570563
#       }
#     ],
#     "outputs": [
#       {
#         "value": 900000,
#         "script": "2102d8bc58354405ec3fe6045894688fbad84b281d7fd1038f857790eecba6e7dec1ad76210264daac5800b1ce8806a0184a416c6af82b32a876b98ed5186f4a32e9c935081eac63755167a914853b775079232503df966e626618e1d388a957208768",
#         "addresses": null,
#         "script_type": "unknown"
#       }
#     ]
#   }
# }
# Sleeping for 20 minutes to let transactions confirm...
# Alice redeem from swap tx (BCY) created successfully!
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "e84791ac98806c63f64839c1ec9b0d2b5fead26e793dc0749166bd390fc5565d",
#     "addresses": [
#       "C9ybksHoqvxdZ4iFYmt1fVm4rpMwnJitw4"
#     ],
#     "total": 800000,
#     "fees": 100000,
#     "size": 182,
#     "vsize": 182,
#     "preference": "high",
#     "relayed_by": "2001:250:401:6554:2440:5517:f3ca:6229",
#     "received": "2022-12-02T10:56:03.292193868Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "59e33ce64833d1faaa42598811585d426854b07cbd54d99d8486b0e8d175f5a6",
#         "output_index": 0,
#         "script": "187468697349734153656372657450617373776f72643132334730440220030dcedc90af7b56543b90555c1cd36a64bf38f7948bef2c9a44796ce34686530220101851433f79e7954430faad11c3b5ccc5e5c10ef481849d0621eda27e84c2fb01",
#         "output_value": 900000,
#         "sequence": 4294967295,
#         "script_type": "unknown",
#         "age": 570701
#       }
#     ],
#     "outputs": [
#       {
#         "value": 800000,
#         "script": "76a914b8d590349a6282170301992b13ae708052d2900988ac",
#         "addresses": [
#           "C9ybksHoqvxdZ4iFYmt1fVm4rpMwnJitw4"
#         ],
#         "script_type": "pay-to-pubkey-hash"
#       }
#     ]
#   }
# }
# Bob redeem from swap tx (BTC) created successfully!
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "22464b8549a963fb747f884a52a3dd400b11cb2ef9d56ed4c391344b659af4e0",
#     "addresses": [
#       "n2HPJf8kDPSnEAyeKzLNBxkMfk3RESGfsF"
#     ],
#     "total": 950585,
#     "fees": 100000,
#     "size": 183,
#     "vsize": 183,
#     "preference": "high",
#     "relayed_by": "2001:250:401:6554:2440:5517:f3ca:6229",
#     "received": "2022-12-02T10:56:04.361888109Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "5f741528c6ce9e0efb5df3f1a4dd7d55040b158c2534e4d10dafa38e6793aa34",
#         "output_index": 0,
#         "script": "187468697349734153656372657450617373776f7264313233483045022100f3c6668eca83c51a0c57b402a1504b149edcf3d300beb194f8a8ea5bcd8b96b8022071f41466a1bf6cacd0363d82bfda0f42da2a593d28412598829e15fccc9a91f001",
#         "output_value": 1050585,
#         "sequence": 4294967295,
#         "script_type": "unknown",
#         "age": 2409425
#       }
#     ],
#     "outputs": [
#       {
#         "value": 950585,
#         "script": "76a914e3c9b2157a273f394605e8a071ed3e33f41af94388ac",
#         "addresses": [
#           "n2HPJf8kDPSnEAyeKzLNBxkMfk3RESGfsF"
#         ],
#         "script_type": "pay-to-pubkey-hash"
#       }
#     ]
#   }
# }

