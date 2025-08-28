#!/usr/bin/python3

# gitcheck - seal's git repo update checker
# (C) Seal Sealy, 2025

# KEEP THIS IN SYNC WITH THE VERSION OF THE SPEC WE CONFORM TO
specversion = '1.0'

import subprocess
import sys
import os

def usage():
	print(f'Usage: {sys.argv[0]} knowngit.txt currentver.txt', file=sys.stderr)
	print(f'This GitCheck conforms with the GitCheck File Format Specification Version {specversion}.', file=sys.stderr)
	sys.exit(1)

if len(sys.argv) != 3:
	usage()

repos = {}
notifs = {}
print('Parsing known Git repos...')
with open(sys.argv[1], 'r') as f:
	for line in f:
		tmp = line.split(' ')
		if tmp[0] == 'rem':
			continue
		elif tmp[0] == 'ntf':
			if len(tmp) < 5:
				print(f'Error: malformed knowngit.txt: expected 4 or more parameters in ntf directive, {len(tmp) - 1} received', file=sys.stderr)
				sys.exit(1)
			if tmp[2] != 'y' and tmp[2] != 'n':
				print(f'Error: malformed knowngit.txt: ntf directive "beep" parameter isn\'t y or n, it\'s {tmp[2]}', file=sys.stderr)
				sys.exit(1)
			if tmp[1] not in notifs:
				notifs[tmp[1]] = []
			notifs[tmp[1]].append([tmp[2], tmp[3], ' '.join(tmp[4:]).strip('\n')])
		elif tmp[0] == 'rpo':
			if len(tmp) != 3:
				print(f'Error: malformed knowngit.txt: invalid amount of parameters in rpo directive: 2 expected, {len(tmp) - 1} received', file=sys.stderr)
				sys.exit(1)
			if tmp[1] not in notifs:
				notifs[tmp[1]] = []
			repos[tmp[1]] = tmp[2].strip('\n')
		elif tmp[0] == 'cmt':
			print('Error: malformed knowngit.txt: cmt directive in file', file=sys.stderr)
			sys.exit(1)
		else:
			print(f'Error: malformed knowngit.txt: unknown directive {tmp[0]} in file', file=sys.stderr)
			sys.exit(1)

for repo in notifs.keys():
	if repo not in repos:
		print(f'Error: malformed knowngit.txt: unknown repo {repo} in ntf directive', file=sys.stderr)
		sys.exit(1)

print('Parsing requested Git repos...')
# this WILL overwrite the old gitcheck-upd.txt
# yes, this is intentional
outfile = open("gitcheck-upd.txt", "w")
with open(sys.argv[2], 'r') as f:
	for line in f:
		tmp = line.split(' ')
		if tmp[0] == 'rem':
			continue
		elif tmp[0] == 'ntf':
			print(f'Error: malformed currentver.txt: ntf directive in file', file=sys.stderr)
			sys.exit(1)
		elif tmp[0] == 'rpo':
			print(f'Error: malformed currentver.txt: rpo directive in file', file=sys.stderr)
			sys.exit(1)
		elif tmp[0] == 'cmt':
			if len(tmp) != 3:
				print('Error: malformed currentver.txt: invalid amount of parameters in cmt directive: 2 expected, {len(tmp) - 1} received', file=sys.stderr)
				sys.exit(1)
			reponame = tmp[1]
			commitid = tmp[2].strip('\n')

			if reponame not in repos:
				print(f'Error: unknown repo {reponame}. Please contact seal331.', file=sys.stderr)
				sys.exit(1)

			newver = subprocess.check_output(['git', 'ls-remote', repos[reponame], 'HEAD'])

			newver = newver.split(b'\t')[0].decode('utf-8')

			if commitid != newver:
				if len(notifs[reponame]) != 0:
					for notif in notifs[reponame]:
						if notif[0] == 'y' and sys.stdout.isatty():
							print('\a', end='')
						print(f'Notification from {notif[1]} for {reponame}: {notif[2]}')
				print(f'Update available for {reponame}: {commitid[:6]} -> {newver[:6]}')
				outfile.write(f'Update available for {reponame}: {commitid[:6]} -> {newver[:6]}')
		else:
			print(f'Error: malformed currentver.txt: unknown directive {tmp[0]}', file=sys.stderr)
			sys.exit(1)

outfile.close()
print('Done.')
