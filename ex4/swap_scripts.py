
from bitcoin.core.script import *

######################################################################
# This function will be used by Alice and Bob to send their respective
# coins to a utxo that is redeemable either of two cases:
# 1) Recipient provides x such that hash(x) = hash of secret 
#    and recipient signs the transaction.
# 2) Sender and recipient both sign transaction
# 
# TODO: Fill this in to create a script that is redeemable by both
#       of the above conditions.
# 
# See this page for opcode: https://en.bitcoin.it/wiki/Script
#
#

# This is the ScriptPubKey for the swap transaction
def coinExchangeScript(public_key_sender, public_key_recipient, hash_of_secret):
    return [
        public_key_recipient,
        OP_CHECKSIG,#验证解锁脚本是否包含接受者签名
        OP_DROP,#丢弃栈顶的true,进行下一步
        OP_DUP,#复制栈顶的secret或sig_sender进行后续判断
        public_key_sender,
        OP_CHECKSIG,#是否为发送者签名
        OP_IF,#如果是
        OP_DROP,# 清空站内元素
        OP_1,#压入true
        OP_ELSE,#如果不是
        OP_HASH160,#hash栈顶的secret
        hash_of_secret,
        OP_EQUAL,#该元素是不是秘密x
        OP_ENDIF
    ]

# This is the ScriptSig that the receiver will use to redeem coins
def coinExchangeScriptSig1(sig_recipient, secret):
    return [
        # fill this in!
        secret,
        sig_recipient
    ]

# This is the ScriptSig for sending coins back to the sender if unredeemed
def coinExchangeScriptSig2(sig_sender, sig_recipient):
    return [
        # fill this in!
        sig_sender,
        sig_recipient
    ]

#
#
######################################################################

