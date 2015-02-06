%define modname fam
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 20_%{modname}.ini

Summary:	File Alteration Monitor Functions
Name:		php-%{modname}
Version:	5.0.1
Release:	24
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/fam/
Source0:	http://pecl.php.net/get/fam-%{version}.tgz
Patch0:		fam-5.0.1-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	fam-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
FAM monitors files and directories, notifying interested applications of
changes. A PHP script may specify a list of files for FAM to monitor using
the functions provided by this extension. The FAM process is started when the
first connection from any application to it is opened. It exits after all
connections to it have been closed. This PHP module adds support for FAM
(File Alteration Monitor). FAM monitors files and directories, notifying
interested applications of changes.

%prep

%setup -q -n fam-%{version}
[ "../package.xml" != "/" ] && mv -f ../package.xml .

%patch0 -p0

# fix version
perl -pi -e "s|^#define PHP_FAM_VERSION .*|#define PHP_FAM_VERSION \"%{version}\"|g" php_fam.h

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


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-23mdv2012.0
+ Revision: 797100
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-22
+ Revision: 761224
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-21
+ Revision: 696417
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-20
+ Revision: 695391
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-19
+ Revision: 646632
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-18mdv2011.0
+ Revision: 629787
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-17mdv2011.0
+ Revision: 628098
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-16mdv2011.0
+ Revision: 600481
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-15mdv2011.0
+ Revision: 588775
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-14mdv2010.1
+ Revision: 514536
- rebuilt for php-5.3.2

* Sun Feb 21 2010 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-13mdv2010.1
+ Revision: 509076
- rebuild

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-12mdv2010.1
+ Revision: 485257
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-11mdv2010.1
+ Revision: 468084
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-10mdv2010.0
+ Revision: 451214
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:5.0.1-9mdv2010.0
+ Revision: 397518
- Rebuild

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-8mdv2010.0
+ Revision: 375357
- rebuilt against php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-7mdv2009.1
+ Revision: 346423
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-6mdv2009.1
+ Revision: 341506
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-5mdv2009.1
+ Revision: 321732
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-4mdv2009.1
+ Revision: 310215
- rebuilt against php-5.2.7

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-3mdv2009.0
+ Revision: 235817
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-2mdv2009.0
+ Revision: 200106
- rebuilt against php-5.2.6

* Wed Apr 30 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.0.1-1mdv2009.0
+ Revision: 199433
- fix build
- 5.0.1

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-19mdv2008.1
+ Revision: 161963
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-18mdv2008.1
+ Revision: 107561
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-17mdv2008.0
+ Revision: 77454
- rebuilt against php-5.2.4

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-16mdv2008.0
+ Revision: 64298
- use the new %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-15mdv2008.0
+ Revision: 39379
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-14mdv2008.0
+ Revision: 33774
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-13mdv2008.0
+ Revision: 21023
- rebuilt against new upstream version (5.2.2)


* Fri Feb 09 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1-12mdv2007.0
+ Revision: 118554
- rebuilt against new upstream php version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-11mdv2007.0
+ Revision: 78159
- fix deps

* Tue Nov 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-10mdv2007.1
+ Revision: 77342
- rebuilt for php-5.2.0

* Thu Nov 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-9mdv2007.1
+ Revision: 75212
- Import php-fam

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-9
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-8mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-7mdk
- rebuilt for php-5.1.4

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-6mdk
- rebuilt for php-5.1.3

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-5mdk
- new group (Development/PHP) and iurt rebuild

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-4mdk
- rebuilt against php-5.1.2

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-3mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-2mdk
- rebuilt against php-5.1.0

* Thu Nov 03 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-1mdk
- rebuilt against php-5.1.0RC4
- fix versioning

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.1-0.RC1.2mdk
- rebuilt to provide a -debug package too

* Wed Sep 21 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.1-0.RC1.1mdk
- rebuilt against php-5.1.0RC1
- the source lives in pecl now (CVS)

* Wed Sep 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.5-1mdk
- rebuilt against php-5.0.5 (Major security fixes)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3-4mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3-3mdk
- rebuilt against a non hardened-php aware php lib

* Sun Jan 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3-2mdk
- rebuild due to hardened-php-0.2.6

* Fri Dec 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3-1mdk
- rebuilt for php-5.0.3

* Sat Sep 25 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.2-1mdk
- rebuilt for php-5.0.2

* Sun Aug 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.1-1mdk
- rebuilt for php-5.0.1

* Wed Aug 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.0-1mdk
- initial mandrake package

