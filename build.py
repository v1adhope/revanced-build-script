#!/usr/bin/env python3

import errno
import os
import shlex
import subprocess

import requests

REVANCED_CLI = "https://github.com/ReVanced/revanced-cli/releases/download/v4.6.0/revanced-cli-4.6.0-all.jar"
REVANCED_PATCHES = "https://github.com/ReVanced/revanced-patches/releases/download/v4.17.0/revanced-patches-4.17.0.jar"

APP_LINKS = ("link-to-apk",)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"


def create_dir(name):
    try:
        os.mkdir(name)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e


def get_file(url, path):
    print("=> Downloading {}".format(url))

    with requests.get(url, stream=True, headers={"user-agent": USER_AGENT}) as resp:
        resp.raise_for_status()

        with open(path, "wb") as file:
            for chunk in resp.iter_content(chunk_size=8192):
                file.write(chunk)


def patch_file(cliPath, patchesPath, outPath, appPath):
    print("=> Patching {}".format(appPath))
    cmd = "java -jar {cli} patch -b {patches} -o {out} {app}".format(
        cli=cliPath,
        patches=patchesPath,
        out=outPath,
        app=appPath,
    )

    processed_cmd = subprocess.run(
        args=shlex.split(cmd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if processed_cmd.returncode:
        print(processed_cmd.stdout)
        processed_cmd.check_returncode()


def main():
    create_dir("tools")

    cliPath = "tools/cli.jar"
    patchesPath = "tools/patches.jar"
    get_file(REVANCED_CLI, cliPath)
    get_file(REVANCED_PATCHES, patchesPath)

    create_dir("apps")
    create_dir("patched_apps")

    for i, al in enumerate(APP_LINKS):
        appPath = "apps/app{}.apk".format(i + 1)
        get_file(al, appPath)
        patch_file(
            cliPath=cliPath,
            patchesPath=patchesPath,
            outPath="patched_apps/patched_{}.apk".format(i + 1),
            appPath=appPath,
        )


if __name__ == "__main__":
    main()
