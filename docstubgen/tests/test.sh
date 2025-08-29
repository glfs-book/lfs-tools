#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
pushd . >/dev/null
cd "$SCRIPT_DIR/.."

env \
    DOCSTUBGEN_TRUSTED_INPUT=1 \
    DOCSTUBGEN_RECURSIVE_SEARCH=1 \
    DOCSTUBGEN_DOCUMENT_LIBRARIES=1 \
    DOCSTUBGEN_I_KNOW_WHAT_I_AM_DOING=1 \
./obj/docstubgen testpkg TESTDIR

./docstubgen-ng testpkg TESTDIR

popd >/dev/null
