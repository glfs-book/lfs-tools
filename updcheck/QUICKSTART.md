# updcheck

A tool for checking LFS-QOL package updates.

## Dependencies

This tool depends on a utility called nvchecker, which has been slightly modified to work around
an issue involving Repology's rate-limiting system. In order to install nvchecker, please execute
the following:

```bash
wget https://github.com/lilydjwg/nvchecker/archive/refs/tags/v2.17.tar.gz
tar zxvf v2.17.tar.gz
cd nvchecker-2.17
patch -Np1 -i ../nvchecker.diff
pip3 install .
cd ..
```

It also depends on Git (to check for updates of those packages LFS-QOL uses direct Git commits
of) and optionally depends on Subversion (to check for updates to idle).

## Running

Just run ``check.sh`` on the LFS-QOL packages.ent file.

## Quirks

When rofi is updated, it's implied that rofi-wayland needs to be updated as well.
