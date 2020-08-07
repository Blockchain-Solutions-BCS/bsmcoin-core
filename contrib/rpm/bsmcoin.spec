%define bdbv 4.8.30
%global selinux_variants mls strict targeted

%if 0%{?_no_gui:1}
%define _buildqt 0
%define buildargs --with-gui=no
%else
%define _buildqt 1
%if 0%{?_use_qt4}
%define buildargs --with-qrencode --with-gui=qt4
%else
%define buildargs --with-qrencode --with-gui=qt5
%endif
%endif

Name:		bsmcoin
Version:	0.12.0
Release:	2%{?dist}
Summary:	Peer to Peer Cryptographic Currency

Group:		Applications/System
License:	MIT
URL:		https://bsmcoin.org/
Source0:	https://bsmcoin.org/bin/bsmcoin-core-%{version}/bsmcoin-%{version}.tar.gz
Source1:	http://download.oracle.com/berkeley-db/db-%{bdbv}.NC.tar.gz

Source10:	https://raw.githubusercontent.com/bsmcoin/bsmcoin/v%{version}/contrib/debian/examples/bsmcoin.conf

#man pages
Source20:	https://raw.githubusercontent.com/bsmcoin/bsmcoin/v%{version}/contrib/debian/manpages/bsmcoind.1
Source21:	https://raw.githubusercontent.com/bsmcoin/bsmcoin/v%{version}/contrib/debian/manpages/bsmcoin-cli.1
Source22:	https://raw.githubusercontent.com/bsmcoin/bsmcoin/v%{version}/contrib/debian/manpages/bsmcoin-qt.1
Source23:	https://raw.githubusercontent.com/bsmcoin/bsmcoin/v%{version}/contrib/debian/manpages/bsmcoin.conf.5

#selinux
Source30:	https://raw.githubusercontent.com/bsmcoin/bsmcoin/v%{version}/contrib/rpm/bsmcoin.te
# Source31 - what about bsmcoin-tx and bench_bsmcoin ???
Source31:	https://raw.githubusercontent.com/bsmcoin/bsmcoin/v%{version}/contrib/rpm/bsmcoin.fc
Source32:	https://raw.githubusercontent.com/bsmcoin/bsmcoin/v%{version}/contrib/rpm/bsmcoin.if

Source100:	https://upload.wikimedia.org/wikipedia/commons/4/46/BsmCoin.svg

%if 0%{?_use_libressl:1}
BuildRequires:	libressl-devel
%else
BuildRequires:	openssl-devel
%endif
BuildRequires:	boost-devel
BuildRequires:	miniupnpc-devel
BuildRequires:	autoconf automake libtool
BuildRequires:	libevent-devel


Patch0:		bsmcoin-0.12.0-libressl.patch


%description
BsmCoin is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of bsmcoins is carried out collectively by the network.

%if %{_buildqt}
%package core
Summary:	Peer to Peer Cryptographic Currency
Group:		Applications/System
Obsoletes:	%{name} < %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
%if 0%{?_use_qt4}
BuildRequires:	qt-devel
%else
BuildRequires:	qt5-qtbase-devel
# for /usr/bin/lrelease-qt5
BuildRequires:	qt5-linguist
%endif
BuildRequires:	protobuf-devel
BuildRequires:	qrencode-devel
BuildRequires:	%{_bindir}/desktop-file-validate
# for icon generation from SVG
BuildRequires:	%{_bindir}/inkscape
BuildRequires:	%{_bindir}/convert

%description core
BsmCoin is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of bsmcoins is carried out collectively by the network.

This package contains the Qt based graphical client and node. If you are looking
to run a BsmCoin wallet, this is probably the package you want.
%endif


%package libs
Summary:	BsmCoin shared libraries
Group:		System Environment/Libraries

%description libs
This package provides the bsmcoinconsensus shared libraries. These libraries
may be used by third party software to provide consensus verification
functionality.

Unless you know need this package, you probably do not.

%package devel
Summary:	Development files for bsmcoin
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files and static library for the
bsmcoinconsensus shared library. If you are developing or compiling software
that wants to link against that library, then you need this package installed.

Most people do not need this package installed.

%package server
Summary:	The bsmcoin daemon
Group:		System Environment/Daemons
Requires:	bsmcoin-utils = %{version}-%{release}
Requires:	selinux-policy policycoreutils-python
Requires(pre):	shadow-utils
Requires(post):	%{_sbindir}/semodule %{_sbindir}/restorecon %{_sbindir}/fixfiles %{_sbindir}/sestatus
Requires(postun):	%{_sbindir}/semodule %{_sbindir}/restorecon %{_sbindir}/fixfiles %{_sbindir}/sestatus
BuildRequires:	systemd
BuildRequires:	checkpolicy
BuildRequires:	%{_datadir}/selinux/devel/Makefile

