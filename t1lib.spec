%define major 5
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %name

Summary:	Type 1 font rasterizer
Name:		t1lib
Version:	5.1.2
Release:	12
License:	LGPLv2+
Group:		System/Libraries
URL:		ftp://sunsite.unc.edu/pub/Linux/libs/graphics/
Source:		ftp://sunsite.unc.edu/pub/Linux/libs/graphics/%{name}-%{version}.tar.gz
Patch1:		%{name}-doc.patch
Patch2:         %{name}-config.patch
Patch4:		t1lib-5.1.2-lib-cleanup.patch
Patch5:		t1lib-5.1.2-segf.patch
Patch6:		t1lib-5.1.2-format_not_a_string_literal_and_no_format_arguments.diff
Patch7:		t1lib-5.1.2-CVE-2010-XXX.diff
BuildRequires:	libx11-devel
BuildRequires:	libxaw-devel
BuildRequires:	libxt-devel
BuildRequires:  tetex
BuildRequires:  tetex-latex
Epoch: 		1

%description
T1lib is a library for generating character and string-glyphs from
Adobe Type 1 fonts under UNIX. T1lib uses most of the code of the X11
rasterizer donated by IBM to the X11-project. But some disadvantages
of the rasterizer being included in X11 have been eliminated.  T1lib
also includes a support for antialiasing.

%package -n %{libname}
Summary: 	Type 1 font rasterizer
Group: 		System/Libraries
Obsoletes: 	%{name} < %version-%release
Provides: 	%{name} = %version-%release
Obsoletes:	%{mklibname name 1}
Provides:	%{name}1 = %version-%release
Provides:	lib%{name} = %version-%release
Requires:	%{name}-config

%description -n %{libname}
T1lib is a library for generating character and string-glyphs from
Adobe Type 1 fonts under UNIX. T1lib uses most of the code of the X11
rasterizer donated by IBM to the X11-project. But some disadvantages
of the rasterizer being included in X11 have been eliminated.  T1lib
also includes a support for antialiasing.

%package -n %{develname}
Summary: 	Header files for Type 1 font rasterizer
Group: 		Development/C
Requires: 	%{libname} >= %{epoch}:%{version}-%{release}
Obsoletes: 	%{name}-devel
Provides: 	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname -d t1lib 1}
Obsoletes:	%{mklibname -d t1lib 5}
Provides:	%{name}1-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname} 
Header files required for compiling packages needing the t1lib.

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
%patch4 -p1 -b .lib-cleanup
%patch5 -p1 -b .fix-segfault
%patch6 -p1 -b .format_not_a_string_literal_and_no_format_arguments
%patch7 -p0 -b .CVE-2010-XXX

%build
%configure2_5x
perl -pi -e 's,-DGLOBAL_CONFIG_DIR="\\"/usr/share/t1lib\\"",-DGLOBAL_CONFIG_DIR="\\"/etc/t1lib\\"",;' Makefile
make without_doc

%install
rm -rf %buildroot

%makeinstall_std
mkdir -p %buildroot/%{_sysconfdir}/t1lib
mv %buildroot/%{_datadir}/t1lib/t1lib.config %buildroot/%{_sysconfdir}/t1lib

%ifarch alpha
(cd %buildroot/%{_libdir}
ln -sf libt1.so libt1.so.0)
%endif

# cleanup
rm -rf %{buildroot}%{_libdir}/*.*a

%files -n %{libname}
%dir %{_sysconfdir}/t1lib
%doc Changes LGPL README.t1*
%attr(0755,root,root) %{_libdir}/libt1*.so.%{major}*

%files -n %{develname}
%doc doc/t1lib_doc.pdf
%{_includedir}/*
%{_libdir}/*.so

%files -n %{name}-progs
%doc README.t1python
%attr(0755,root,root) %{_bindir}/*

%files -n %{name}-config
%config(noreplace) %{_sysconfdir}/t1lib/t1lib.config
