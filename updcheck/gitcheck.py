#!/usr/bin/python3

# gitcheck - seal's git repo update checker
# (C) Seal Sealy, 2025

DEBUG = 0

import subprocess
import sys
import os

def usage():
	print(f'Usage: {sys.argv[0]} knowngit.txt currentver.txt', file=sys.stderr)
	sys.exit(1)

if len(sys.argv) != 3:
	usage()

repos = {}
print('Parsing known Git repos...')
with open(sys.argv[1], 'r') as f:
	for line in f:
		tmp = line.split(' ')
		repos[tmp[0]] = tmp[1].strip()

print('Parsing requested Git repos...')
with open(sys.argv[2], 'r') as f:
	for line in f:
		tmp = line.split(' ')
		tmp[1] = tmp[1].strip()

		if tmp[0] not in repos:
			print(f'Error: unknown repo {tmp[0]}. Please contact seal331.', file=sys.stderr)
			sys.exit(1)

		newver = subprocess.check_output(['git', 'ls-remote', repos[tmp[0]], 'HEAD'])
		if DEBUG:
			print(tmp[0], tmp[1], newver.split(b'\t')[0].decode('utf-8'))

		newver = newver.split(b'\t')[0].decode('utf-8')
		if tmp[1] != newver:
			print(f'Update available for {tmp[0]}: {tmp[1][:6]} -> {newver[:6]}')
			os.system(f'echo "Update available for {tmp[0]}: {tmp[1][:6]} -> {newver[:6]}" >> gitcheck-upd.txt')

print('Done.')
