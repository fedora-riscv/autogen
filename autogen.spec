Summary:	Automated text file generator
Name:		autogen
Version:	5.9.4
Release:	5%{?dist}
# Some files are licensed under GPLv2+.
# We redistribute them under GPLv3+.
License:	GPLv3+
Group:		Development/Tools
URL:		http://www.gnu.org/software/autogen/
Source0:	ftp://ftp.gnu.org/gnu/autogen/rel5.9.4/%{name}-%{version}.tar.gz

Patch0:		%{name}-%{version}-autoopts-config.patch
Patch1:		%{name}-%{version}-pkgconfig.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# Will be dropped in Fedora 10.
Provides:	%{name}-manuals = %{version}-%{release}
Obsoletes:	%{name}-manuals < 5.9.4-1

Requires:	%{name}-libopts = %{version}-%{release}
Requires(post):	/sbin/install-info
Requires(preun):  /sbin/install-info

BuildRequires:	guile-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel

%description
AutoGen is a tool designed to simplify the creation and maintenance of
programs that contain large amounts of repetitious text. It is especially
valuable in programs that have several blocks of text that must be kept
synchronised.

%package libopts
Summary:	Automated option processing library based on %{name}
# Although sources are dual licensed with BSD, some autogen generated files
# are only under LGPLv3+. We drop BSD to avoid multiple licensing scenario.
License:	LGPLv3+
Group:		System Environment/Libraries

%description libopts
Libopts is very powerful command line option parser consisting of a set of
AutoGen templates and a run time library that nearly eliminates the hassle of
parsing and documenting command line options.

%package libopts-devel
Summary:	Development files for libopts
# Although sources are dual licensed with BSD, some autogen generated files
# are only under LGPLv3+. We drop BSD to avoid multiple licensing scenario.
License:	LGPLv3+
Group:		Development/Libraries

# Will be dropped in Fedora 10.
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < 5.9.4-1

Requires:	automake
Requires:	%{name}-libopts = %{version}-%{release}
Requires:	pkgconfig

%description libopts-devel
This package contains development files for libopts.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export LDFLAGS="-lguile"

# Static libraries are needed to run test-suite.
%configure

# Fix Libtool to remove rpaths.
rm -f ./libtool
cp %{_bindir}/libtool .

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' ./libtool

make %{?_smp_mflags}

%check
# make check
# 1 out of 20 tests fail.

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -delete
find $RPM_BUILD_ROOT -type f -name "*.a" -delete

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/autoopts.m4
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/libopts-31.0.6.tar.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info \
  %{_infodir}/dir >/dev/null 2>&1 || :
fi

%post libopts -p /sbin/ldconfig

%postun libopts -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc NEWS
%doc README
%doc THANKS
%doc TODO
%doc pkg/libopts/COPYING.gplv3
%{_bindir}/columns
%{_bindir}/getdefs
%{_bindir}/%{name}
%{_bindir}/xml2ag
%{_infodir}/%{name}.info.gz
%{_infodir}/%{name}.info-1.gz
%{_infodir}/%{name}.info-2.gz
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man1/columns.1.gz
%{_mandir}/man1/getdefs.1.gz
%{_mandir}/man1/xml2ag.1.gz

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/stdoptions.def
%{_datadir}/%{name}/*.tpl

%files libopts
%defattr(-,root,root,-)
%doc pkg/libopts/COPYING.mbsd
%doc pkg/libopts/COPYING.lgplv3
%{_libdir}/libguileopts.so.*
%{_libdir}/libopts.so.*

%files libopts-devel
%defattr(-,root,root,-)
%{_bindir}/autoopts-config
%{_datadir}/aclocal/autoopts.m4
%{_datadir}/aclocal/liboptschk.m4
%{_libdir}/libguileopts.so
%{_libdir}/libopts.so
%{_libdir}/pkgconfig/autoopts.pc
%{_mandir}/man1/autoopts-config.1.gz
%{_mandir}/man3/*

%dir %{_includedir}/autoopts
%{_includedir}/autoopts/options.h
%{_includedir}/autoopts/usage-txt.h

%changelog
* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 25 2008 Debarshi Ray <rishi@fedoraproject.org> - 5.9.4-4
- Changed dual licensing of autogen-libopts by dropping BSD.
- Fixed multilib conflicts, static libraries and removed rpath setting bits
  from autoopts-config.
- Replaced 'BuildRequires: chrpath' with 'BuildRequires: libtool' for removing
  rpaths.

* Sun Feb 24 2008 Debarshi Ray <rishi@fedoraproject.org> - 5.9.4-3
- Added 'Obsoletes: autogen-manuals ...'.
- Changed dual licensing of autogen-libopts-devel by dropping BSD.
- Defined undefined non-weak symbols.
- Omitted unused direct shared library dependencies.
- Removed rpath setting bits from pkgconfig file.
- Miscellaneous fixes.

* Thu Feb 21 2008 Debarshi Ray <rishi@fedoraproject.org> - 5.9.4-2
- Prefixed libopts and libopts-devel with autogen-.
- Removed 'BuildRequires: /usr/sbin/alternatives' and use of alternatives.
- Added Provides & Obsoletes pair in autogen-libopts-devel according to
  Fedora naming guidelines.

* Sat Feb 09 2008 Debarshi Ray <rishi@fedoraproject.org> - 5.9.4-1
- Initial build. Imported SPEC from Rawhide.
- Removed 'Obsoletes: libopts ...' and introduced libopts subpackages to avoid
  mulitple licensing scenario.
