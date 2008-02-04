%define modname fam
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 20_%{modname}.ini

Summary:	FAM (File Alteration Monitor) module for PHP
Name:		php-%{modname}
Version:	0.1
Release:	%mkrel 19
Group:		Development/PHP
URL:		http://pecl.php.net
License:	PHP License
Source0:	fam.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	fam-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This PHP module adds support for FAM (File Alteration Monitor). FAM monitors
files and directories, notifying interested applications of changes.

%prep

%setup -q -n fam

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS package.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
