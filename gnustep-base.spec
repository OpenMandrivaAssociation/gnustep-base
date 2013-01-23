%define	build_doc 1

%define major 	1.24
%define libname %mklibname %{name} %major
%define develname %mklibname %{name} -d

Summary: 	GNUstep Base package
Name: 		gnustep-base
Version: 	1.24.0
Release: 	3
Source0: 	http://ftpmain.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
Source100:	gnustep-base.rpmlintrc
Patch1:		gnustep-base-1.24.0.libxml.patch
License: 	LGPLv2+
Group: 		Development/Other
URL:		http://www.gnustep.org/
BuildRequires:	gnustep-make >= 2.6.2-3
BuildRequires:	gcc-objc
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	binutils-devel
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(icu-i18n)
%if %build_doc
BuildRequires:	tetex-dvips
BuildRequires:	texi2html
BuildRequires:	texinfo
%endif
Requires:	gnustep-make >= 2.6.2-3

%description
The GNUstep Base Library is a powerful fast library of general-purpose,
non-graphical Objective C classes, inspired by the superb OpenStep API but
implementing Apple and GNU additions to the API as well.  It includes for
example classes for unicode strings, arrays, dictionaries, sets, byte
streams, typed coders, invocations, notifications, notification dispatchers,
scanners, tasks, files, networking, threading, remote object messaging
support (distributed objects), event loops, loadable bundles, attributed
unicode strings, xml, mime, user defaults. This package includes development
headers too.

%package -n     %{libname}
Summary:        Dynamic libraries from %{name}
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n     %{develname}
Summary:        Header files and static libraries from %{name}
Group:          Development/Other
Requires:       %{libname} >= %{version}
Provides:       %{name}-devel = %{version}-%{release} 
Obsoletes:      %{name}-devel

%description -n %{develname}
Libraries and includes files for developing programs based on %{name}.

%prep  
%setup -q
%apply_patches

%build
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{_datadir}/GNUstep/Makefiles/GNUstep.sh
fi
%define __cputoolize /bin/true
# FIXME We force ld.bfd because of a gold bug last seen in 2.23.51.0.8, causing
# the build to fail on x86_32. -fuse-ld=bfd should be removed as soon as this
# is fixed.
LDFLAGS="%ldflags -fuse-ld=bfd" %configure2_5x --with-default-config=/etc/GNUstep/GNUstep.conf --with-installation-domain=SYSTEM --enable-setuid-gdomap
%make GNUSTEP_INSTALLATION_DOMAIN=SYSTEM
%if %build_doc
export LD_LIBRARY_PATH="${RPM_BUILD_DIR}/%{name}-%{version}/Source/obj:${LD_LIBRARY_PATH}"
make -C Documentation
%endif

%install
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{_datadir}/GNUstep/Makefiles/GNUstep.sh
fi
%makeinstall_std GNUSTEP_INSTALLATION_DOMAIN=SYSTEM
%if %build_doc
cd Documentation
%makeinstall_std GNUSTEP_INSTALLATION_DOMAIN=SYSTEM
%endif
mkdir -p $RPM_BUILD_ROOT%_libdir/GNUstep/Libraries/Resources

%post 
grep -q '^gdomap' /etc/services                                            \
   || (echo "gdomap 538/tcp # GNUstep distributed objects" >> /etc/services  \
       && echo "gdomap 538/udp # GNUstep distributed objects" >> /etc/services)

%postun 
mv -f /etc/services /etc/services.orig
grep -v "^gdomap 538" /etc/services.orig > /etc/services
rm -f /etc/services.orig

