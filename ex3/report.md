下面对每个参数进行说明
OP_2DUP 表示两个操作数
OP_ADD 表示相加
xxxx是我的学号前四位
OP_EQUALVERIFY表示比较是否相等
OP_SUB表示相减
xxx为我的学号后三位xxx
OP_EQUAL输出结果为TRUE
那么整体过程如下：
在我们在b中填写的x和y进行压栈，复制xy（OP_2DUP——两个操作数），然后取出栈顶的x和y相加
（OP_ADD）和xxxx比较（OP_EQUALVERIFY），相等的话就会把true压入栈中，继续验证我的学
号的后三位，如果不等会报错并把false压入栈中。然后就是把x和y相减（OP_SUB）和xxx比较
（OP_EQUALVERIFY），相等返回true。
这里的1019和993就是我们的x和y,x+y=xxxx,x-y=xxx
填写代码以及注释说明
EX3A
ex3a_txout_scriptPubKey = [OP_2DUP, OP_ADD, xxxx, OP_EQUALVERIFY, OP_SUB, xxx,
OP_EQUAL]
PYTHON
EX3B
txin_scriptSig = [xxxx, xxx]
PYTHON
交易的输出
EX3A
201 Created
{
 "tx": {
 "block_height": -1,
 "block_index": -1,
 "hash":
"7c3bc1d4260a8d99f9d468ef0997938e99ec25b01901c9756e8ab5fc781dae71",
 "addresses": [
 "mypxELiC9GaRWGMfAN4Z6R1KuQUYYPorDr"
 ],
 "total": 7656,
 "fees": 60001,
 "size": 176,
 "vsize": 176,
 "preference": "high",
 "relayed_by": "2001:250:401:6554:98fc:7230:2e2a:1b6b",
 "received": "2022-11-03T14:29:44.562093571Z",
 "ver": 1,
 "double_spend": false,
 "vin_sz": 1,
 "vout_sz": 1,
 "confirmations": 0,
 "inputs": [
 {
 "prev_hash":
"445aba232e61ac913f1c24c29f2c5eb19bcc87ff81ae5d03260842a753de0736",
 "output_index": 6,
 "script":
"4730440220543379c70347874f1148c7b885113539f938532aaf78516561526336db64ebcd022
00420a9349d8838b352848fe5f646cd728910d1e5d4c96fbbb9dc999cf516f481012103f67eca8
c6ab04112e58b2d9ff24fa0639a716a81b39d3a5719b7afd47d81c342",
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
 "script": "6e9302dc078894011a87",
 "addresses": null,
 "script_type": "unknown"
 }
 ]
 }
}
EX3B
201 Created
{
 "tx": {
 "block_height": -1,
 "block_index": -1,
 "hash":
"19428382f9de088bbf925475898d12615386a0591233fec9356dd80f32ad023c",
 "addresses": [
 "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
 ],
 "total": 7,
 "fees": 7649,
 "size": 91,
 "vsize": 91,
 "preference": "medium",
 "relayed_by": "2001:250:401:6554:98fc:7230:2e2a:1b6b",
 "received": "2022-11-03T14:30:51.067137291Z",
 "ver": 1,
 "double_spend": false,
 "vin_sz": 1,
 "vout_sz": 1,
 "confirmations": 0,
 "inputs": [
 {
 "prev_hash":
"7c3bc1d4260a8d99f9d468ef0997938e99ec25b01901c9756e8ab5fc781dae71",
 "output_index": 0,
 "script": "02fb0302e103",
 "output_value": 7656,
 "sequence": 4294967295,
 "script_type": "unknown",
 "age": 0
 }
 ],
 "outputs": [
 {
 "value": 7,
 "script": "76a9149f9a7abd600c0caa03983a77c8c3df8e062cb2fa88ac",
 "addresses": [
 "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
 ],
 "script_type": "pay-to-pubkey-hash"
 }
 ]
 }
}
截图验证
EX3A
EX3B