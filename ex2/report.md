所有需要填写的代码均在下方给出，对代码的说明以注释的形式逐行给出。
首先是填写私钥
然后是函数中的返回值
然后看一下主函数的内容
代码
EX2A
cust1_private_key = CBitcoinSecret(
 'cVRoenyBCjuCbr97W95QLGmZV37Gjuio55hqegY2iRQMg5WVdZbf')
cust1_public_key = cust1_private_key.pub
cust2_private_key = CBitcoinSecret(
 'cP1vqG29g2ZeeuUZBpgcdfTuQVtesg6FqJ9wXR4qZyHFiprBW7rs')
cust2_public_key = cust2_private_key.pub
cust3_private_key = CBitcoinSecret(
 'cP1vqG29g2ZeeuUZBpgcdfTuQVtesg6FqJ9wXR4qZyHFiprBW7rs')
cust3_public_key = cust3_private_key.pub
#首先是我申请的三个新的账户
PYTHON
ex2a_txout_scriptPubKey = [my_public_key,#银行公钥
OP_CHECKSIGVERIFY,#弹出 signature,pubkey, 验证两者是否匹配。如果验证为假,那么交易
直接失败
OP_1,#将数值1放在栈顶
cust1_private_key.pub,
cust2_private_key.pub,
cust3_private_key.pub, #三个客户的公钥
OP_3,#将数值3放在栈顶
OP_CHECKMULTISIG]#多重签名验证 , 弹出的数据根据 n/m 来确定.
PYTHON
amount_to_send = 0.00007657#这里是我们要交出去的钱
 txid_to_spend = (
 '445aba232e61ac913f1c24c29f2c5eb19bcc87ff81ae5d03260842a753de0736')
 #这是第一次实验所得到的分币的hash
 utxo_index = 2#这里用分币得到的第三个币，前两个在第一次实验时已经用了
PYTHON
还是先看一下函数返回值的内容
首先需要其他三个账户，这是我注册的信息
接下来首先是EX1A的输出
EX2B
return [OP_0,
 cust1_sig,#理论上这需要三个人来解锁，但是貌似一个人就能成功
 bank_sig]#还需要我自己第一个账户（银行）进行解锁
PYTHON
交易信息
Private key: cVRoenyBCjuCbr97W95QLGmZV37Gjuio55hqegY2iRQMg5WVdZbf
Address: mkGbK4JXT1YKy26pDgjTyoAq8PWBcvBhMA
Private key: cP1vqG29g2ZeeuUZBpgcdfTuQVtesg6FqJ9wXR4qZyHFiprBW7rs
Address: mw8XWCDN7gbKd7SGq2VaJwiPsqbQFq5Kr3
Private key: cP1vqG29g2ZeeuUZBpgcdfTuQVtesg6FqJ9wXR4qZyHFiprBW7rs
Address: mw8XWCDN7gbKd7SGq2VaJwiPsqbQFq5Kr3
201 Created
{
 "tx": {
 "block_height": -1,
 "block_index": -1,
 "hash":
"1b9459aec1d4c9e4d3529cb9ee2470262af911665d3115bfa983ad53b4d9d1b6",
 "addresses": [
 "mypxELiC9GaRWGMfAN4Z6R1KuQUYYPorDr",
 "zLk4xUAxFGWGL1N2sRWDmgSixLEZ3XTt1v"
 ],
 "total": 7656,
 "fees": 60001,
 "size": 307,
 "vsize": 307,
 "preference": "high",
 "relayed_by": "2001:250:401:6545:25e5:20cc:d93d:a8d9",
 "received": "2022-10-24T10:08:47.839025924Z",
 "ver": 1,
 "double_spend": false,
然后是EX2B的输出
 "vin_sz": 1,
 "vout_sz": 1,
 "confirmations": 0,
 "inputs": [
 {
 "prev_hash":
"445aba232e61ac913f1c24c29f2c5eb19bcc87ff81ae5d03260842a753de0736",
 "output_index": 2,
 "script":
"483045022100b599cafb1bd5d5355b6a9d5b89d8f038eaf6da6a377fb4dee7a317be4995d83e0
22026f4db9269b2060305968deb2ea3989723354977450ba745a9f467b458b266af012103f67ec
a8c6ab04112e58b2d9ff24fa0639a716a81b39d3a5719b7afd47d81c342",
 "output_value": 67657,
 "sequence": 4294967295,
 "addresses": [
 "mypxELiC9GaRWGMfAN4Z6R1KuQUYYPorDr"
 ],
 "script_type": "pay-to-pubkey-hash",
 "age": 2350395
 }
 ],
 "outputs": [
 {
 "value": 7656,
 "script":
"2103f67eca8c6ab04112e58b2d9ff24fa0639a716a81b39d3a5719b7afd47d81c342ad512103e
6f0545dee260054a696106afd82a23998e8a70ef2b346c424844c28474a41a82103891b5bd5180
46b8a108c3b5eb6cd0df64c9c711e1dcedcf2a8e3332385710b1c2103891b5bd518046b8a108c3
b5eb6cd0df64c9c711e1dcedcf2a8e3332385710b1c53ae",
 "addresses": [
 "zLk4xUAxFGWGL1N2sRWDmgSixLEZ3XTt1v"
 ],
 "script_type": "pay-to-multi-pubkey-hash"
 }
 ]
 }
}
201 Created
{
 "tx": {
 "block_height": -1,
 "block_index": -1,
 "hash":
"4dffcc2fa4cd398703bf5d937453a49f87e4fb4b8c5c839aba08cd54432babb6",
 "addresses": [
 "zLk4xUAxFGWGL1N2sRWDmgSixLEZ3XTt1v",
 "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
 ],
 "total": 5,
 "fees": 7651,
 "size": 231,
 "vsize": 231,
 "preference": "low",
 "relayed_by": "2001:250:401:6545:25e5:20cc:d93d:a8d9",
 "received": "2022-10-24T10:11:14.451444552Z",
 "ver": 1,
 "double_spend": false,
 "vin_sz": 1,
 "vout_sz": 1,
 "confirmations": 0,
 "inputs": [
 {
 "prev_hash":
"1b9459aec1d4c9e4d3529cb9ee2470262af911665d3115bfa983ad53b4d9d1b6",
 "output_index": 0,
 "script":
"00473044022013868dfe3923836b2bbbd976fb95e4d7426b96b37680faa11634d1ecaa2cc4f40
2202aad51dcd888c16c4fd29f866777d96c72a7c0dc717f46b7a22d7555a9b9b7e601483045022
100d7327fbeed55421e3f1b68d26815afeb5ddd922e68af47a28d3b432bda5508390220672f145
da5458429415fef001e35dcfb1302e00e07d12748c0103804ddfc9c6601",
 "output_value": 7656,
 "sequence": 4294967295,
 "addresses": [
 "zLk4xUAxFGWGL1N2sRWDmgSixLEZ3XTt1v"
 ],
 "script_type": "pay-to-multi-pubkey-hash",
 "age": 0
 }
 ],
 "outputs": [
 {
 "value": 5,
 "script": "76a9149f9a7abd600c0caa03983a77c8c3df8e062cb2fa88ac",
两个交易信息已经用黑框标出，可以和上面的HASH进行比对，结果是一样的。
 "addresses": [
 "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
 ],
 "script_type": "pay-to-pubkey-hash"
 }
 ]
 }
}
截图