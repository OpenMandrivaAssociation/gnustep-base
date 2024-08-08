%define	build_doc 0

%define major 	%(echo %{version} |cut -d. -f1-2)
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d
%define underscoredversion %(echo %{version} |sed -e 's,\\.,_,g')

# -Os / -Oz fails because of the float vs. _Float32 issue -- override it
%global optflags %{optflags} -O3

Summary: 	GNUstep Base package
Name: 		gnustep-base
Version: 	1.30.0
Release: 	1
License: 	LGPLv2+
Group: 		Development/Other
Url:		http://www.gnustep.org/
Source0: 	https://github.com/gnustep/libs-base/releases/download/base-%{underscoredversion}/gnustep-base-%{version}.tar.gz
Source100:	gnustep-base.rpmlintrc

BuildRequires:	gnustep-make >= 2.6.2-3
BuildRequires:	pkgconfig(libobjc)
BuildRequires:	binutils-devel
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(icu-i18n)
%if %build_doc
BuildRequires:	tetex-dvips
BuildRequires:	texi2html
BuildRequires:	texinfo
%endif
BuildRequires:	which
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
%define oldlibname %mklibname %{name} 1.28
Obsoletes:	%{oldlibname} < %{EVRD}

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n     %{devname}
Summary:        Header files and static libraries from %{name}
Group:          Development/Other
Requires:       %{name} >= %{version}-%{release}
Requires:       %{libname} >= %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release} 

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%prep  
%autosetup -p1

%build
# must match gnustep-make
export CC=`gnustep-config --variable=CC -fobjc-arc -fno-lto`
export CXX=`gnustep-config --variable=CXX -fobjc-arc -fno-lto`

if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{_datadir}/GNUstep/Makefiles/GNUstep.sh
fi
%define __cputoolize /bin/true
%configure \
	--with-default-config=/etc/GNUstep/GNUstep.conf \
	--with-installation-domain=SYSTEM \
	--enable-setuid-gdomap || :

echo "Configure failed. config.log:"
cat config.log
exit 1

# messages=yes enables verbose build [like ninja -v]
%make_build GNUSTEP_INSTALLATION_DOMAIN=SYSTEM messages=yes
%if %build_doc
export LD_LIBRARY_PATH="${RPM_BUILD_DIR}/%{name}-%{version}/Source/obj:${LD_LIBRARY_PATH}"
%make_build -C Documentation
%endif

%install
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{_datadir}/GNUstep/Makefiles/GNUstep.sh
fi
%make_install GNUSTEP_INSTALLATION_DOMAIN=SYSTEM
%if %build_doc
cd Documentation
%make_install GNUSTEP_INSTALLATION_DOMAIN=SYSTEM
%endif
mkdir -p %{buildroot}%{_libdir}/GNUstep/Libraries/Resources

%post 
grep -q '^gdomap' /etc/services                                            \
	|| (echo "gdomap 538/tcp # GNUstep distributed objects" >> /etc/services  \
	&& echo "gdomap 538/udp # GNUstep distributed objects" >> /etc/services)

%postun 
mv -f /etc/services /etc/services.orig
grep -v "^gdomap 538" /etc/services.orig > /etc/services
rm -f /etc/services.orig

%files
%doc NEWS
%{_bindir}/*
%{_libdir}/GNUstep
%{_mandir}/man1/*
%{_mandir}/man8/*
%if %build_doc
%{_infodir}/*
%endif

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%doc ANNOUNCE COPYING COPYING.LIB ChangeLog*
%{_includedir}/*
%{_datadir}/GNUstep/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
