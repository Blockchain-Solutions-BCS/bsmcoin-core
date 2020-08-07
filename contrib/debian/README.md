
Debian
====================
This directory contains files used to package bsmcoind/bsmcoin-qt
for Debian-based Linux systems. If you compile bsmcoind/bsmcoin-qt yourself, there are some useful files here.

## bsmcoin: URI support ##


bsmcoin-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install bsmcoin-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your bsmcoin-qt binary to `/usr/bin`
and the `../../share/pixmaps/bsmcoin128.png` to `/usr/share/pixmaps`

bsmcoin-qt.protocol (KDE)

