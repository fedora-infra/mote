# There is no need to make our lives so difficult!
# %{!?python_sitelib: %global python_sitelib %(%{__python3} -c "from
# %distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Name:       mote
Version:    0.7.0
Release:    4%{?dist}
Summary:    A MeetBot log wrangler, providing a user-friendly interface for Fedora's logs

License:    GPLv2+
URL:        https://github.com/t0xic0der/mote
Source0:    https://github.com/t0xic0der/mote/archive/%{version}.tar.gz
BuildArch:  noarch

BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-mod_wsgi
BuildRequires: python3-flask
BuildRequires: python3-fedora
BuildRequires: python3-openid
# We do not make use of memcached anymore
# BuildRequires: python3-memcached
BuildRequires: python3-openid-cla
BuildRequires: python3-openid-teams
BuildRequires: python3-requests
BuildRequires: python3-dateutil
BuildRequires: python3-beautifulsoup4
BuildRequires: python3-fedora-flask
BuildRequires: python3-six
BuildRequires: python3-arrow
BuildRequires: fedmsg

# For RPM macros so we know where to install the service file.
BuildRequires: systemd

Requires: python3
Requires: python3-pip
Requires: python3-mod_wsgi
Requires: python3-flask
Requires: python3-fedora
Requires: python3-openid
# We do not make use of memcached anymore
# Requires: python3-memcached
Requires: python3-openid-cla
Requires: python3-openid-teams
Requires: python3-requests
Requires: python3-dateutil
Requires: python3-beautifulsoup4
Requires: python3-fedora-flask
Requires: python3-six
Requires: python3-arrow
Requires: fontawesome-fonts
Requires: fontawesome-fonts-web
Requires: fedmsg

%description
A Meetbot log wrangler, providing a user-friendly interface for
Fedora Project's logs. mote allows contributors to the Fedora Project to
quickly search and find logs beneficial in keeping up to date with the
project's activities.

%prep
%setup -q -n %{name}-%{version}
rm -rf *.egg*

%build
python3 setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python3 setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

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
rm -rf %{buildroot}/%{python3_sitelib}/mote/static/fonts

# Symlink font files
ln -s /usr/share/fonts/fontawesome %{buildroot}/%{python3_sitelib}/mote/static/fonts

# systemd service file for the fedmsg cache updater
%{__mkdir_p} %{buildroot}%{_unitdir}
%{__install} -pm644 files/mote-updater.service %{buildroot}%{_unitdir}/mote-updater.service

%files
%doc README.md
%{!?_licensedir:%global license %doc}
%license LICENSE
%dir %{_sysconfdir}/mote/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mote.conf
%config(noreplace) %{_sysconfdir}/mote/config.py
# Where are these files anyway?
# %config(noreplace) %{_sysconfdir}/mote/config.pyc
# %config(noreplace) %{_sysconfdir}/mote/config.pyo
%{_datadir}/mote/
%{_unitdir}/mote-updater.service
%{python3_sitelib}/mote/
%{python3_sitelib}/mote*.egg-info
%{_bindir}/mote-updater

%changelog
* Fri May 14 2021 Akashdeep Dhar <t0xic0der@fedoraproject.org> - 0.7.0
- Update 0.7.0
- Persisted copyright footer information in reduced width views
- Mote now makes use of Python 3
- Config.json location is now fixed when a JSON store is opted for
- Memcached is now no longer supported
- Changed the Select2 color to match the theme
- Text wrap is fixed to stay constrained on the viewport

* Tue May 2 2017 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.6.2
- Update 0.6.2
- Fix latest meeting button
- Add missing import for soke in __init__ that may have been causing uncaught 500s

* Tue Mar 28 2017 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.6.1
- Update 0.6.1
- Fix exception logging
- Add "deep link" #94
- Implement more descriptive team icons
- Other small bug fixes and improvements

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Apr 9 2016 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.5.2
- Update 0.5.2
- Fix datagrepper access in staging
- Fix meeting serving when symbols are included in the filename

* Tue Feb 23 2016 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.5.1
- Update 0.5.1
- Tighten wide try/except clauses
- Add latest meetings section on main page
- Defer JS loading
- Remove mote console script entry point
- Fix scroll-to-line within log viewer

* Sat Jan 30 2016 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.4.3
- Update 0.4.3
- Several updates to name and group mapping files
- Added unit tests
- Removed redundancy within code
- Added proper name and group map aliasing
- Improved regex to avoid mistakes while being lenient towards files which skew

* Sat Oct 24 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.4.2
- Update 0.4.2
- Use event binding rather than "onclick"
- README improvements and general bugfixes

* Mon Sep 7 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.4.1
- Update 0.4.1
- Add modal permalink option
- Fix full log links in modals and full views
- Other bug fixes

* Sun Jul 12 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.3.4
- Update 0.3.4
- Catch links with trailing slash, e.g blockerbug date links

* Tue Jun 23 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.3.3
- Update 0.3.3
- Fix mote-updater
- Catch legacy date links

* Thu Jun 18 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.3.2
- Update 0.3.2
- Fix mote-updater
- Fix weird configuration import issue

* Thu Jun 18 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.3.1
- Update 0.3.1
- List most recent results first
- Use GET instead of POST in meeting log requests
- Run teams script after meeting in order to fix slow sync
- Add loading icon while waiting for modal loading
- Other small bugfixes

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2b1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Chaoyi Zha <cydrobolt@fedoraproject.org> - 0.2.1b1
- Update 0.2.1 Beta 1
- Add Fedmsg listener, refresh cache when new meeting ends

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