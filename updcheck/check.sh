#!/bin/bash

set -e

# Helper script for running the entire updcheck suite.
# (C) Seal Sealy, 2025

if [ -z "$1" ]; then
	echo "Usage: check.sh packages.ent"
	echo "Set the CONTINUE_ON_ERRORS environment variable to ignore errors"
	echo "post-Stage 1. Warning: NOT RECOMMENDED."
	exit 1
fi

if [ ! -f ./packagesent2toml.py ]; then
	echo "Error: this script must be run from the updcheck folder."
	exit 1
fi

if ! command -v nvchecker &> /dev/null; then
	echo "Error: nvchecker is not installed."
	exit 1
fi

# this also generates idle-currentver, which is required for stage4
echo "Running Stage 1 - packagesent2toml"
python3 packagesent2toml.py $1 > /dev/null
echo "Stage 1 finished successfully."

if [ ! -z "${CONTINUE_ON_ERRORS}" ]; then
	echo "WARNING: You have chosen to ignore all errors post-Stage 1."
	echo "This is NOT something the updcheck maintainers recommend doing,"
	echo "and if you have an actual issue with updcheck, it is better to"
	echo "report it to the maintainers on the lfs-tools issue tracker than"
	echo "to use this option. Continue at your own risk."
	set +e
fi

echo "Running Stage 2 - nvchecker"
nvchecker -c lfsqol.toml --failures -l error
echo "Stage 2 finished successfully."

echo "Running Stage 3 - gitcheck"
rm -f gitcheck-upd.txt
python3 gitcheck.py knowngit.txt lfsqol-git.txt > /dev/null
echo "Stage 3 finished successfully."

if ! command -v svn &> /dev/null; then
        echo "SVN not installed. Skipping Stage 4."
else
	echo "Running Stage 4 - idle update check"
	newest=$(svn info https://svn.code.sf.net/p/idle-lisa-emu/code/ | awk '/Revision:/ { print $2 }')
	current=$(cat idle-currentver)
	if [[ "$current" != "$newest" ]]; then
		echo "idle update available: r$current -> r$newest" > idle-update.txt
	fi
	echo "Stage 4 completed successfully."
fi

echo "Stage 5 - collecting results"
nvcmp -c lfsqol.toml
if [ -f ./gitcheck-upd.txt ]; then
	cat gitcheck-upd.txt
fi
if [ -f ./idle-update.txt ]; then
        cat idle-update.txt
fi
echo "Please manually check for OpenJDK updates."
echo "Stage 5 done."
echo "Script done."
