# Aleo Delegation Guide

[Aleo](https://aleo.org) is a L1 smart contract blockchain focused on enabling and building private decentralized applications using zero-knowledge. It's built on SnarkOS and SnarkVM allowing for single proof of execution validations and a private environment that processes transactions at scale making verifiable proofs the only onchain requirement.

Staking to the Coinbase validator contributes to the protocol consensus and as a result, stakers earn a proportionate amount of inflationary rewards provided to the validator they stake with.

| Protocol Parameter | Value                                         |
| :----------------- | :-------------------------------------------- |
| Minimum to stake   | 10,000 Aleo                                   |
| Warm-up period     | 1–2 blocks and rewards compound automatically |
| Cooldown period    | 360 blocks (approximately 1 hour)             |
| Service fee        | 10% of rewards¹                               |

<Info>
  **COINBASE VALIDATOR INFORMATION**

  Name: `Coinbase 1`\
  Validator Information: aleo1m5vc6da037erge36scdmefk0dcnrjk9tu04zyedfvxunwcwd3vxqtcy7ln\
  Validator URL: [https://aleoscan.io/address?a=aleo1m5vc6da037erge36scdmefk0dcnrjk9tu04zyedfvxunwcwd3vxqtcy7ln](https://aleoscan.io/address?a=aleo1m5vc6da037erge36scdmefk0dcnrjk9tu04zyedfvxunwcwd3vxqtcy7ln)

  Name: `Coinbase 2`\
  Validator Information: aleo1vfukg8ky2mhfprw63s0k0hl4vvd8573s6fkn8cv9y0ca6q27eq8qwdnxls\
  Validator URL: [https://aleoscan.io/address?a=aleo1vfukg8ky2mhfprw63s0k0hl4vvd8573s6fkn8cv9y0ca6q27eq8qwdnxls](https://aleoscan.io/address?a=aleo1vfukg8ky2mhfprw63s0k0hl4vvd8573s6fkn8cv9y0ca6q27eq8qwdnxls)

  Name: `Coinbase 3`\
  Validator Information: aleo1hdtsgk52nsualvrt4t676m9sydp6zllwe0mr4w5mzknxj3rkzs8slhszhs\
  Validator URL: [https://aleoscan.io/address?a=aleo1hdtsgk52nsualvrt4t676m9sydp6zllwe0mr4w5mzknxj3rkzs8slhszhs](https://aleoscan.io/address?a=aleo1hdtsgk52nsualvrt4t676m9sydp6zllwe0mr4w5mzknxj3rkzs8slhszhs)
</Info>

<Warning>
  **Service fee**\
  ¹Coinbase may change its service fee during the lifetime of this validator (e.g., increasing fees as total delegation increases to ensure we are never running an outsized portion of the network on our node).
</Warning>

