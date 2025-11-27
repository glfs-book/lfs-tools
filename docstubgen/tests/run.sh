#!/usr/bin/env bash

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

    if [ ! -d "${package}_DESTDIR" ]; then
        tar -xf "${package}"*.tar.?z &&
            [ -d "${package}"*/ ] && mv -f "${package}"*/ "${package}_DESTDIR"
    fi
done

# TODO: Get a better tarball for curl or use a different package
# Curl hack
if [ -d install ]; then
    rm -rf install
    mkdir -p curl_DESTDIR && mv usr curl_DESTDIR
fi

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
