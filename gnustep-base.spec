%define gs_root         %{_prefix}/GNUstep/System
%define gs_install_dir  %{_prefix}/GNUstep/System
%define name         	gnustep-base
%define version      	1.12.0
%define rel                 2
              
##CAE needs gnusteb-base lib to build
%define build_docs 0

%define major 1.12

%define libname %mklibname %name %major
%define libnamedev %mklibname %name %major -d

Name: 		%{name}
Version: 	%{version}
Prefix: 	%{gs_install_dir}
Release: 	%mkrel %{rel}
Source: 	%{name}-%{version}.tar.bz2
License: 	LGPL
Group: 		Development/Other
Summary: 	GNUstep Base package
URL:		http://www.gnustep.org/
BuildRequires:	gnustep-make libffcall-devel
BuildRequires:	gcc-objc
BuildConflicts:  libgnustep-base < %{version}
%if %{build_docs}
BuildRequires:	tetex-dvips
BuildRequires:	tetex-texi2html 
BuildRequires:  %libname = %{version}
%endif
Requires:	gnustep-make >= 1.5.1, gcc-objc
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

%package -n %libname
Summary: GNUstep Base library package
Group: Development/Other
Requires: %name
Provides: libgnustep-base = %{version}
Provides: libgnustep-base.so.%{major}

%description -n %libname
The GNUstep Base Library is a powerful fast library of general-purpose,
non-graphical Objective C classes, inspired by the superb OpenStep API but
implementing Apple and GNU additions to the API as well.  It includes for
example classes for unicode strings, arrays, dictionaries, sets, byte
streams, typed coders, invocations, notifications, notification dispatchers,
scanners, tasks, files, networking, threading, remote object messaging
support (distributed objects), event loops, loadable bundles, attributed
unicode strings, xml, mime, user defaults. This package includes development
headers too.

%package -n %libnamedev
Summary: GNUstep Base library package
Group: Development/Other
Requires: %libname = %version
Provides: libgnustep-base-devel = %{version}
Conflicts: libgnustep-base-devel < %{version}

%description -n %libnamedev
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
rm -rf $RPM_BUILD_ROOT
%setup -q -n %{name}-%{version}

%build
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{gs_root}/Makefiles/GNUstep.sh 
fi 
CFLAGS="$RPM_OPT_FLAGS" 
./configure --prefix=%{gs_root} --enable-pass-arguments
%make

%if %{build_docs} 
%{__make} -C Documentation
%endif

%install
 
if [ -z "$GNUSTEP_SYSTEM_ROOT" ]; then
  . %{gs_root}/Makefiles/GNUstep.sh 
fi

%make INSTALL_ROOT_DIR=$RPM_BUILD_ROOT \
  GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{gs_install_dir} \
  filelist=yes install 

gunzip -d $RPM_BUILD_ROOT%{gs_root}/Library/Documentation/man/man1/*.gz
gunzip -d $RPM_BUILD_ROOT%{gs_root}/Library/Documentation/man/man8/*.gz
bzip2 $RPM_BUILD_ROOT%{gs_root}/Library/Documentation/man/man1/*
bzip2 $RPM_BUILD_ROOT%{gs_root}/Library/Documentation/man/man8/*
bzip2 ChangeLog.*

%if %{build_docs}
mkdir -p  ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/Base \
               ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/BaseAdditions \
               ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/BaseTools \                             ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/General \
               ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/HtmlNav \
               ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/ReleaseNotes \
               ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/manual
mv Documentation/Base/*.html ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/Base
mv Documentation/BaseAdditions/*.html ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/BaseAdditions
mv Documentation/BaseTools/*.html ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/BaseTools
mv Documentation/General/General/*.html ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/General
mv Documentation/HtmlNav/*.html ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/HtmlNav
mv Documentation/HtmlNav/*.jpg ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/HtmlNav
mv Documentation/ReleaseNotes/*.html ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/ReleaseNotes
mv Documentation/manual/*.html ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/manual
mv Documentation/manual/*.info ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/manual
mv Documentation/manual/*.pdf ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/manual
mv Documentation/manual/manual ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation/manual
mv Documentation/*.info ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation
mv Documentation/*.pdf ${RPM_BUILD_ROOT}%{gs_root}/Library/Documentation
%endif

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
%post -n %{libname} -p /sbin/ldconfig

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
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr (-,root,root)
%doc ANNOUNCE COPYING COPYING.LIB ChangeLog* INSTALL
%doc NEWS README
%_prefix/GNUstep/System/Library/Makefiles
%_prefix/GNUstep/System/Library/Libraries
%exclude %_prefix/GNUstep/System/Library/Libraries/*.so.*
%exclude %_prefix/GNUstep/System/Library/Libraries/*.so
%_prefix/GNUstep/System/Library/Bundles
%_prefix/GNUstep/System/Library/DTDs
%_prefix/GNUstep/System/Library/Documentation
%_prefix/GNUstep/System/Tools

%files -n %libname
%defattr (-, root, root)
%_prefix/GNUstep/System/Library/Libraries/*.so.*

%files -n %libnamedev
%defattr (-, root, root)
%doc Examples/*
%_prefix/GNUstep/System/Library/Libraries/*.so
%_prefix/GNUstep/System/Library/Headers

