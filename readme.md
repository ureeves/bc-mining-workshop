# Inhouse Day - Blockchain Workshop

## Objectives
In this workshop we will be coding a blockchain mining algorithm as an
introduction to the base concept of a blockchain - the block.

We will be working in the Python programming language - specifically version
3. Some experience with Python will give you a headstart, however it's not
required.

## Background
Blockchains are, in essence, backwards linked lists where the "link" that
is used to refer to the previous block is the cryptographic hash of that
previous block - replacing the pointers/references you may have used in your
classes.

A blockchain, therefore, looks something like this.

```
_____________     _____________     _____________
|           |     |           |     |           |
| prev_hash |  _--| prev_hash |  _--| prev_hash |
|   hash    |<-   |   hash    |<-   |   hash    |
|           |     |           |     |           |   (...)
|   nonce   |     |   nonce   |     |   nonce   |
|  tx_root  |     |  tx_root  |     |  tx_root  |
|___________|     |___________|     |___________|
```

The first two fields in such a block have already been discussed, however there
are two more fields we still need to cover for this assignement. One of them is
the `tx_root` field.

The `tx_root` field represents the so called merkle-root of our transactions.
For our purposes we'll just look at this as the transactions in our block.

The `nonce` field will be important for us, since it's what miners change,
along with the hash, to prove that they have done work - meaning expended
computational power - to include the block on the chain.

## Proof of Work
To prove that they have done computational work, miners have to find a nonce
such that the hash of the block conforms to the following conditions:

- The hash is the hash of the block without the hash in it (duh)
- The hash has a minimum number `D` of trailing zeros.

`D` is the so called difficulty parameter - the larger it is, the harder it
becomes to find an appropriate nonce. If we represent the hash as a bit string
it will end up looking like this:

```
D = 4

0000101001010100101001000111...
___|

D = 5

0000010100101001010101010101...
____|


```

## Challenge
Your challenge is to code a function that finds an appropriate nonce for an
arbitrary difficulty number.
This nonce is then placed, together with the hash of the block, inside the
structure and the entire structure is then returned.

Don't worry! These structures are already defined in the Block and BlockParams
classes in the [block_pb2.py](block_pb2.py) file in this repository. Copy this
file and import its contents to your workspace. The structures look like this:

```
Block {
    uint64 nonce; // 64-bit integer

    string hash;  // sha256 hex string
    string prev_hash; // sha256 hex string

    string tx_root; // sha256 hex string
}

BlockParams {
    uint64 difficulty; // 64-bit integer
}

```


Start by creating a file name `main.py` in the root of your repository, and
filling it with the following contents:

```python
# main.py

import hashlib # hashes
import block_pb2 # file you should have copied
import random # generate random numbers

# This is so that you can address single bits in an array of bytes
def bit_in_array(data: bytes, num: int):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] & (1<<shift)) >> shift


def is_valid_block(block: block_pb2.Block, params: block_pb2.BlockParams) -> bool:

    # TODO fill this in
    # TIP Remember the difficulty parameter?

    return False


def hash_block(block: block_pb2.Block, params: block_pb2.BlockParams) -> block_pb2.Block:

    while not is_valid_block(block, params):
        # TODO fill this in
        # TIP Generate random nonce and compute the sha256 hash of the block
        # TIP Remember that the hashes are represented in HEX in the block

    return block
```

You'll also need protobuf support. So, in your terminal:

```bash
pip install protobuf
```

It is your job to scour Python's documentation for appropriate functions and
patterns to use.

**Good Luck!**

## Grading
After you've completed (or not) the assignement, give the GitHub URL of your
repository to the supervisor, and he'll be able to put your code through the
test.
