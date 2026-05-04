#!/usr/bin/env python3

import argparse
import json
import os
import re
import requests
import time

entity_pattern = re.compile(r'<!ENTITY\s+(\S+)\s+"([^"]*)">')
ref_pattern = re.compile(r'&(\S+?);')

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--quiet", help="decrease output verbosity", action="store_true")
parser.add_argument("book", help="the book to check")
args = parser.parse_args()

match args.book.lower():
    case "slfs":
        packages_ent_link = "https://raw.githubusercontent.com/glfs-book/slfs/trunk/packages.ent"
    case "glfs":
        packages_ent_link = "https://raw.githubusercontent.com/glfs-book/glfs/trunk/packages.ent"
    case "lfs":
        packages_ent_link = "https://raw.githubusercontent.com/lfs-book/lfs/trunk/packages.ent"
    case "blfs":
        packages_ent_link = "https://raw.githubusercontent.com/lfs-book/blfs/trunk/packages.ent"
    case _:
        print(f"unknown book: {args.book}")
        exit(1)

content = requests.get(packages_ent_link).text
data = json.loads(requests.get("https://raw.githubusercontent.com/tox-wtf/vat/master/p/ALL.json").text)

def parse_ents(haystack):
    return { k.lower(): v for k, v in dict(entity_pattern.findall(haystack)).items() }

def expand_ents(ents):
    resolved = {}
    def resolve(name, stack=None):
        if stack is None:
            stack = set()

        if name in resolved:
            return resolved[name]

        if name in stack:
            raise ValueError(f"Circular reference detected for {name}")

        stack.add(name)
        value = ents[name]

        def replace(match):
            ref = match.group(1)
            if ref not in ents:
                raise KeyError(f"Undefined ent: {ref}")

            return resolve(ref, stack)

        expanded = ref_pattern.sub(replace, value)
        resolved[name] = expanded
        stack.remove(name)

        return expanded

    for name in ents:
        resolve(name)

    return resolved

BUILTIN_ENTS = { "lt": "<", "gt": ">", "amp": "&" }

# Ents used in lfs/packages.ent
# These are defined to avoid errors but we don't care about them
COMPAT_ENTS = {"savannah": "",
               "savannah-nongnu": "",
               "gnu": "",
               "gnu-software": "",
               "github": "",
               "sourceforge": "",
               "pypi-src": "",
               "pypi-home": "",
               "kernel": "",
               "downloads-root": "",
               "anduin-sources": "",
              }

ents = parse_ents(content)
lfs_ents = expand_ents(ents | BUILTIN_ENTS | COMPAT_ENTS)

def lfs_ver(lfs_key_full):
    return lfs_ents[f"{lfs_key_full}"]

def is_commit(string):
    return len(string) == 40

def truncate_commit(string, length):
    if is_commit(string):
        return string[:length]

    return string

def pkg(name, *, key=None, lfs_key=None, lfs_key_full=None, vat_key=None, channel="release", **overrides):
    key = key or name.lower()
    vat_key = vat_key or key
    lfs_key_full = lfs_key_full or (lfs_key+"-version" if lfs_key else key+"-version")

    # FIXME: I think vat default execs non-lazily
    base = {
        "flag": "*",
        "lfs": overrides.get("lfs", lfs_ver(lfs_key_full)),
        "vat": overrides.get("vat", data[vat_key][channel]),
    }

    return { name: base | overrides }

with open(args.book.lower(), "r") as f:
    exec(f.read())

print(f"{'Name':<32}{'LFS':<12}{'VAT':<12}Flag")
print("-" * 60)
for name, data in packages.items():
    lfs = truncate_commit(data["lfs"], 6)
    vat = truncate_commit(data["vat"], 6)

    if lfs == vat:
        if not args.quiet:
            print(f"{name:<32}{lfs:<12}{vat}")
    else:
        print(f"{name:<32}{lfs:<12}{vat:<12}{data['flag']}")
