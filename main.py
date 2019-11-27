import os
import git
import stat
import hashlib
import json
import block_pb2
import random
from importlib import import_module


def create_dir_ifnexists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def delete_dir_contents(path):
    if os.path.exists(path) and os.path.isdir(path):
        for f in os.listdir(path):
            fpath = path + "/" + f
            if os.path.isfile(fpath):
                os.chmod(fpath, stat.S_IWRITE)
                os.remove(fpath)
            else:
                delete_dir_contents(fpath)
                os.rmdir(fpath)


def bit_in_array(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] & (1<<shift)) >> shift


def is_difficulty_compliant(binary_bhash: bytes, difficulty: int) -> bool:
    for n in range(difficulty):
        if bit_in_array(binary_bhash, n) != 0:
            return False

    return True


def is_valid_block(
    block: block_pb2.Block,
    params: block_pb2.BlockParams) -> bool:

    bhash = block.hash
    binary_bhash = bytes.fromhex(bhash)

    if not is_difficulty_compliant(binary_bhash, params.difficulty):
        return False

    block.hash = ""
    computed_hash = hashlib.sha256(block.SerializeToString()).hexdigest()
    block.hash = bhash

    if computed_hash != bhash:
        return False

    return True


class Color:
   PURPLE = '\033[95m'
   GREEN = '\033[92m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   END = '\033[0m'


def random_block() -> block_pb2.Block:
    block = block_pb2.Block()

    block.nonce = random.getrandbits(64)
    block.hash = format(random.getrandbits(256), 'x')
    block.prev_hash = format(random.getrandbits(256), 'x')
    block.tx_root = format(random.getrandbits(256), 'x')

    return block

if __name__ == "__main__":

    path = "cloned"
    create_dir_ifnexists(path)
    delete_dir_contents(path)

    json_file = open("repos.json", "r")
    repos = json.load(json_file)
    json_file.close()

    # clone repositories and make a list of user and module names
    user_module_list = []
    for repo in repos:
        split = repo.rsplit('/', 1)
        repo_name = split[1]
        user_name = split[0].rsplit('/', 1)[1]

        cpath = path + "/" + user_name + "/" + repo_name
        mpath = path + "." + user_name + "." + repo_name + ".main"

        user_module_list.append((user_name, mpath))

        git.repo.base.Repo.clone_from(repo, cpath)
        print(user_name, repo_name, sep=" --> ")

    # define the difficulty at which to test
    params = block_pb2.BlockParams()
    params.difficulty = 20

    # test the mining algorithm implementations
    for (user_name, module_name) in user_module_list:
        try:
            print("===========", Color.BOLD + user_name + Color.END, "===========")

            mod = import_module(module_name)
            block = random_block()
            block = mod.hash_block(block, params)

            if is_valid_block(block, params):
                print(Color.GREEN + "Pass" + Color.END)
            else:
                print(Color.RED + "Fail" + Color.END)

        except Exception as e:
            print(Color.PURPLE + "Error:" + Color.END, e)
