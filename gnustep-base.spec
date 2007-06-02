%define build_doc 0

%define name    gnustep-base
%define version 1.15.0
%define release %mkrel 2
              
%define major 1.15

%define libname %mklibname %name %major
%define libnamedev %mklibname %name %major -d

%define gs_root %{_prefix}/GNUstep/System/Library

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
%if %{build_doc}
BuildRequires:	tetex-dvips
BuildRequires:	tetex-texi2html 
BuildRequires:	%name = %version
%endif
Requires:	gnustep-make >= 2.0.0
Provides:	libgnustep-base.so.%{major} libgnustep-base.so.%{major}()(64bit)
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

%prep  
%setup -q

%build
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{gs_root}/Makefiles/GNUstep.sh 
fi 
./configure --prefix=/%_prefix
make
%if %{build_doc}
make -C Documentation
%endif 

%install
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{gs_root}/Makefiles/GNUstep.sh 
fi
%makeinstall_std
bzme $RPM_BUILD_ROOT%{gs_root}/Documentation/man/man1/*.gz
bzme $RPM_BUILD_ROOT%{gs_root}/Documentation/man/man8/*.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post 
if [ $1 = 1 ]; then
#  if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
#     . %{gs_root}/Makefiles/GNUstep.sh 
#  fi
grep -q '^gdomap' /etc/services                                            \
   || (echo "gdomap 538/tcp # GNUstep distributed objects" >> /etc/services  \
       && echo "gdomap 538/udp # GNUstep distributed objects" >> /etc/services)
fi
echo "/usr/GNUstep/System/Libraries/ix86/linux-gnu/gnu-gnu-gnu" >> /etc/ld.so.conf 
/sbin/ldconfig

%postun 
if [ $1 = 0 ]; then
#  if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
#     . %{gs_root}/Makefiles/GNUstep.sh 
#  fi
mv -f /etc/services /etc/services.orig
grep -v "^gdomap 538" /etc/services.orig > /etc/services
rm -f /etc/services.orig
fi
grep -v "/usr/GNUstep/System/Libraries/ix86/linux-gnu/gnu-gnu-gnu" /etc/ld.so.conf > /etc/ld.so.conf.sauv
cp -f /etc/ld.so.conf.sauv /etc/ld.so.conf
/sbin/ldconfig

%files
%defattr (-,root,root)
%doc ANNOUNCE COPYING COPYING.LIB ChangeLog*
%doc NEWS README
%_prefix/GNUstep/System/Library/*
%_prefix/GNUstep/System/Tools/*
