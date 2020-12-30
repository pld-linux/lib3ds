#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	The 3D Studio File Format Library
Summary(pl.UTF-8):	Biblioteka obsługująca format plików 3D Studio
Name:		lib3ds
Version:	1.3.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/lib3ds/%{name}-%{version}.zip
# Source0-md5:	2572f7b0f29b591d494c1a0658b35c86
URL:		http://lib3ds.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake >= 1.4
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
lib3ds is a free alternative to Autodesk's 3DS File Toolkit for
handling 3DS files. It's main goal is to simplify the creation of 3DS
import and export filters.

This project is not related in any form to Autodesk. The library is
based on unofficial information about the 3DS format found on the web.

%description -l pl.UTF-8
lib3ds to wolnodostępna alternatywa dla 3DS File Toolkit Autodeska do
obsługi plików 3DS. Głównym celem biblioteki jest uproszczenie
tworzenia filtrów importujących i eksportujących 3DS.

Projekt nie jest w żaden sposób związany z Autodeskiem. Biblioteka
jest oparta na nieoficjalnych informacjach o formacie 3DS znalezionych
w sieci.

%package devel
Summary:	lib3ds header files
Summary(pl.UTF-8):	Pliki nagłówkowe lib3ds
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
lib3ds header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe lib3ds.

%package static
Summary:	Static lib3ds library
Summary(pl.UTF-8):	Statyczna biblioteka lib3ds
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lib3ds library.

%description static -l pl.UTF-8
Statyczna biblioteka lib3ds.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
#CPPFLAGS="-I/usr/X11R6/include" - but GL/glut is used only for noinst_PROGRAMS
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/3dsdump
%attr(755,root,root) %{_libdir}/lib3ds-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib3ds-1.so.3
%{_mandir}/man1/3dsdump.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lib3ds-config
%attr(755,root,root) %{_libdir}/lib3ds.so
%{_libdir}/lib3ds.la
%{_includedir}/lib3ds
%{_aclocaldir}/lib3ds.m4
%{_mandir}/man1/lib3ds-config.1*
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib3ds.a
%endif
