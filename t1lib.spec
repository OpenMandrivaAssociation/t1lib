%define major 5
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %name
%define _disable_lto 1

Summary:	Type 1 font rasterizer
Name:		t1lib
Version:	5.1.2
Release:	26
License:	LGPLv2+
Group:		System/Libraries
URL:		ftp://sunsite.unc.edu/pub/Linux/libs/graphics/
Source0:	ftp://sunsite.unc.edu/pub/Linux/libs/graphics/%{name}-%{version}.tar.gz
Patch1:		%{name}-doc.patch
Patch2:     %{name}-config.patch
Patch4:		t1lib-5.1.2-lib-cleanup.patch
Patch5:		t1lib-5.1.2-segf.patch
Patch6:		t1lib-5.1.2-format_not_a_string_literal_and_no_format_arguments.diff
Patch7:		t1lib-5.1.2-CVE-2010-2642,CVE-2011-0433.diff
Patch8:		t1lib-5.1.2-CVE-2011-0764,1552,1553,1554.diff
Patch10:	configure.patch
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xt)
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
Provides: 	%{name} = %{version}-%{release}
Provides:	%{name}1 = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
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
Requires: 	%{libname} = %{EVRD}
Provides: 	%{name}-devel = %{version}-%{release}
Provides:	%{name}1-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname} 
Header files required for compiling packages needing the t1lib.

%package -n %{name}-progs
Summary: 	Programs dor manipulating Type 1 font
Group: 		Graphics
License: 	GPL
Provides:	 %{name}1-progs

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
%patch7 -p1 -b .CVE-2010-2642,CVE-2011-0433
%patch8 -p1 -b .CVE-2011-0764,1552,1553,1554
%patch10 -p1 -b .configure

%build
export ac_64bit_type="long"
%configure
perl -pi -e 's,-DGLOBAL_CONFIG_DIR="\\"/usr/share/t1lib\\"",-DGLOBAL_CONFIG_DIR="\\"/etc/t1lib\\"",;' Makefile
make without_doc

%install
%makeinstall_std
mkdir -p %buildroot/%{_sysconfdir}/t1lib
mv %buildroot/%{_datadir}/t1lib/t1lib.config %buildroot/%{_sysconfdir}/t1lib

# cleanup
rm -rf %{buildroot}%{_libdir}/*.*a

chmod 0755 %{buildroot}%{_libdir}/*.so.*

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


%changelog
* Thu Jan 12 2012 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.2-13
+ Revision: 760419
- sync with MDVSA-2012:004

* Sun Dec 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.2-12
+ Revision: 737637
- fix build, heh...
- drop the static lib, its sub package and the libtool *.la file
- various fixes
- funny...

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.2-11
+ Revision: 670657
- mass rebuild

* Fri Jan 21 2011 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.2-10
+ Revision: 632025
- sync with MDVSA-2011:016

  + Funda Wang <fwang@mandriva.org>
    - tighten BR

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.2-9mdv2011.0
+ Revision: 607959
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.2-8mdv2010.1
+ Revision: 519073
- rebuild

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1:5.1.2-7mdv2010.0
+ Revision: 427223
- rebuild

* Sat Mar 28 2009 Funda Wang <fwang@mandriva.org> 1:5.1.2-6mdv2009.1
+ Revision: 361913
- rebuild

* Mon Dec 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.2-5mdv2009.1
+ Revision: 317652
- fix build with -Werror=format-security (P6)

* Tue Aug 26 2008 Funda Wang <fwang@mandriva.org> 1:5.1.2-4mdv2009.0
+ Revision: 276382
- new devel package policy
- obsoletes wrong old libname to ease upgrade

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1:5.1.2-3mdv2009.0
+ Revision: 225605
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Jan 31 2008 Anssi Hannula <anssi@mandriva.org> 1:5.1.2-2mdv2008.1
+ Revision: 160930
- fix major
- ensure major correctness

* Thu Jan 31 2008 Frederik Himpe <fhimpe@mandriva.org> 1:5.1.2-1mdv2008.1
+ Revision: 160919
- New upstream version
- Rediff CVE-2007-4033 patch
- Add Patch4 from Fedora/Debian: don't link with unneeded libraries
- Add Patch5 from Fedora: fix a segfault
- Remove copies of standard licenses

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Thu Sep 27 2007 Andreas Hasenack <andreas@mandriva.com> 1:5.1.1-2mdv2008.0
+ Revision: 93379
- security patch for CVE-2007-4033 (#34223)


* Sun Feb 18 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 5.1.1-1mdv2007.0
+ Revision: 122249
- Release 5.1.1.
- Removed Patch0 (merged upstream).
- Import t1lib

* Tue Sep 05 2006 Giuseppe Ghibò <ghibo@mandriva.com> 5.1.0-3mdv2007.0
- Rebuilt.

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 5.1.0-2mdk
- Rebuild

* Thu Aug 04 2005 Giuseppe Ghibò <ghibo@mandriva.com> 5.1.0-1mdk
- Release 5.1.0.
- Rebuilt Patch0.

* Mon Apr 18 2005 Olivier Thauvin <nanardon@mandrake.org> 5.0.2-5mdk
- rebuild && reupload
- %%mkrel

* Tue Jan 11 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.0.2-4mdk
- %%major is 5
- split config into %%name-config

* Tue Jan 11 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.0.2-3mdk
- Fix name/obsoletes/provides cause %%mklibname

* Sun Jan 09 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.0.2-2mdk
- reupload

* Tue Jan 04 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.0.2-1mdk
- 5.0.2

* Sat Aug 28 2004 Giuseppe Ghibr <ghibo@mandrakesoft.com> 1.3.1-15mdk
- Rebuilt.

* Tue Mar 02 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.3.1-14mdk
- Fix another DEP with epoch

* Mon Mar 01 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.3.1-13mdk
- Added 1 to Requires.

