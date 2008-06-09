%define name	t1lib
%define version	5.1.2
%define release %mkrel 2
%define lib_major 5
%define lib_name %mklibname %{name} %{lib_major}

Summary:	Type 1 font rasterizer
Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		ftp://sunsite.unc.edu/pub/Linux/libs/graphics/
Source:		ftp://sunsite.unc.edu/pub/Linux/libs/graphics/%{name}-%{version}.tar.gz
Patch1:		%{name}-doc.patch
Patch2:         %{name}-config.patch
# http://qa.mandriva.com/show_bug.cgi?id=34223
Patch3:         t1lib-5.1.2-ub-CVE-2007-4033.patch
Patch4:		t1lib-5.1.2-lib-cleanup.patch
Patch5:		t1lib-5.1.2-segf.patch
Group:		System/Libraries
BuildRequires:	X11-devel xpm-devel
BuildRequires:  tetex
BuildRequires:  tetex-latex
License:	LGPLv2+
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Epoch: 		1

%description
T1lib is a library for generating character and string-glyphs from
Adobe Type 1 fonts under UNIX. T1lib uses most of the code of the X11
rasterizer donated by IBM to the X11-project. But some disadvantages
of the rasterizer being included in X11 have been eliminated.  T1lib
also includes a support for antialiasing.

%package -n %{lib_name}
Summary: 	Type 1 font rasterizer
Group: 		System/Libraries
Obsoletes: 	%{name}
Provides: 	%{name}
Obsoletes:	%{name}1
Provides:	%{name}1 = %version-%release
Provides:	lib%{name} = %version-%release
Requires:	%{name}-config

%description -n %{lib_name}
T1lib is a library for generating character and string-glyphs from
Adobe Type 1 fonts under UNIX. T1lib uses most of the code of the X11
rasterizer donated by IBM to the X11-project. But some disadvantages
of the rasterizer being included in X11 have been eliminated.  T1lib
also includes a support for antialiasing.


%package -n %{lib_name}-devel
Summary: 	Header files for Type 1 font rasterizer
Group: 		Development/C
Requires: 	%{lib_name} = %{epoch}:%{version}-%{release}
Obsoletes: 	%{name}-devel
Provides: 	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}1-devel
Provides:	%{name}1-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel 
Header files required for compiling packages needing the t1lib.

%package -n %{lib_name}-static-devel
Summary:        Static libraries for Type 1 font rasterizer
Group:          Development/C
Requires:       %{lib_name}-devel = %{epoch}:%{version}-%{release}
Provides:       %{name}-static-devel = %{version}-%{release}
Obsoletes:	%{name}1-static-devel
Provides:	%{name}1-static-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}

%description -n %{lib_name}-static-devel
Static libraries required for staticaly compiling packages needing the
t1lib.

%package -n %{name}-progs
Summary: 	Programs dor manipulating Type 1 font
Group: 		Graphics
License: 	GPL
Obsoletes:	%{name}1-progs
Provides:	%{name}1-progs

%description -n %{name}-progs
The t1lib-progs contains the programs "xglyph" and "type1afm" It also
contains the "t1libconfig" script used to configure t1lib.

%package -n %{name}-config
Summary:	Configuration for %name
Group:		Graphics

%description -n %{name}-config
The t1lib-config contains configuration files for t1lib library

%prep
%setup -q
%patch1 -p0
%patch2 -p0
%patch3 -p1 -b .CVE-2007-4033
%patch4 -p1 -b .lib-cleanup
%patch5 -p1 -b .fix-segfault

%build
%configure2_5x
perl -pi -e 's,-DGLOBAL_CONFIG_DIR="\\"/usr/share/t1lib\\"",-DGLOBAL_CONFIG_DIR="\\"/etc/t1lib\\"",;' Makefile
make without_doc
(cd doc
make clean
make pdf)

%install
rm -rf %buildroot
%makeinstall_std
mkdir -p %buildroot/%{_sysconfdir}/t1lib
mv %buildroot/%{_datadir}/t1lib/t1lib.config %buildroot/%{_sysconfdir}/t1lib

%ifarch alpha
(cd %buildroot/%{_libdir}
ln -sf libt1.so libt1.so.0)
%endif

%if %mdkversion < 200900
%post 	-n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%clean
rm -rf %buildroot

%files -n %{lib_name}
%defattr(-,root,root)
%dir %{_sysconfdir}/t1lib
%doc Changes LGPL README.t1*
%attr(755,root,root) %{_libdir}/libt1*.so.%{lib_major}*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc LGPL doc/t1lib_doc.pdf
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la

%files -n %{lib_name}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

%files -n %{name}-progs
%defattr(-,root,root)
%doc README.t1python
%attr(755,root,root) %{_bindir}/*

%files -n %{name}-config
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/t1lib/t1lib.config


