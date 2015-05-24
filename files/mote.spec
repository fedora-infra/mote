%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from
%distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Name:     mote
Version:  0.0.2b2
Release:  1%{?dist}
Summary:  A meetbot log wrangler, providing a user-friendly interface for Fedora's logs.

# Group:
License:  GPLv2+
URL:      https://github.com/fedora-infra/mote
Source0:  %{name}-%{version}.tar.gz
# Source0:  https://github.com/fedora-infra/mote/archive/master.tar.gz

BuildRequires: python2-devel
BuildRequires: python-pip
BuildRequires: memcached
BuildRequires: libmemcached
BuildRequires: libmemcached-devel
BuildRequires: mod_wsgi
BuildRequires: python-flask
BuildRequires: python-fedora
BuildRequires: python-openid
BuildRequires: python-pylibmc
BuildRequires: python-openid-cla
BuildRequires: python-openid-teams
BuildRequires: python-requests
BuildRequires: python-dateutil
BuildRequires: python-beautifulsoup4
BuildRequires: python-fedora-flask

Requires: python2
Requires: python-pip
Requires: memcached
Requires: libmemcached
Requires: libmemcached-devel
Requires: mod_wsgi
Requires: python-flask
Requires: python-fedora
Requires: python-openid
Requires: python-pylibmc
Requires: python-openid-cla
Requires: python-openid-teams
Requires: python-requests
Requires: python-dateutil
Requires: python-beautifulsoup4
Requires: python-fedora-flask

%description
A Meetbot log wrangler, providing a user-friendly interface for Fedora Project's logs. Mote allows contributors to the Fedora Project to quickly search and find logs beneficial in keeping up to date with the project's activities.

%prep
%setup -q -n mote-master

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Install apache configuration file
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/
install -m 644 files/mote.conf $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/mote.conf

# Install mote configuration file
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mote
install -m 644 files/config.py $RPM_BUILD_ROOT/%{_sysconfdir}/mote/config.py

# Install mote wsgi file
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mote
install -m 644 files/mote.wsgi $RPM_BUILD_ROOT/%{_datadir}/mote/mote.wsgi

%files
%doc README.md
%dir %{_sysconfdir}/mote/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mote.conf
%config(noreplace) %{_sysconfdir}/mote/config.py
%config(noreplace) %{_sysconfdir}/mote/config.pyc
%config(noreplace) %{_sysconfdir}/mote/config.pyo
%{_bindir}/mote
%{_datadir}/mote/
%{python_sitelib}/mote/
%{python_sitelib}/mote*.egg-info

%changelog

* Sat May 23 2015 Chaoyi Zha <cydrobolt@fedoraproject.org>
- Update 0.0.2 Beta 2
- Multiple fixes to bugs blocking successful build
- Fixes to WSGI and folder access
- Removal of unneeded JSON data files
- Inclusion of needed templates and static files
- Fix httpd serve root
* Fri May 22 2015 Chaoyi Zha <cydrobolt@fedoraproject.org>
- Update 0.0.1 Alpha
- Initial Release
