#!/usr/bin/python3

# packagesent2toml - seal's stupid packages.ent to nvchecker toml converter
# (C) Seal Sealy, 2025

MAINTAINER_MODE = 0

import os
import sys
import tomllib

gitstuff = []
TMP_inxi_revision = 'PLCHLDR'

def usage():
	print(f"Usage: {sys.argv[0]} packages.ent", file=sys.stderr)
	sys.exit(1)

if not MAINTAINER_MODE:
	with open("./lfsqol.toml", "rb") as toml:
		normal_pkgs = tomllib.load(toml)
	# [1:] to avoid bringing in __config__
	pkgs = list(normal_pkgs)[1:]
	with open("./lfsqol-git.txt", "r") as f:
		for line in f:
			pkgs.append(line.split(' ')[0])

# seal's ad-hoc purpose-built xml parser
# i'm too stupid to figure out how to use a proper XML parser with this
def parsexml(line):
	global gitstuff, TMP_inxi_revision
	repo = 'arch'
	# check for comments
	if not line.startswith("<!ENTITY "):
		return False
	tmp = line.split(" ")
	tmp = [i for i in tmp if i != '']
	#print(tmp)
	# yes, we really like hacks over here
	pkgname = tmp[1].split("-version")[0]
	version = tmp[2].strip()[1:-2]
	# ALL SPECIAL CASING SHOULD GO HERE

	# seal331 22/05/2025 21:23 MSK: libdatachannel has submodules, we only
	# need the library version itself
	if ('libdatachannel' in pkgname) and (not (pkgname == 'libdatachannel')):
		return False

	# seal331 22/05/2025 21:35 MSK: befunge -minor is for the download link
	if ('befunge-minor' == pkgname):
		return False

	# seal331 22/05/2025 21:38 MSK: idle source code storage is a massive
	# mess, we check it completely separately out of the main process
	# seal331 23/05/2025 3:34 MSK: refactor
	if ('idle-minor' == pkgname):
		with open('idle-currentver', 'w') as file:
			file.write(version[1:])
		return False

	if ('idle' == pkgname):
		return False

	# seal331 22/05/2025 21:41 MSK: lotus123 requires its own binutils
	# build due to obscure system requirements, we don't update it unless
	# upstream does
	if ('lotus123-binutils' == pkgname):
		return False

	# seal331 22/05/2025 21:43 MSK: gkermit has an obscure tarball name
	# which is stored in packages.ent despite not being a version
	if ('gkermit-tarball' == pkgname):
		return False

	# seal331 22/05/2025 21:44 MSK: obs-cef is a component of OBS
	if ('obs-cef' == pkgname):
		return False

	# seal331 22/05/2025 21:46 MSK: cuda-nvidia is not a package itself
	if ('cuda-nvidia' == pkgname):
		return False

	# seal331 22/05/2025 21:48 MSK: gnat-binary is tied to GCC, imo I'd
	# rather check the GCC version than parse this
	if ('gnat-binary' == pkgname):
		return False

	# seal331 22/05/2025 21:50 MSK: LFS-QOL intentionally ships an older
	# version of openjdk for compatibility with old Minecraft
	# seal331 23/05/2025 4:39 MSK: and more Java stuff got added...
	if ('openjdk-major' == pkgname) or ('openjdk' == pkgname) or \
			('openjdk-build' == pkgname) or ('java-major' == pkgname) or \
			('java' == pkgname) or ('java-build' == pkgname):
		return False

	# seal331 22/05/2025 21:56 MSK: rofi-wayland is tied to upstream
	# rofi, so check only one
	if ('rofi-wayland' == pkgname):
		return False

	# seal331 22/05/2025 21:59 MSK: cde-de is named cdesktopenv in most
	# places
	# seal331 23/05/2025 2:03 MSK: and it's also not in Arch's official 
	# repos
	if ('cde-de' == pkgname):
		pkgname = 'cdesktopenv'
		repo = 'pkgsrc_current'

	# seal331 22/05/2025 22:02 MSK: wayfire has coordinated releases of
	# their entire suite
	if ('wf-config' == pkgname) or ('wayfire' == pkgname) or \
			('wayfire-plugins-extra' == pkgname):
		return False
	if ('wf' == pkgname):
		pkgname = 'wayfire'

	# seal331 22/05/2025 22:04 MSK: musashi-submodule is not a package
	if ('musashi-submodule' == pkgname):
		return False

	# seal331 22/05/2025 22:05 MSK: dolphin is a mess of submodules
	if ('dolphin' in pkgname) and (not (pkgname == 'dolphin')):
		return False

	# seal331 22/05/2025 22:08 MSK: mupen64plus is very modular but it's
	# still one suite
	if ('mupen64plus' in pkgname) and (not (pkgname == 'mupen64plus')):
                return False
	if ('gliden64' == pkgname):
		return False

	# seal331 23/05/2025 0:56 MSK: intercal is not in Arch's repos
	if ('intercal' == pkgname):
		repo = 'freebsd'

	# seal331 23/05/2025 0:58 MSK: aquamarine has a different name on
	# Repology's side
	if ('aquamarine' == pkgname):
		pkgname = 'aquamarine-rendering-backend'

	# seal331 23/05/2025 0:59 MSK: printproto is not in Arch's repos
	if ('printproto' == pkgname):
		repo = 'opensuse_tumbleweed'

	# seal331 23/05/2025 1:00 MSK: wayfire is not in Arch's official repos
	if ('wayfire' == pkgname):
		repo = 'debian_unstable'

	# seal331 23/05/2025 1:02 MSK: we actually ship a newer version of
	# xhomer than all the BSDs which are the sole people who ship it other
	# than us, and given how the release prior to the 2024 one was in 2006
	# there's not really much sense to check it this often
	if ('xhomer' == pkgname):
		return False

	# seal331 23/05/2025 1:20 MSK: gkermit is not in Arch's repos
	if ('gkermit' == pkgname):
		repo = 'debian_unstable'

	# seal331 23/05/2025 1:21 MSK: lotus123 is not in Arch's repos
	if ('lotus123' == pkgname):
		repo = 'slackbuilds'

	# seal331 23/05/2025 1:22 MSK: melonds is not in Arch's repos
	if ('melonds' == pkgname):
		repo = 'opensuse_tumbleweed'

	# seal331 23/05/2025 1:23 MSK: dolphin has a different name on
	# Repology's side
	# seal331 23/05/2025 4:45 MSK: and it's also not up to date in Arch
	if ('dolphin' == pkgname):
		pkgname = 'dolphin-emu'
		repo = 'fedora_rawhide'

	# seal331 23/05/2025 1:28 MSK: prismlauncher has a different name on
	# Repology's side and is not in Arch's official repos

	if ('prism-launcher' == pkgname):
		pkgname = 'prismlauncher'
		repo = 'alpine_edge'

	# seal331 23/05/2025 1:30 MSK: neofetch is not in Arch's official repos
	if ('neofetch' == pkgname):
		repo = 'alpine_edge'

	# seal331 23/05/2025 1:32 MSK: literally no one ships heirloom-ng, so
	# this is a hack to check it
	if ('heirloom-ng' == pkgname):
		print(f'Currently parsing {pkgname}')
		tomlout.write(f'''[{pkgname}]
source = "github"
github = "Projeto-Pindorama/heirloom-ng"
use_latest_release = true

''')
		os.system(f'nvtake -c lfsqol.toml {pkgname}={version}')
		return False

	# seal331 23/05/2025 1:45 MSK: unlambda collides with some haskell
	# thing leading to false positives, and given how the last update was
	# 1999 don't even bother
	if ('unlambda' == pkgname):
		return False

	# seal331 23/05/2025 1:48 MSK: for some reason quite a lot of distros
	# are still shipping AT&T ksh which has been unmaintained since 2020,
	# switch to a distro that ships the maintained fork to avoid false
	# positives
	if ('ksh' == pkgname):
		repo = 'fedora_rawhide'

	# seal331 23/05/2025 1:52 MSK: schilytools is not in Arch's official
	# repos
	# seal331 23/05/2025 2:11 MSK: and we use a different version notation
	# than everyone else, so make us comply as to not get false positives
	if ('schilytools' == pkgname):
		repo = 'opensuse_tumbleweed'
		version = version.replace('-', '.')

	# seal331 23/05/2025 1:53 MSK: heirloom-sh is not in Arch's official
	# repos
	if ('heirloom-sh' == pkgname):
		repo = 'gentoo'

	# seal331 23/05/2025 1:54 MSK: heirloom-devtools is not in Arch's repos
	if ('heirloom-devtools' == pkgname):
		repo = 'adelie_current'

	# seal331 23/05/2025 1:57 MSK: fuse2 is a legacy version, don't bother
	if ('fuse2' == pkgname):
		return False

	# seal331 23/05/2025 1:59 MSK: qrcodegencpp is not in Arch's repos
	if ('qrcodegencpp' == pkgname):
		repo = 'nix_unstable'

	# seal331 23/05/2025 2:01 MSK: wbg is not in Arch's official repos
	if ('wbg' == pkgname):
		repo = 'opensuse_tumbleweed'

	# seal331 23/05/2025 2:04 MSK: sdl2_net has a different name in Repology
	if ('sdl2_net' == pkgname):
		pkgname = 'sdl2-net'

	# seal331 23/05/2025 2:05 MSK: befunge has a different name in Repology
	# and is only shipped by Homebrew and us
	if ('befunge' == pkgname):
		pkgname = 'befunge93'
		repo = 'homebrew'

	# seal331 23/05/2025 2:08 MSK: we use a different asio version notation
	# than everyone else, so make us comply so we don't get false positives
	if ('asio' == pkgname):
		version = version.replace('-', '.')

	# seal331 23/05/2025 2:13 MSK: re2 version notation is inconsistent
	# between distros, so switch to one that doesn't require us to bother
	# with changing ours
	if ('re2' == pkgname):
		repo = 'nix_unstable'

	# seal331 23/05/2025 2:15 MSK: tmux version notation is inconsistent
	# between distros, so switch to one that doesn't require us to bother
	# with changing ours
	if ('tmux' == pkgname):
		repo = 'debian_unstable'

	# seal331 28/05/2025 13:29 MSK: inxi version is split across 2
	# separate entities, this is the exact thing I hoped wouldn't happen...
	# put a hack here so we can at least attempt to parse it
	# seal331 28/05/2025 13:37 MSK: and we use a different notation than
	# some distros, so check a distro with the same notation
	if ('inxi-rev' == pkgname):
		TMP_inxi_revision = version
		return False
	if ('inxi' == pkgname):
		if TMP_inxi_revision == 'PLCHLDR':
			print('ERROR: something broke with inxi rev handler', file=sys.stderr)
			sys.exit(1)
		version = version.replace('&inxi-rev;', TMP_inxi_revision)
		repo = 'debian_unstable'

	# seal331 28/05/2025 14:43 MSK: GCC is checked by the LFS team, not us
	if ('gcc' == pkgname):
		return False

	# seal331 30/05/2025 22:14 MSK: libutempter-tag is used just so we can
	# get stuff from GitHub properly
	if ('libutempter-tag' == pkgname):
		return False

	# seal331 30/05/2025 22:16 MSK: see LFS-QOL packages.ent comment above
	# the Rofi entries to see why we need this
	if ('rofi' == pkgname):
		return False
	if ('rofi-full' == pkgname):
		pkgname = 'rofi'
		if (version != '1.7.9.1') and MAINTAINER_MODE:
			print('Maintainer warning: please check if the Rofi hack is still needed', file=sys.stderr)

	# seal331 03/06/2025 20:41 MSK: libime-kenlm is a submodule, not a
        # package itself
	if ('libime-kenlm' == pkgname):
		return False

	# seal331 03/06/2025 20:44 MSK: cldr-emoji-annotation-tarball is just
	# the tarball version
	if ('cldr-emoji-annotation-tarball' == pkgname):
		return False

	# seal331 03/06/2025 20:56 MSK: we use a slightly different version
	# notation than everyone else; and Arch still packages the dead
	# upstream version which you can't even fetch despite Debian fixing
	# it up
	if ('anthy' == pkgname):
		repo = 'debian_unstable'
		version = version.split(':')[1]
		version = version.split('-')[0]

	# seal331 03/06/2025 20:59 MSK: don't bother checking this, there's
	# a pending TODO to drop this in favor of actual up-to-date Unicode
	# CLDR, the repo from which we get this is unmaintained and nobody
	# ships it
	if ('cldr-emoji-annotation' == pkgname):
		return False

	# seal331 03/06/2025 21:04 MSK: Repology uses a different name for
	# this than us
	if ('m17n' == pkgname):
		pkgname = 'm17n-lib'

	# seal331 03/06/2025 21:07 MSK: Arch has an outdated version of this
	if ('m17n-db' == pkgname):
		repo = 'debian_unstable'

	# seal331 22/05/2025 21:27 MSK: -minor stuff is usually nicer-looking
	# Git commit abbreviations, we check the git stuff separately
	# NOT ALWAYS TRUE, KEEP THIS SPECIAL CASE LAST
	if ('minor' in pkgname):
		gitstuff.append(pkgname.split("-minor")[0])
		return False

	# SPECIAL CASING ENDS HERE
	return [repo, pkgname, version]

if len(sys.argv) != 2:
	usage()

tomlout = open("lfsqol.toml", "w")
tomlout.write('''[__config__]
oldver = "versions_book.json"
newver = "versions_current.json"
max_concurrency = 1

''')

tomlout.close()
tomlout = open("lfsqol.toml", "a")

gitout = open("lfsqol-git.txt", "w")

with open(sys.argv[1], 'r') as f:
	for line in f:
		parsed = parsexml(line)
		if parsed == False:
			continue
		if not MAINTAINER_MODE:
			if parsed[1] not in pkgs:
				continue
		print(f'Currently parsing {parsed[1]}')
		if parsed[1] in gitstuff:
			gitout.write(f"{parsed[1]} {parsed[2]}\n")
		else:
			tomlout.write(f'''[{parsed[1]}]
source = "repology"
repology = "{parsed[1]}"
repo = "{parsed[0]}"

''')
			os.system(f'nvtake -c lfsqol.toml {parsed[1]}={parsed[2]}')

gitout.close()
tomlout.close()
