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
License: 	LGPLv2+
Group: 		Development/Other
URL:		http://www.gnustep.org/
BuildRequires:	gnustep-make >= 2.6.2-3 pkgconfig(libffi)
BuildRequires:	gcc-objc
BuildRequires:	libxml2-devel libxslt-devel zlib-devel
BuildRequires:	libopenssl-devel gnutls-devel
BuildRequires:	binutils-devel
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
%configure2_5x --with-default-config=/etc/GNUstep/GNUstep.conf --with-installation-domain=SYSTEM --enable-setuid-gdomap
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