%description server
This package provides a stand-alone bsmcoin-core daemon. For most users, this
package is only needed if they need a full-node without the graphical client.

Some third party wallet software will want this package to provide the actual
bsmcoin-core node they use to connect to the network.

If you use the graphical bsmcoin-core client then you almost certainly do not
need this package.

%package utils
Summary:	BsmCoin utilities
Group:		Applications/System

%description utils
This package provides several command line utilities for interacting with a
bsmcoin-core daemon.

The bsmcoin-cli utility allows you to communicate and control a bsmcoin daemon
over RPC, the bsmcoin-tx utility allows you to create a custom transaction, and
the bench_bsmcoin utility can be used to perform some benchmarks.

This package contains utilities needed by the bsmcoin-server package.


%prep
%setup -q
%patch0 -p1 -b .libressl
cp -p %{SOURCE10} ./bsmcoin.conf.example
tar -zxf %{SOURCE1}
cp -p db-%{bdbv}.NC/LICENSE ./db-%{bdbv}.NC-LICENSE
mkdir db4 SELinux
cp -p %{SOURCE30} %{SOURCE31} %{SOURCE32} SELinux/


%build
CWD=`pwd`
cd db-%{bdbv}.NC/build_unix/
../dist/configure --enable-cxx --disable-shared --with-pic --prefix=${CWD}/db4
make install
cd ../..

./autogen.sh
%configure LDFLAGS="-L${CWD}/db4/lib/" CPPFLAGS="-I${CWD}/db4/include/" --with-miniupnpc --enable-glibc-back-compat %{buildargs}
make %{?_smp_mflags}

pushd SELinux
for selinuxvariant in %{selinux_variants}; do
	make NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile
	mv bsmcoin.pp bsmcoin.pp.${selinuxvariant}
	make NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile clean
done
popd


%install
make install DESTDIR=%{buildroot}

mkdir -p -m755 %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/bsmcoind %{buildroot}%{_sbindir}/bsmcoind

# systemd stuff
mkdir -p %{buildroot}%{_tmpfilesdir}
cat <<EOF > %{buildroot}%{_tmpfilesdir}/bsmcoin.conf
d /run/bsmcoind 0750 bsmcoin bsmcoin -
EOF
touch -a -m -t 201504280000 %{buildroot}%{_tmpfilesdir}/bsmcoin.conf

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/bsmcoin
# Provide options to the bsmcoin daemon here, for example
# OPTIONS="-testnet -disable-wallet"

OPTIONS=""

# System service defaults.
# Don't change these unless you know what you're doing.
CONFIG_FILE="%{_sysconfdir}/bsmcoin/bsmcoin.conf"
DATA_DIR="%{_localstatedir}/lib/bsmcoin"
PID_FILE="/run/bsmcoind/bsmcoind.pid"
EOF
touch -a -m -t 201504280000 %{buildroot}%{_sysconfdir}/sysconfig/bsmcoin

mkdir -p %{buildroot}%{_unitdir}
cat <<EOF > %{buildroot}%{_unitdir}/bsmcoin.service
[Unit]
Description=BsmCoin daemon
After=syslog.target network.target

[Service]
Type=forking
ExecStart=%{_sbindir}/bsmcoind -daemon -conf=\${CONFIG_FILE} -datadir=\${DATA_DIR} -pid=\${PID_FILE} \$OPTIONS
EnvironmentFile=%{_sysconfdir}/sysconfig/bsmcoin
User=bsmcoin
Group=bsmcoin

Restart=on-failure
PrivateTmp=true
TimeoutStopSec=120
TimeoutStartSec=60
StartLimitInterval=240
StartLimitBurst=5

[Install]
WantedBy=multi-user.target
EOF
touch -a -m -t 201504280000 %{buildroot}%{_unitdir}/bsmcoin.service
#end systemd stuff

mkdir %{buildroot}%{_sysconfdir}/bsmcoin
mkdir -p %{buildroot}%{_localstatedir}/lib/bsmcoin

#SELinux
for selinuxvariant in %{selinux_variants}; do
	install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
	install -p -m 644 SELinux/bsmcoin.pp.${selinuxvariant} %{buildroot}%{_datadir}/selinux/${selinuxvariant}/bsmcoin.pp
done

