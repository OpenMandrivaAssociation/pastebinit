Name:           pastebinit
Version:        1.7.0
Release:        1
Summary:        Send anything you want directly to a pastebin from the command line

Group:          System/Networking
License:        GPLv2+
URL:            https://launchpad.net/pastebinit
#Source0:        https://github.com/felixonmars/pastebinit/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Source0:        https://github.com/pastebinit/pastebinit/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz

#
# supress useless dependancy to lsb_release, folow the comportement of
# upstream by using per default fpaste.org.
# this patch musn't be push to the upstream
#
#Patch0:         pastebinit-1.4.1-mga-delete-dependancy-to-lsb_release.patch
BuildArch:      noarch
BuildRequires:  docbook-style-xsl 
BuildRequires:  xsltproc 
BuildRequires:  gettext
Requires:       python-configobj
Obsoletes:      pastebin

%description
A software that lets you send anything you want directly to a
pastebin from the command line.  This software lets you send a file
or simply the result of a command directly to the pastebin you want
(if it's supported) and gives you the URL in return.

%prep
%setup -q
#autopatch -p1
# Change the location of pastebin config file from /etc/pastebin.d/
# to /usr/share/pastebinit/ (unappropriate dir. name "pastebinit.d"
# + FHS)
# See https://bugs.launchpad.net/pastebinit/+bug/621923
#
sed -i "s|pastebin.d|%{name}|g" %{name} README

%build
# Generate the man page from docbook xml
xsltproc -''-nonet %{_datadir}/sgml/docbook/xsl-stylesheets*/manpages/docbook.xsl pastebinit.xml

# Build translation
pushd po
%make
popd

%install
mkdir -p %{buildroot}%{_datadir}/
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/

cp -a pastebin.d %{buildroot}%{_datadir}
mv %{buildroot}%{_datadir}/pastebin.d/ %{buildroot}%{_datadir}/%{name}/

install -m 0755 -D -p %{name} %{buildroot}%{_bindir}/%{name}
install -m 0644 -D -p %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

# Install translations
pushd po
cp -a mo %{buildroot}%{_datadir}/locale/
popd

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_datadir}/%{name}/
%dir %{_sysconfdir}/%{name}/
%doc README COPYING
