#!/usr/bin/python3

# gitcheck - seal's git repo update checker
# (C) Seal Sealy, 2025

# KEEP THIS IN SYNC WITH THE VERSION OF THE SPEC WE CONFORM TO
specversion = '1.1.1'

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
# the architecture of updcheck doesn't allow you to put an int into this
# variable with a malformed mde directive, therefore use an int to avoid giving
# the user the wrong error in obscure corner cases that look more like
# intentional misuse, but anyway
mode = 13371337
antiabusemodenum = 'NERPA'
supportedmodes = ['normal', 'antiabuse_standard', 'antiabuse_silent', 'silent']
print('Parsing known Git repos...')
with open(sys.argv[1], 'r') as f:
	for line in f:
		tmp = line.split(' ')
		# hack for unknown/malformed directives alone on line
		tmp[0] = tmp[0].strip('\n')
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
		elif tmp[0] == 'mde':
			if mode != 13371337:
				print(f'Error: malformed knowngit.txt: multiple mde directives', file=sys.stderr)
				sys.exit(1)
			if len(tmp) < 2:
				print(f'Error: malformed knowngit.txt: mde directive with no parameters', file=sys.stderr)
				sys.exit(1)
			mode_to_be_set = tmp[1].strip('\n')
			if mode_to_be_set not in supportedmodes:
				print(f'Error: malformed knowngit.txt: unsupported mode in mde directive, see specification', file=sys.stderr)
				sys.exit(1)
			argcount = 2
			if mode_to_be_set == 'antiabuse_standard' or mode_to_be_set == 'antiabuse_silent':
				argcount = 3
			if len(tmp) != argcount:
				print(f'Error: malformed knowngit.txt: invalid amount of parameters in mde directive, {argcount - 1} expected, {len(tmp) - 1} received', file=sys.stderr)
				sys.exit(1)
			mode = mode_to_be_set
			if mode_to_be_set == 'antiabuse_standard' or mode_to_be_set == 'antiabuse_silent':
				try:
					int(tmp[2])
				except ValueError:
					print(f'Error: malformed knowngit.txt: ValueError encountered converting num parameter to an integer, are you sure you passed an integer?', file=sys.stderr)
					sys.exit(1)
				if int(tmp[2]) < 0:
					print(f'Error: malformed knowngit.txt: mde directive num parameter less than 0', file=sys.stderr)
					sys.exit(1)
				antiabusemodenum = int(tmp[2])
		else:
			print(f'Error: malformed knowngit.txt: unknown directive {tmp[0]} in file', file=sys.stderr)
			sys.exit(1)

if len(repos) == 0:
	print(f'Error: malformed knowngit.txt: no rpo directives specified', file=sys.stderr)
	sys.exit(1)

if mode == 13371337:
	print(f'Error: malformed knowngit.txt: no mde directive specified', file=sys.stderr)
	sys.exit(1)

if (mode == 'antiabuse_standard' or mode == 'antiabuse_silent') and antiabusemodenum == 'NERPA':
	print(f'Error: internal error: mode is an antiabuse variant and antiabusemodenum is still unset for some reason, contact seal331', file=sys.stderr)
	sys.exit(1)

for repo in notifs.keys():
	if repo not in repos:
		print(f'Error: malformed knowngit.txt: unknown repo {repo} in ntf directive', file=sys.stderr)
		sys.exit(1)

if mode == 'antiabuse_standard':
	beeps_scheduled = 0
	for key, value in notifs.items():
		for midlevellist in value:
			for bottomlevellist in midlevellist:
				if bottomlevellist[0] == 'y':
					beeps_scheduled += 1

	if beeps_scheduled > antiabusemodenum:
		print(f'Error: anti-abuse protection violation: {antiabusemodenum} beeps allowed, {beeps_scheduled} beeps scheduled', file=sys.stderr)
		sys.exit(1)

# we have to suffer with all this range(len(thing)) hackery because unlike in
# the last loop we actually may need to modify this one
if mode == 'antiabuse_silent':
	beeps_scheduled = 0
	for key, value in notifs.items():
		for midlevellist in range(len(value)):
			if value[midlevellist][0] == 'y':
				if beeps_scheduled >= antiabusemodenum:
					value[midlevellist][0] = 'n'
					notifs[key] = value
				else:
					beeps_scheduled += 1

print('Parsing requested Git repos...')
# verification pass
cmtamount = 0
with open(sys.argv[2], 'r') as f_verify:
	for line in f_verify:
		tmp = line.split(' ')
		if tmp[0] == 'rem':
			continue
		elif tmp[0] == 'ntf':
			print(f'Error: malformed currentver.txt: ntf directive in file', file=sys.stderr)
			sys.exit(1)
		elif tmp[0] == 'rpo':
			print(f'Error: malformed currentver.txt: rpo directive in file', file=sys.stderr)
			sys.exit(1)
		elif tmp[0] == 'mde':
			print(f'Error: malformed currentver.txt: mde directive in file', file=sys.stderr)
			sys.exit(1)
		elif tmp[0] == 'cmt':
			if len(tmp) != 3:
				print(f'Error: malformed currentver.txt: invalid amount of parameters in cmt directive: 2 expected, {len(tmp) - 1} received', file=sys.stderr)
				sys.exit(1)
			reponame = tmp[1]
			if reponame not in repos:
				print(f'Error: unknown repo {reponame}. Please contact seal331.', file=sys.stderr)
				sys.exit(1)
			cmtamount += 1
		else:
			print(f'Error: malformed currentver.txt: unknown directive {tmp[0]}', file=sys.stderr)
			sys.exit(1)

if cmtamount == 0:
        print(f'Error: malformed currentver.txt: no cmt directives specified', file=sys.stderr)
        sys.exit(1)

# this WILL overwrite the old gitcheck-upd.txt
# yes, this is intentional
outfile = open("gitcheck-upd.txt", "w")
# no error handling in this loop anymore, all that got moved to the verification
# pass above
# if there's somehow an error that got past the verification pass -
# WE'RE IN BIG TROUBLE
with open(sys.argv[2], 'r') as f:
	for line in f:
		tmp = line.split(' ')
		if tmp[0] == 'cmt':
			reponame = tmp[1]
			commitid = tmp[2].strip('\n')

			newver = subprocess.check_output(['git', 'ls-remote', repos[reponame], 'HEAD'])

			newver = newver.split(b'\t')[0].decode('utf-8')

			if commitid != newver:
				if len(notifs[reponame]) != 0:
					for notif in notifs[reponame]:
						if notif[0] == 'y' and sys.stdout.isatty() and (not (mode == 'silent')):
							print('\a', end='')
						print(f'Notification from {notif[1]} for {reponame}: {notif[2]}')
				print(f'Update available for {reponame}: {commitid[:6]} -> {newver[:6]}')
				outfile.write(f'Update available for {reponame}: {commitid[:6]} -> {newver[:6]}')

outfile.close()
print('Done.')
