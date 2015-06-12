%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from
%distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Name:       mote
Version:    0.1.2b1
Release:    1%{?dist}
Summary:    A MeetBot log wrangler, providing a user-friendly interface for Fedora's logs

License:    GPLv2+
URL:        https://github.com/fedora-infra/mote
Source0:    https://github.com/fedora-infra/mote/archive/%{version}.tar.gz
BuildArch:  noarch

BuildRequires: python2-devel
BuildRequires: python-pip
BuildRequires: mod_wsgi
BuildRequires: python-flask
BuildRequires: python-fedora
BuildRequires: python-openid
BuildRequires: python-memcached
BuildRequires: python-openid-cla
BuildRequires: python-openid-teams
BuildRequires: python-requests
BuildRequires: python-dateutil
BuildRequires: python-beautifulsoup4
BuildRequires: python-fedora-flask

Requires: python2
Requires: python-pip
Requires: mod_wsgi
Requires: python-flask
Requires: python-fedora
Requires: python-openid
Requires: python-memcached
Requires: python-openid-cla
Requires: python-openid-teams
Requires: python-requests
Requires: python-dateutil
Requires: python-beautifulsoup4
Requires: python-fedora-flask
Requires: fontawesome-fonts
Requires: fontawesome-fonts-web

%description
A Meetbot log wrangler, providing a user-friendly interface for
Fedora Project's logs. mote allows contributors to the Fedora Project to
quickly search and find logs beneficial in keeping up to date with the
project's activities.

%prep
%setup -q -n %{name}-%{version}
rm -rf *.egg*

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

# Remove bundled font files
rm -rf %{buildroot}/%{python_sitelib}/mote/static/fonts

# Symlink font files
ln -s /usr/share/fonts/fontawesome %{buildroot}/%{python_sitelib}/mote/static/fonts

%files
%doc README.md
%{!?_licensedir:%global license %doc}
%license LICENSE
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
* Fri Jun 12 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.1.2b1
- Update 0.1.2 Beta 1
- Remove some external font and JS dependencies
- Add permalink button and fix hardcoded "original" button
- Fix small typo on front page
- Other small bugfixes
* Thu Jun 11 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.1.1b1
- Update 0.1.1 Beta 1
- Added JSON filestore as backup to memcached store
- Made memcached store optional
* Fri Jun 5 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.0.6b2
- Update 0.0.6 Beta 2
- Move to FontAwesome CDN
- Set cache expiry time and recreate cache when it is expired
- Small bugfixes
* Thu May 28 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.0.5b1
- Update 0.0.5 Beta 1
- Remove bundled fontawesome fonts, symlink to appropriate font
- Clean up RPM spec, fix issues
* Tue May 26 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.0.4b2
- Update 0.0.4 Beta 2
- Migrate to python-memcached from pylibmc
* Sat May 23 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.0.3b1
- Update 0.0.3 Beta 1
- Multiple fixes to bugs blocking successful build
- Fixes to WSGI and folder access
- Removal of unneeded JSON data files
- Inclusion of needed templates and static files
- Fix httpd serve root
* Fri May 22 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.0.1a1
- Update 0.0.1 Alpha
- Initial Release
