#!/usr/bin/env bash

# WARNING: This test suite is still in a very rough state

set -u

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
owd="$PWD"
cd "$SCRIPT_DIR"

teststatus() {
    case "$1" in
        0 )
            printf "PASS\n"
            ((passed++))
        ;;
        * )
            printf "FAIL\n"
            ((failed++))
        ;;
    esac
}

# Setup testdata
for package in *.xml; do
    package="${package%.xml}"

    tar -xf ${package}*.tar.?z &&
        mv -f ${package}*/ ${package}_DESTDIR
done

rm -rf install
mkdir curl-slack && mv usr curl-slack

# Run tests
passed=0
failed=0
curr=0
for destdir in *_DESTDIR; do
    ((curr++))
    package="${destdir%_*}"
    printf "%d. %16s " "$curr" "$package"
    ../docstubgen-ng "$package" "$destdir" | diff - "$package.xml"
    teststatus "$?"
done

if [ $failed -gt 0 ]; then
    echo "$failed tests failed" >&2
    exit 1
fi

echo "All tests passed"
