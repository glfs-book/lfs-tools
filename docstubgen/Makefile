# Makefile for docstubgen
#
# Copyright (c) 2025 The GLFS Development Team

.PHONY all install install-docstubgen install-man clean lint test testdata

PREFIX=/usr
BINDIR=$(PREFIX)/bin
DATADIR=$(PREFIX)/share
MANDIR=$(DATADIR)/man

all: docstubgen-ng.1

docstubgen-ng.1: docstubgen-ng.1.scd
	scdoc < docstubgen-ng.1.scd > docstubgen-ng.1

install: install-docstubgen install-man

install-docstubgen: docstubgen-ng
	install -Dm755 docstubgen-ng -t $(DESTDIR)$(BINDIR)/

install-man: docstubgen-ng.1
	install -Dm644 docstubgen-ng.1 -t $(DESTDIR)$(MANDIR)/man1/

clean:
	rm -f docstubgen-ng.1
	rm -rf tests/*_DESTDIR tests/*.tar.?z
	rm -f docstubgen-ng.tar.gz

lint: docstubgen-ng
	typos docstubgen-ng docstubgen-ng.1.scd
	shellcheck docstubgen-ng

test: docstubgen-ng testdata
	tests/run.sh

docstubgen-ng.tar.gz: all
	make
	make DESTDIR=$$PWD/docstubgen-ng-0.0.0 install
	tar czf docstubgen-ng.tar.gz docstubgen-ng-0.0.0
	rm -rf docstubgen-ng-0.0.0

testdata: tests/fastfetch-linux-amd64.tar.gz \
	tests/curl-8.17.0-x86_64-1.tar.xz \
	tests/docstubgen-ng.tar.gz

tests/docstubgen-ng.tar.gz: docstubgen-ng.tar.gz
	mv -f docstubgen-ng.tar.gz tests/

tests/fastfetch-linux-amd64.tar.gz:
	curl -fsSL https://github.com/fastfetch-cli/fastfetch/releases/download/2.54.0/fastfetch-linux-amd64.tar.gz -o tests/fastfetch-linux-amd64.tar.gz

tests/curl-8.17.0-x86_64-1.tar.xz:
	curl -fsSL https://mirrors.slackware.com/slackware/slackware64-current/slackware64/n/curl-8.17.0-x86_64-1.txz -o tests/curl-8.17.0-x86_64-1.tar.xz
