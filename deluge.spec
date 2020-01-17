Name:  deluge
Version:  2.0.3
Release:  1.1
Summary:  A GTK+ BitTorrent client with support for DHT, UPnP, and PEX
License:  GPLv3 with exceptions
URL:      http://deluge-torrent.org/
Source0:  http://download.deluge-torrent.org/source/2.0/%{name}-%{version}.tar.xz
Source2:  deluge-daemon.service
Source3:  deluge-web.service

# No noarch because we are using bundle binaries modules python3
# BuildArch:  noarch
BuildRequires: python3-dev
BuildRequires: pip
BuildRequires: openssl-dev
BuildRequires: geoip-dev

#Requires: python3
Requires: openssl
Requires: libtorrent-rasterbar
Requires: geoip

Requires: pyxdg-python3
Requires: six-python3
Requires: zope.interface-python3
Requires: chardet-python3
Requires: setproctitle-python3
Requires: Pillow-python3
Requires: dbus-python-python3
Requires: distro-python3
Requires: Mako-python3
Requires: rencode-python3

%description
Deluge is a new BitTorrent client, created using Python and GTK+. It is
intended to bring a native, full-featured client to Linux GTK+ desktop
environments such as GNOME and XFCE. It supports features such as DHT
(Distributed Hash Tables), PEX (µTorrent-compatible Peer Exchange), and UPnP
(Universal Plug-n-Play) that allow one to more easily share BitTorrent data
even from behind a router with virtually zero configuration of port-forwarding.


%prep
%setup -n deluge-2.0.3


%build
#/usr/bin/2to3
#/usr/bin/2to3-3.8
#/usr/bin/2to3-3.7

unset http_proxy
unset no_proxy 
unset https_proxy

python3 setup.py build

%install

unset http_proxy
unset no_proxy 
unset https_proxy

# http://dev.deluge-torrent.org/ticket/2034
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-daemon.service
install -m644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}-web.service
mkdir -p %{buildroot}/var/lib/%{name}

#/usr/bin/2to3 setup.py install -O1 --skip-build --root %{buildroot}
python3 -tt setup.py build  install --root=%{buildroot}


python3 -m pip install --user pyOpenSSL GeoIP
pushd $HOME
cp -rf .local/lib/python3.8/site-packages/* %{buildroot}/usr/lib/python3.8/site-packages/
popd


%files
/usr/bin/deluge
/usr/bin/deluge-console
/usr/bin/deluge-gtk
/usr/bin/deluge-web
/usr/bin/deluged
/usr/lib/python3.8/site-packages/deluge-2.0.3-py*.egg-info/*
/usr/lib/python3.8/site-packages/deluge/
/usr/share/icons/hicolor/*/apps/deluge*.png
/usr/share/icons/hicolor/*/apps/deluge.svg
/usr/share/man/man1/deluge-console.1
/usr/share/man/man1/deluge-gtk.1
/usr/share/man/man1/deluge-web.1
/usr/share/man/man1/deluge.1
/usr/share/man/man1/deluged.1
/usr/share/pixmaps/deluge.png

# Our bundle python3 modules
/usr/lib/python3.8/site-packages/GeoIP-1.3.2-py*.egg-info/*
/usr/lib/python3.8/site-packages/GeoIP.cpython-38-x86_64-linux-gnu.so

%post 
%systemd_post deluge-daemon.service
%systemd_post deluge-web.service

%preun 
%systemd_preun deluge-daemon.service
%systemd_preun deluge-web.service

%postun 
%systemd_postun_with_restart deluge-daemon.service
%systemd_postun_with_restart deluge-web.service

%changelog
* Mon Jan 13 2020 David Va <davidva AT tuta DOT io> - 2.0.3-1.1
* Initial build
