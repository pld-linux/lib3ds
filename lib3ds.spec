#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	The 3D Studio File Format Library
Summary(pl.UTF-8):	Biblioteka obsługująca format plików 3D Studio
Name:		lib3ds
Version:	1.2.0
Release:	2
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/lib3ds/%{name}-%{version}.tar.gz
# Source0-md5:	3a7f891d18af0151876b98bc05d3b373
Patch0:		%{name}-shared.patch
Patch1:		%{name}-am18.patch
URL:		http://lib3ds.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
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
%patch0 -p1
%patch1 -p1

# extract CONFIGURE_GLUT macro
tail -n 116 aclocal.m4 | head -n 102 > acinclude.m4

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
install examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
sed -e 's/@GLUT_HEADER_DIR@/GL/' examples/glstub.h.in \
	>$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/glstub.h

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/3ds*
%attr(755,root,root) %{_libdir}/lib3ds.so.*.*
%{_mandir}/man1/3ds*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lib3ds-config
%attr(755,root,root) %{_libdir}/lib3ds.so
%{_libdir}/lib3ds.la
%{_includedir}/lib3ds
%{_aclocaldir}/*.m4
%{_mandir}/man1/lib3ds-config.1*
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib3ds.a
%endif
