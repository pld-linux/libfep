#
# Conditional build:
%bcond_without	apidocs		# gtk-doc based API documentation
%bcond_without	static_libs	# static libraries

Summary:	Library to implement FEP (front end processor) on ANSI terminals
Summary(pl.UTF-8):	Biblioteka do implementacji FEP (procesorów frontendowych) na terminalach ANSI
Name:		libfep
Version:	0.1.0
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://github.com/ueno/libfep/releases
Source0:	https://github.com/ueno/libfep/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	261c6d47a18acc8aecf55cda2a5275bc
Patch0:		%{name}-docs.patch
URL:		https://github.com/ueno/libfep/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gobject-introspection-devel >= 0.9.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libtool >= 2:2
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
# not needed for releases
#BuildRequires:	vala
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libfep is a library to implement FEP (front end processor) on ANSI
terminals. Features:
- render text at the bottom of the terminal,
- render text at the cursor position,
- send text to the child process,
- monitor key strokes typed on the terminal.

%description -l pl.UTF-8
libfep to biblioteka do implementacji FEP (procesorów frontendowych)
na terminalach ANSI. Możliwości:
- renderowanie tekstu na dole terminala,
- renderowanie tekstu na pozycji kursora,
- wysyłanie tekstu do procesu potomnego,
- monitorowanie naciśnięć klawiszy na terminalu.

%package devel
Summary:	Header files for libfep library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libfep
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.0

%description devel
Header files for libfep library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libfep.

%package static
Summary:	Static libfep library
Summary(pl.UTF-8):	Statyczna biblioteka libfep
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libfep library.

%description static -l pl.UTF-8
Statyczna biblioteka libfep.

%package -n vala-libfep
Summary:	Vala API for libfep library
Summary(pl.UTF-8):	API języka Vala do biblioteki libfep
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-libfep
Vala API for libfep library.

%description -n vala-libfep -l pl.UTF-8
API języka Vala do biblioteki libfep.

%package apidocs
Summary:	libfep API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libfep
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for libfep library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libfep.

%prep
%setup -q
%patch -P0 -p1

# force rebuild
%{__rm} docs/libfep/*.txt docs/libfep-glib/*.txt

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-gtk-doc} \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfep*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/fep
%attr(755,root,root) %{_bindir}/fepcli
%attr(755,root,root) %{_libdir}/libfep.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfep.so.0
%attr(755,root,root) %{_libdir}/libfep-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfep-glib.so.0
%{_libdir}/girepository-1.0/Fep-1.0.typelib
%{_mandir}/man1/fep.1*
%{_mandir}/man1/fepcli.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfep.so
%attr(755,root,root) %{_libdir}/libfep-glib.so
%{_datadir}/gir-1.0/Fep-1.0.gir
%{_includedir}/fep-1.0
%{_pkgconfigdir}/libfep.pc
%{_pkgconfigdir}/libfep-glib.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfep.a
%{_libdir}/libfep-glib.a
%endif

%files -n vala-libfep
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libfep-glib.deps
%{_datadir}/vala/vapi/libfep-glib.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libfep
%{_gtkdocdir}/libfep-glib
%endif