%files
%doc NEWS README
%{_bindir}/*
%{_libdir}/GNUstep
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_infodir}/*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{develname}
%doc ANNOUNCE COPYING COPYING.LIB ChangeLog*
%{_includedir}/*
%{_datadir}/GNUstep/*
%{_libdir}/*.so


%changelog
* Fri May 11 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.24.0-2
+ Revision: 798266
- Fix rpmlint braindamage

* Thu May 10 2012 Lev Givon <lev@mandriva.org> 1.24.0-1
+ Revision: 798130
- Fix major, remove old tarball.

  + Jon Dill <dillj@mandriva.org>
    - rebuild against new version of libffi4

* Tue Aug 03 2010 Funda Wang <fwang@mandriva.org> 1.20.1-1mdv2011.0
+ Revision: 565259
- New version 1.20.1

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 1.18.0-4mdv2010.1
+ Revision: 537371
- rebuild

* Wed Nov 25 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.18.0-3mdv2010.1
+ Revision: 469882
- rebuild to statically link against libbfd

* Sat Mar 14 2009 Funda Wang <fwang@mandriva.org> 1.18.0-2mdv2009.1
+ Revision: 354830
- fix file list
- fix str fmt
- rebuild for new binutils
- protect libmajor

* Wed Jan 07 2009 Funda Wang <fwang@mandriva.org> 1.18.0-1mdv2009.1
+ Revision: 326909
- New version 1.18.0

* Thu Dec 25 2008 Michael Scherer <misc@mandriva.org> 1.16.5-2mdv2009.1
+ Revision: 318451
- rebuild for new py^W binutils

* Mon Dec 01 2008 Funda Wang <fwang@mandriva.org> 1.16.5-1mdv2009.1
+ Revision: 308687
- New version 1.16.5

* Fri Nov 14 2008 Funda Wang <fwang@mandriva.org> 1.16.4-1mdv2009.1
+ Revision: 303304
- New version 1.16.4
- procfs merged upstream

* Wed Aug 20 2008 Funda Wang <fwang@mandriva.org> 1.16.3-3mdv2009.0
+ Revision: 274214
- add fix for procfs detection
- New version 1.16.3
- fix sh path
- New version 1.16.2
- BR gnutls and binutils
- fix building
- add info files
- New version 1.16.1

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Franck Villaume <fvill@mandriva.com>
    - new version 1.15.3

* Tue Jan 22 2008 Funda Wang <fwang@mandriva.org> 1.15.2-1mdv2008.1
+ Revision: 156313
- New version 1.15.2

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Aug 03 2007 Austin Acton <austin@mandriva.org> 1.15.0-4mdv2008.0
+ Revision: 58679
- buildrequires texinfo when building docs
- rebuild to get documentation

* Tue Jul 10 2007 Austin Acton <austin@mandriva.org> 1.15.0-3mdv2008.0
+ Revision: 51102
- rebuild for new locations
- move to FHS structure
- re libify; non-versioned devel
- drop explicit provides hack

* Sat Jun 02 2007 Austin Acton <austin@mandriva.org> 1.15.0-2mdv2008.0
+ Revision: 34756
- setup for doc build
- explicit provides (Charles Edwards)

* Wed May 30 2007 Austin Acton <austin@mandriva.org> 1.15.0-1mdv2008.0
+ Revision: 32872
- new version
- redo most of spec file for simplicity
- disable documentation, temporarily


* Mon Jun 19 2006 Charles A Edwards <eslrahc@mandriva.org> 1.12.0-2mdv2007.0
- post postrun ldconfig

* Mon Jun 19 2006 Charles A Edwards <eslrahc@mandriva.org> 1.12.0-1mdv2007.0
- 1.12.0
- mkrel
- bump major
- add doc build

* Mon Apr 04 2005 Charles A Edwards <eslrahc@mandrake.org> 1.10.2-1mdk
- 1.10.2
- mv headers to devel pkg
- use _prefix
- bzip2 changelog 1 & 2 and include in Doc
- add Examples as Doc in devel pkg

* Sat Nov 06 2004 Charles A Edwards <eslrahc@mandrake.org> 1.10.1-3mdk
- exclude so from main pkg

* Thu Nov 04 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.10.1-1mdk
- 1.10.1

* Fri Sep 10 2004 Charles A Edwards <eslrahc@mandrake.org> 1.10.0-2mdk
- fix Major and Provides

* Fri Sep 10 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.10.0-1mdk
- 1.10.0

* Fri Aug 08 2003 Marcel Pol <mpol@gmx.net> 1.6.0-2mdk
- rebuild
- setup -q

