%define name    gnustep-base
%define version 1.15.0
%define release %mkrel 3

# haven't found a hack to make the documentaion build without DTDs installed
# so, requires itself to build currently
%define	build_doc 0

%define major 	1.15

%define libname %mklibname %name %major
%define libnamedev %mklibname %name -d

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source: 	%{name}-%{version}.tar.bz2
License: 	LGPL
Group: 		Development/Other
Summary: 	GNUstep Base package
URL:		http://www.gnustep.org/

BuildRequires:	gnustep-make libffcall-devel
BuildRequires:	gcc-objc
BuildRequires:	libxml2-devel libxslt-devel zlib-devel
BuildRequires:	libopenssl-devel
%if %build_doc
BuildRequires:	tetex-dvips
BuildRequires:	tetex-texi2html
BuildRequires:	%name
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
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{_sysconfdir}/profile.d/GNUstep.sh 
fi 
./configure --prefix=/%_prefix
make
%if %build_doc
make -C Documentation
%endif

%install
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{_sysconfdir}/profile.d/GNUstep.sh 
fi
%makeinstall_std
bzme $RPM_BUILD_ROOT/%{_mandir}/man1/*.gz
bzme $RPM_BUILD_ROOT/%{_mandir}/man8/*.gz

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

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr (-,root,root)
%doc ANNOUNCE COPYING COPYING.LIB ChangeLog*
%doc NEWS README
%{_bindir}/*
%{_prefix}/lib/GNUstep
%{_mandir}/man1/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%{_prefix}/lib/*.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/GNUstep/Makefiles/Additional/*
%{_prefix}/lib/*.so

