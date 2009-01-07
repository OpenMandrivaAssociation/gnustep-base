%define name    gnustep-base
%define version 1.18.0
%define release %mkrel 1

%define	build_doc 1

%define major 	1.18

%define libname %mklibname %name %major
%define libnamedev %mklibname %name -d

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source: 	http://ftpmain.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
License: 	LGPLv2+
Group: 		Development/Other
Summary: 	GNUstep Base package
URL:		http://www.gnustep.org/
BuildRequires:	gnustep-make libffcall-devel
BuildRequires:	gcc-objc
BuildRequires:	libxml2-devel libxslt-devel zlib-devel
BuildRequires:	libopenssl-devel gnutls-devel
BuildRequires:	binutils-devel
%if %build_doc
BuildRequires:	tetex-dvips
BuildRequires:	tetex-texi2html
BuildRequires:	texinfo
%endif
Requires:	gnustep-make >= 2.0.0
BuildRoot: 	%{_tmppath}/%{name}-%{version}

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
Summary:        Dynamic libraries from %name
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %name.

%package -n     %{libnamedev}
Summary:        Header files and static libraries from %name
Group:          Development/Other
Requires:       %{libname} >= %{version}
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release} 
Obsoletes:      %name-devel

%description -n %{libnamedev}
Libraries and includes files for developing programs based on %name.

%prep  
%setup -q

%build
autoreconf -vi
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{_datadir}/GNUstep/Makefiles/GNUstep.sh
fi
%define __cputoolize /bin/true
%configure2_5x --with-default-config=/etc/GNUstep/GNUstep.conf
make
%if %build_doc
export LD_LIBRARY_PATH="${RPM_BUILD_DIR}/%name-%version/Source/obj:${LD_LIBRARY_PATH}"
make -C Documentation
%endif

%install
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{_datadir}/GNUstep/Makefiles/GNUstep.sh
fi
%makeinstall_std
%if %build_doc
cd Documentation
%makeinstall_std
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post 
grep -q '^gdomap' /etc/services                                            \
   || (echo "gdomap 538/tcp # GNUstep distributed objects" >> /etc/services  \
       && echo "gdomap 538/udp # GNUstep distributed objects" >> /etc/services)

%postun 
mv -f /etc/services /etc/services.orig
grep -v "^gdomap 538" /etc/services.orig > /etc/services
rm -f /etc/services.orig

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr (-,root,root)
%doc ANNOUNCE COPYING COPYING.LIB ChangeLog*
%doc NEWS README
%{_bindir}/*
%{_prefix}/lib/GNUstep
%{_mandir}/man1/*
%{_mandir}/man8/*
%_infodir/*

%files -n %{libname}
%defattr(-,root,root)
%{_prefix}/lib/*.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/GNUstep/*
%{_prefix}/lib/*.so