%if %{_buildqt}
# qt icons
install -D -p share/pixmaps/bsmcoin.ico %{buildroot}%{_datadir}/pixmaps/bsmcoin.ico
install -p share/pixmaps/nsis-header.bmp %{buildroot}%{_datadir}/pixmaps/
install -p share/pixmaps/nsis-wizard.bmp %{buildroot}%{_datadir}/pixmaps/
install -p %{SOURCE100} %{buildroot}%{_datadir}/pixmaps/bsmcoin.svg
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/bsmcoin16.png -w16 -h16
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/bsmcoin32.png -w32 -h32
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/bsmcoin64.png -w64 -h64
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/bsmcoin128.png -w128 -h128
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/bsmcoin256.png -w256 -h256
%{_bindir}/convert -resize 16x16 %{buildroot}%{_datadir}/pixmaps/bsmcoin256.png %{buildroot}%{_datadir}/pixmaps/bsmcoin16.xpm
%{_bindir}/convert -resize 32x32 %{buildroot}%{_datadir}/pixmaps/bsmcoin256.png %{buildroot}%{_datadir}/pixmaps/bsmcoin32.xpm
%{_bindir}/convert -resize 64x64 %{buildroot}%{_datadir}/pixmaps/bsmcoin256.png %{buildroot}%{_datadir}/pixmaps/bsmcoin64.xpm
%{_bindir}/convert -resize 128x128 %{buildroot}%{_datadir}/pixmaps/bsmcoin256.png %{buildroot}%{_datadir}/pixmaps/bsmcoin128.xpm
%{_bindir}/convert %{buildroot}%{_datadir}/pixmaps/bsmcoin256.png %{buildroot}%{_datadir}/pixmaps/bsmcoin256.xpm
touch %{buildroot}%{_datadir}/pixmaps/*.png -r %{SOURCE100}
touch %{buildroot}%{_datadir}/pixmaps/*.xpm -r %{SOURCE100}

# Desktop File - change the touch timestamp if modifying
mkdir -p %{buildroot}%{_datadir}/applications
cat <<EOF > %{buildroot}%{_datadir}/applications/bsmcoin-core.desktop
[Desktop Entry]
Encoding=UTF-8
Name=BsmCoin
Comment=BsmCoin P2P Cryptocurrency
Comment[fr]=BsmCoin, monnaie virtuelle cryptographique pair à pair
Comment[tr]=BsmCoin, eşten eşe kriptografik sanal para birimi
Exec=bsmcoin-qt %u
Terminal=false
Type=Application
Icon=bsmcoin128
MimeType=x-scheme-handler/bsmcoin;
Categories=Office;Finance;
EOF
# change touch date when modifying desktop
touch -a -m -t 201511100546 %{buildroot}%{_datadir}/applications/bsmcoin-core.desktop
%{_bindir}/desktop-file-validate %{buildroot}%{_datadir}/applications/bsmcoin-core.desktop

# KDE protocol - change the touch timestamp if modifying
mkdir -p %{buildroot}%{_datadir}/kde4/services
cat <<EOF > %{buildroot}%{_datadir}/kde4/services/bsmcoin-core.protocol
[Protocol]
exec=bsmcoin-qt '%u'
protocol=bsmcoin
input=none
output=none
helper=true
listing=
reading=false
writing=false
makedir=false
deleting=false
EOF
# change touch date when modifying protocol
touch -a -m -t 201511100546 %{buildroot}%{_datadir}/kde4/services/bsmcoin-core.protocol
%endif

# man pages
install -D -p %{SOURCE20} %{buildroot}%{_mandir}/man1/bsmcoind.1
install -p %{SOURCE21} %{buildroot}%{_mandir}/man1/bsmcoin-cli.1
%if %{_buildqt}
install -p %{SOURCE22} %{buildroot}%{_mandir}/man1/bsmcoin-qt.1
%endif
install -D -p %{SOURCE23} %{buildroot}%{_mandir}/man5/bsmcoin.conf.5

# nuke these, we do extensive testing of binaries in %%check before packaging
rm -f %{buildroot}%{_bindir}/test_*

%check
make check
pushd src
srcdir=. test/bsmcoin-util-test.py
popd
qa/pull-tester/rpc-tests.py -extended

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%pre server
getent group bsmcoin >/dev/null || groupadd -r bsmcoin
getent passwd bsmcoin >/dev/null ||
	useradd -r -g bsmcoin -d /var/lib/bsmcoin -s /sbin/nologin \
	-c "BsmCoin wallet server" bsmcoin
exit 0

%post server
%systemd_post bsmcoin.service
# SELinux
if [ `%{_sbindir}/sestatus |grep -c "disabled"` -eq 0 ]; then
for selinuxvariant in %{selinux_variants}; do
	%{_sbindir}/semodule -s ${selinuxvariant} -i %{_datadir}/selinux/${selinuxvariant}/bsmcoin.pp &> /dev/null || :
done
%{_sbindir}/semanage port -a -t bsmcoin_port_t -p tcp 5555
%{_sbindir}/semanage port -a -t bsmcoin_port_t -p tcp 5556
%{_sbindir}/semanage port -a -t bsmcoin_port_t -p tcp 15555
%{_sbindir}/semanage port -a -t bsmcoin_port_t -p tcp 15556
%{_sbindir}/fixfiles -R bsmcoin-server restore &> /dev/null || :
%{_sbindir}/restorecon -R %{_localstatedir}/lib/bsmcoin || :
fi

%posttrans server
%{_bindir}/systemd-tmpfiles --create

%preun server
%systemd_preun bsmcoin.service

%postun server
%systemd_postun bsmcoin.service
# SELinux
if [ $1 -eq 0 ]; then
	if [ `%{_sbindir}/sestatus |grep -c "disabled"` -eq 0 ]; then
	%{_sbindir}/semanage port -d -p tcp 5555
	%{_sbindir}/semanage port -d -p tcp 5556
	%{_sbindir}/semanage port -d -p tcp 15555
	%{_sbindir}/semanage port -d -p tcp 15556
	for selinuxvariant in %{selinux_variants}; do
		%{_sbindir}/semodule -s ${selinuxvariant} -r bsmcoin &> /dev/null || :
	done
	%{_sbindir}/fixfiles -R bsmcoin-server restore &> /dev/null || :
	[ -d %{_localstatedir}/lib/bsmcoin ] && \
		%{_sbindir}/restorecon -R %{_localstatedir}/lib/bsmcoin &> /dev/null || :
	fi
fi

%clean
rm -rf %{buildroot}

%if %{_buildqt}
%files core
%defattr(-,root,root,-)
%license COPYING db-%{bdbv}.NC-LICENSE
%doc COPYING bsmcoin.conf.example doc/README.md doc/bips.md doc/files.md doc/multiwallet-qt.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%attr(0755,root,root) %{_bindir}/bsmcoin-qt
%attr(0644,root,root) %{_datadir}/applications/bsmcoin-core.desktop
%attr(0644,root,root) %{_datadir}/kde4/services/bsmcoin-core.protocol
%attr(0644,root,root) %{_datadir}/pixmaps/*.ico
%attr(0644,root,root) %{_datadir}/pixmaps/*.bmp
%attr(0644,root,root) %{_datadir}/pixmaps/*.svg
%attr(0644,root,root) %{_datadir}/pixmaps/*.png
%attr(0644,root,root) %{_datadir}/pixmaps/*.xpm
%attr(0644,root,root) %{_mandir}/man1/bsmcoin-qt.1*
%endif

%files libs
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/shared-libraries.md
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/developer-notes.md doc/shared-libraries.md
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files server
%defattr(-,root,root,-)
%license COPYING db-%{bdbv}.NC-LICENSE
%doc COPYING bsmcoin.conf.example doc/README.md doc/REST-interface.md doc/bips.md doc/dnsseed-policy.md doc/files.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%attr(0755,root,root) %{_sbindir}/bsmcoind
%attr(0644,root,root) %{_tmpfilesdir}/bsmcoin.conf
%attr(0644,root,root) %{_unitdir}/bsmcoin.service
%dir %attr(0750,bsmcoin,bsmcoin) %{_sysconfdir}/bsmcoin
%dir %attr(0750,bsmcoin,bsmcoin) %{_localstatedir}/lib/bsmcoin
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/bsmcoin
%attr(0644,root,root) %{_datadir}/selinux/*/*.pp
%attr(0644,root,root) %{_mandir}/man1/bsmcoind.1*
%attr(0644,root,root) %{_mandir}/man5/bsmcoin.conf.5*

%files utils
%defattr(-,root,root,-)
%license COPYING
%doc COPYING bsmcoin.conf.example doc/README.md
%attr(0755,root,root) %{_bindir}/bsmcoin-cli
%attr(0755,root,root) %{_bindir}/bsmcoin-tx
%attr(0755,root,root) %{_bindir}/bench_bsmcoin
%attr(0644,root,root) %{_mandir}/man1/bsmcoin-cli.1*
%attr(0644,root,root) %{_mandir}/man5/bsmcoin.conf.5*



%changelog
* Fri Feb 26 2016 Alice Wonder <buildmaster@librelamp.com> - 0.12.0-2
- Rename Qt package from bsmcoin to bsmcoin-core
- Make building of the Qt package optional
- When building the Qt package, default to Qt5 but allow building
-  against Qt4
- Only run SELinux stuff in post scripts if it is not set to disabled

* Wed Feb 24 2016 Alice Wonder <buildmaster@librelamp.com> - 0.12.0-1
- Initial spec file for 0.12.0 release

# This spec file is written from scratch but a lot of the packaging decisions are directly
# based upon the 0.11.2 package spec file from https://www.ringingliberty.com/bsmcoin/
