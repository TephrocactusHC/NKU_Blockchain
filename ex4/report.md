区块链ex4实验报告
2012026穆禹宸 2011831夏楝然
1.解释代码内容，以及 coinExchangeScript如何工作
def coinExchangeScript(public_key_sender, public_key_recipient, hash_of_secret):
 return [
 # fill this in!
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
PYTHON
实验原理图:
还需要注意的是，在 alice.py 和 bob.py 文件中赎回函数和交换函数中都使用到了 GetTxid()函数，并使用 b2x()函数将其进行 格式的转换，但是由于网络
编址大小端的问题，所以使得最终得到的 transactionid 不匹配，无法交易。将此函数改为b2lx()将大小端问题解决，顺利运行代码。
只有当 Bob 将 TX2 签名后，Alice 才会公布 TX3。Alice将把交换钱的操作写在了存储A中，该交易可以通过双方的签名或Bob签名和秘密将钱取出; 如果
Bob不在再融资A上签名, Alice不公开存储A, 保证两个时间单位过去后，存款还没有被领取，她可以赎回她的存款.如果Bob在再融资A上签名,但交易不进行,
即Bob 不把钱赎回来,那么两个时间单位过去后，存款还没有被领取，她可以赎回她的存款.
2.以 Alice 用 coinExchangeScript 向 Bob 发送硬币为例：如果 Bob 不把钱赎回来，Alice 为什么总能拿回
她的钱？
如果 Bob 不把钱赎回来，Alice 为什么总能拿回她的钱？
为什么不能用简单的 1/2 multisig 来解决这个问题？
由于最初始的模型建立中就将交换货币的两方视为不可信的，如果使用了1/2 multisig，可以利用任何一个人的签名将钱赎回，可能会发生赎回连续赎回自
己发出的钱和对方发送的钱的问题.
1. Alice选择一个随机字符串x,计算其哈希值
2. Alice创建存储A，将钱输入；但未广播
3. Alice创建再融资A，为自己可以将钱赎回的交易，将该交易广播到网络上,其交易有48小时的锁定时间，让Bob有足够的时间去兑换存储A中的钱
4. Bob对再融资A进行签名，Alice获得了Bob的签名，便将存储A广播
5. Bob创建存储B，将钱输入；此时未广播.
6. Bob创建再融资B，为自己可以将钱赎回的交易，将该交易广播到网络上；该交易有24小时的锁定时间，让Alice有足够的时间去兑换存储B中的钱
7. Alice对再融资B进行签名，Bob获得了Alice的签名，将存储B广播到网络上
8. Alice利用自己的签名和秘密对存储B中的钱进行赎回，一旦赎回，秘密x便广播
9. Bob拿到了秘密x，利用自己的签名和秘密将存储A中的钱赎回,交易完成
10. 如果双方不赎回，超过设定小时后可以将自己的钱通过双方的签名拿回
4)中Alice将存储A公布到了网络上，发生了资金流转，此时钱不属于任何人；
7)中 Bob将存储B公布到了网络上，发生了资金流转，此时钱不属于任何人；
8)中Alice利用秘密x和签名A将存储B中的钱赎回到自己的地址中，发生资金流动，Bob的钱到了Alice手中；
9)中 Bob利用秘密x和签名B将存储A中的钱赎回到自己的地址中，发生资金流动，Alice的钱到了Bob手中，一次成功的跨链原子交换完成。
所使用的账户信息如下所示：
btc
token
bcy
3.解释 Alice (Bob) 创建的一些交易内容和先后次序，以及背后的设计原理。
4.本次作业中，一次成功的跨链原子交换中，资金是如何流转的
5.实验结果
Alice
Private key: cSrgj3nTUvPDUCAFoLMqYNspaYiogjJs5PaA2fSFWyrqCVwZ9cpL
Address: mypxELiC9GaRWGMfAN4Z6R1KuQUYYPorDr
9853dc71aa4e107f5a38f494d9a9a5a77c55affbc4513fa8b7924fd5928d85ef
Bob
Private key: cW9wKQUqt5mH6KvusfCwdzL9BedBHEkCvXVbWdKSHxovixfJEbcE
Address: n2HPJf8kDPSnEAyeKzLNBxkMfk3RESGfsF
a6e4540ff5998788654ace194368ba54a873a970f766e6ce6cc3c1e0e7906b46
token
alice
Token 76cee1ed3c9b4e6aa021f8e01188bdc9
bob
Token b99fc91632a54040a7c1f2b8092fbef4
alice
{
 "private": "0af98ccef7c16a7d5deed650efeba2859255f40cd33b6854f18d7eb78a80c2fd",
 "public": "02d8bc58354405ec3fe6045894688fbad84b281d7fd1038f857790eecba6e7dec1",
txid_to_spend
 "address": "C9ybksHoqvxdZ4iFYmt1fVm4rpMwnJitw4",
 "wif": "BohN5y2GaWhDX5KYjjHQi7sFpMNgTkw8fcVDR3JrhV9jf9N2c9sJ"
}
bob
{
 "private": "c9751710788a24008f8fea6f11229749f307bea84f2b08e70173a5f459b738b3",
 "public": "0264daac5800b1ce8806a0184a416c6af82b32a876b98ed5186f4a32e9c935081e",
 "address": "CGNfUxki6Mj28N5eycVTALqCZKwt4BjJky",
 "wif": "Bv5dw9erqoUuTNv6MBQFVUF2S3a4Bx1b4r2ypcgUshK89xUGSfRL"
}
alice
c19e590d49cbcd6c0822809d7cc17f0fe92431b4a2875ea34d9518ead8cdb96a
bob
{
 "tx_ref": "af412981894bfa66c9e784703fb53fc3e7af5e7f6e70ff072849db6180863044"
}
最终的交易输出
Alice swap tx (BTC) created successfully!
201 Created
{
 "tx": {
 "block_height": -1,
 "block_index": -1,
 "hash": "5f741528c6ce9e0efb5df3f1a4dd7d55040b158c2534e4d10dafa38e6793aa34",
 "addresses": [
 "mypxELiC9GaRWGMfAN4Z6R1KuQUYYPorDr"
 ],
 "total": 1050585,
 "fees": 100000,
 "size": 266,
 "vsize": 266,
 "preference": "high",
 "relayed_by": "2001:250:401:6554:2440:5517:f3ca:6229",
 "received": "2022-12-02T10:36:02.47123685Z",
 "ver": 1,
 "double_spend": false,
 "vin_sz": 1,
 "vout_sz": 1,
 "confirmations": 0,
 "inputs": [
 {
 "prev_hash": "c19e590d49cbcd6c0822809d7cc17f0fe92431b4a2875ea34d9518ead8cdb96a",
 "output_index": 0,
 "script":
"4830450221008b2ed3a700b230a9ea515c06e0e435809f72959750a854b54d16a2425ceb512b022039f7c09f476490d19afe0dceaec2c80bff93
675bb2d67877f70c2e190e579fcf012103f67eca8c6ab04112e58b2d9ff24fa0639a716a81b39d3a5719b7afd47d81c342",
 "output_value": 1150585,
 "sequence": 4294967295,
 "addresses": [
 "mypxELiC9GaRWGMfAN4Z6R1KuQUYYPorDr"
 ],
 "script_type": "pay-to-pubkey-hash",
 "age": 2349919
 }
 ],
 "outputs": [
 {
 "value": 1050585,
 "script":
"21039a06ed497a075b86f181ee14b05b30f61f9b2f4a10e0816a14052f3274336990ad762103f67eca8c6ab04112e58b2d9ff24fa0639a716a81
b39d3a5719b7afd47d81c342ac63755167a914853b775079232503df966e626618e1d388a957208768",
 "addresses": null,
 "script_type": "unknown"
 }
 ]
 }
}
Bob swap tx (BCY) created successfully!
201 Created
{
 "tx": {
 "block_height": -1,
 "block_index": -1,
 "hash": "59e33ce64833d1faaa42598811585d426854b07cbd54d99d8486b0e8d175f5a6",
 "addresses": [
 "CGNfUxki6Mj28N5eycVTALqCZKwt4BjJky"
 ],
 "total": 900000,
 "fees": 100000,
 "size": 266,
 "vsize": 266,
 "preference": "high",
 "relayed_by": "2001:250:401:6554:2440:5517:f3ca:6229",
 "received": "2022-12-02T10:36:02.878079071Z",
 "ver": 1,
 "double_spend": false,
 "vin_sz": 1,
 "vout_sz": 1,
 "confirmations": 0,
 "inputs": [
 {
 "prev_hash": "af412981894bfa66c9e784703fb53fc3e7af5e7f6e70ff072849db6180863044",
 "output_index": 0,
 "script":
"483045022100a2ef3bd466aab9da1a6e82ed0c400f48b14e691c4e2e0023648318ee363bf531022049defb1a978ed3ff8526cc8577c8a606be5e
aaf7d3aa7e1d97ae5c3c5b743cfb01210264daac5800b1ce8806a0184a416c6af82b32a876b98ed5186f4a32e9c935081e",
 "output_value": 1000000,
 "sequence": 4294967295,
 "addresses": [
 "CGNfUxki6Mj28N5eycVTALqCZKwt4BjJky"
 ],
 "script_type": "pay-to-pubkey-hash",
 "age": 570563
 }
 ],
 "outputs": [
 {
 "value": 900000,
 "script":
"2102d8bc58354405ec3fe6045894688fbad84b281d7fd1038f857790eecba6e7dec1ad76210264daac5800b1ce8806a0184a416c6af82b32a876
b98ed5186f4a32e9c935081eac63755167a914853b775079232503df966e626618e1d388a957208768",
 "addresses": null,
 "script_type": "unknown"
 }
 ]
 }
}
Sleeping for 20 minutes to let transactions confirm...
Alice redeem from swap tx (BCY) created successfully!
201 Created
{
 "tx": {
 "block_height": -1,
 "block_index": -1,
 "hash": "e84791ac98806c63f64839c1ec9b0d2b5fead26e793dc0749166bd390fc5565d",
 "addresses": [
 "C9ybksHoqvxdZ4iFYmt1fVm4rpMwnJitw4"
 ],
 "total": 800000,
 "fees": 100000,
 "size": 182,
 "vsize": 182,
 "preference": "high",
 "relayed_by": "2001:250:401:6554:2440:5517:f3ca:6229",
 "received": "2022-12-02T10:56:03.292193868Z",
 "ver": 1,
 "double_spend": false,
 "vin_sz": 1,
 "vout_sz": 1,
 "confirmations": 0,
 "inputs": [
 {
 "prev_hash": "59e33ce64833d1faaa42598811585d426854b07cbd54d99d8486b0e8d175f5a6",
 "output_index": 0,
 "script":
"187468697349734153656372657450617373776f72643132334730440220030dcedc90af7b56543b90555c1cd36a64bf38f7948bef2c9a44796c
e34686530220101851433f79e7954430faad11c3b5ccc5e5c10ef481849d0621eda27e84c2fb01",
 "output_value": 900000,
 "sequence": 4294967295,
 "script_type": "unknown",
 "age": 570701
 }
 ],
 "outputs": [
 {
 "value": 800000,
 "script": "76a914b8d590349a6282170301992b13ae708052d2900988ac",
 "addresses": [
 "C9ybksHoqvxdZ4iFYmt1fVm4rpMwnJitw4"
 ],
 "script_type": "pay-to-pubkey-hash"
 }
 ]
 }
}
Bob redeem from swap tx (BTC) created successfully!
201 Created
{
 "tx": {
 "block_height": -1,
 "block_index": -1,
 "hash": "22464b8549a963fb747f884a52a3dd400b11cb2ef9d56ed4c391344b659af4e0",
 "addresses": [
 "n2HPJf8kDPSnEAyeKzLNBxkMfk3RESGfsF"
 ],
 "total": 950585,
 "fees": 100000,
 "size": 183,
 "vsize": 183,
 "preference": "high",
 "relayed_by": "2001:250:401:6554:2440:5517:f3ca:6229",
 "received": "2022-12-02T10:56:04.361888109Z",
 "ver": 1,
 "double_spend": false,
 "vin_sz": 1,
 "vout_sz": 1,
 "confirmations": 0,
 "inputs": [
 {
 "prev_hash": "5f741528c6ce9e0efb5df3f1a4dd7d55040b158c2534e4d10dafa38e6793aa34",
 "output_index": 0,
 "script":
"187468697349734153656372657450617373776f7264313233483045022100f3c6668eca83c51a0c57b402a1504b149edcf3d300beb194f8a8ea
5bcd8b96b8022071f41466a1bf6cacd0363d82bfda0f42da2a593d28412598829e15fccc9a91f001",
 "output_value": 1050585,
 "sequence": 4294967295,
 "script_type": "unknown",
 "age": 2409425
 }
 ],
 "outputs": [
 {
 "value": 950585,
 "script": "76a914e3c9b2157a273f394605e8a071ed3e33f41af94388ac",
 "addresses": [
 "n2HPJf8kDPSnEAyeKzLNBxkMfk3RESGfsF"
 ],
 "script_type": "pay-to-pubkey-hash"
 }
 ]
 }
}
网站截图