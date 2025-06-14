# updcheck

A tool for checking LFS-QOL package updates.

## Dependencies

This tool depends on a utility called nvchecker, which has been slightly
modified to work around an issue involving Repology's rate-limiting system. In
order to install nvchecker, please follow the SLFS page for it
[here](https://glfs-book.github.io/slfs/general/python-modules.html#nvchecker),
apply the patch, and download the recommended dependencies.
For checking for certain packages that only have a subversion repository, which
there is a checking stage dedicated to it, you will need [Subversion from
BLFS](https://linuxfromscratch.org/blfs/view/svn/general/subversion.html).
The [idle](https://glfs-book.github.io/slfs/emu/idle.html) package is one such
package.

## Running

Just run ``check.sh`` on the LFS-QOL packages.ent file.

## Quirks

When rofi is updated, it's implied that rofi-wayland needs to be updated as well.
