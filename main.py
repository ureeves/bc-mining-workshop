import os
import git
import stat
import json


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


if __name__ == "__main__":
    path = "cloned"
    create_dir_ifnexists(path)
    delete_dir_contents(path)

    json_file = open("repos.json", "r")
    repos = json.load(json_file)
    json_file.close()

    user_names = []
    repo_names = []
    g = git.Git(path)

    # clone repositories and build lists of user names and repo names
    for repo in repos:
        split = repo.rsplit('/', 1)
        repo_name = split[1]
        user_name = split[0].rsplit('/', 1)[1]

        user_names.append(user_name)
        repo_names.append(repo_name)

        g.clone(repo)
        print(user_name, repo_name, sep=" --> ")
