DOCSTUBGEN-NG(1) ["DOCSTUBGEN-NG(1)" ["*LFS Tools"]]


# NAME

*docstubgen-ng* - generate docstubs for \*LFS pages


# SYNOPSIS

*docstubgen-ng* package DESTDIR


# EXAMPLES

*docstubgen-ng* curl /source/curl/DESTDIR | wl-copy


# ENVIRONMENT

- *DOCSTUBGEN_DEBUG* - if set, display debug output
- *DOCSTUBGEN_RECURSION_DEPTH* - recursion depth limit when finding files in
  destdir, defaults to 64


# EXIT STATUS

- *0* - success
- *1* - docstubgen failed
- *2* - syntax or other usage error


# DESCRIPTION

Docstubgen-ng is the next-generation version of the original docstubgen, which
was a utility to generate XML-formatted documentation stubs for \*LFS packages.

These docstubs can be copied to the XML page for a package. The only necessary
edits should then be descriptions for contents.


# HISTORY

The original docstubgen was written by Seal Sealy in early 2025 and first
introduced into SLFS, then called LFS-QOL on February 1st. What began as a 74
line Python script ballooned to 359 lines of undocumented hacks and a
backward-compatibility graveyard by the time it was moved to the lfs-tools
repository.

On August 16th, Sealy opened an issue for the rewrite Tox had begun working on.
An excerpt is shown below:

_"The codebase as is is written in such an awful way that I have no clue what's
going on in specific parts of the code, and the only reason why I can even
maintain it is because I still have a faint idea of the control flow."_
	_\-\- Seal Sealy_

Tox pushed her first draft of docstubgen-ng on August 29th, before remembering
she was now in college and had no time (and also that she has a distaste for
XML). All work on the rewrite was halted until November 10th, whereupon instead
of reviewing for her Linear Algebra exam, Tox largely completed the rewrite.


# REPORTING BUGS

If you discover a bug, please open an issue at++
https://github.com/glfs-book/lfs-tools/issues.


# AUTHORS

Docstubgen-ng is primarily maintained by tox <tox@tox.wtf>. The project is part
of the lfs-tools repository hosted at++
https://github.com/glfs-book/lfs-tools.

The original docstubgen was authored by Seal Sealy <butilkama@gmail.com>.


# COPYRIGHT

MIT License

Copyright (c) 2025 The GLFS Development Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
