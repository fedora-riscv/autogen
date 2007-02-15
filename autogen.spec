Summary: Sourcecode autogenerator
Name: autogen
Version: 5.8.9
Release: 1%{?dist}
License: GPL
Group: Development/Tools
Source: http://kent.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
URL: http://autogen.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: guile-devel libxml2-devel libtool
Requires: ldconfig autoconf
Requires(postun): %{_sbindir}/alternatives
Requires(preun): /sbin/install-info %{_sbindir}/alternatives
Requires(post): /sbin/install-info %{_sbindir}/alternatives

Obsoletes: libopts-devel
Obsoletes: libopts

%description
AutoGen is a tool designed to simplify the creation and maintenance of 
programes that contain large amounts of repetitious text. It is especially
valuable in programs that have several blocks of text that must be kept 
synchronised.

%package devel
Summary: Development files for autogen
Group: Development/Libraries
Requires: %{name} = %{version}-%{release} pkgconfig

%description devel
Development files for autogen.

%package manuals
Summary: man files for autogen (not devel)
Group: Documentation

%description manuals
man files for autogen (not for the devel package)

%prep
%setup -q -n %{name}-%{version}
chmod 0644 COPYING

%build
%configure
#find -name Makefile -exec sed -i -e 's/-Werror//' {} \;
make LIBTOOL=%{_bindir}/libtool
# no smp flags as it falls over during build

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
chmod 0644 %{buildroot}/%{_libdir}/pkgconfig/autoopts.pc
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
find %{buildroot} -type f -name "*.a" -exec rm -f {} ';'
rm -f %{buildroot}/%{_infodir}/dir
mv %{buildroot}/%{_bindir}/columns %{buildroot}/%{_bindir}/columns.autogen
mv %{buildroot}/%{_bindir}/getdefs %{buildroot}/%{_bindir}/getdefs.autogen
mkdir -p %{buildroot}/%{_sysconfdir}/alternatives
rm -f %{buildroot}/%{_datadir}/autogen/libopts*.tar.gz

%check
make check

%preun
if [ $1 = 0 ] ; then
/sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
%{_sbindir}/alternatives --remove columns %{_bindir}/columns.autogen
%{_sbindir}/alternatives --remove getdefs %{_bindir}/getdefs.autogen
fi

%postun 
# bits ripped from the sendmail spec file - thanks to spot!

columns=`readlink /etc/alternatives/columns`
if [ "$columns" == "%{_bindir}/columns.autogen" ]; then
   %{_sbindir}/alternatives --set columns %{_bindir}/columns.autogen
fi

getdefs=`readlink /etc/alternatives/getdefs`
if [ "$getdefs" == "%{_bindir}/getdefs.autogen" ]; then
   %{_sbindir}/alternatives --set getdefs %{_bindir}/getdefs.autogen
fi

/sbin/ldconfig

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
/sbin/ldconfig

# set up the alteratives

%{_sbindir}/alternatives --install %{_bindir}/columns columns %{_bindir}/columns.autogen 90
%{_sbindir}/alternatives --install %{_bindir}/getdefs getdefs %{_bindir}/getdefs.autogen 90

%triggerpostun -- autogen < 5.8.5
%{_sbindir}/alternatives --auto columns
%{_sbindir}/alternatives --auto getdefs

%clean
rm -rf %{buildroot}

%files
%doc AUTHORS ChangeLog COPYING NEWS NOTES README THANKS TODO VERSION
%defattr(-,root,root)
%{_bindir}/autogen
%{_bindir}/columns.autogen
%{_bindir}/getdefs.autogen
%{_infodir}/autogen.info*
%{_bindir}/xml2ag
%{_libdir}/libguileopts.so.0*
%{_libdir}/libopts.so.*
%{_datadir}/autogen/

%files manuals
%{_mandir}/man1/autogen*
%{_mandir}/man1/columns*
%{_mandir}/man1/getdefs*
%{_mandir}/man1/xml2ag*

%files devel
%defattr(-,root,root)
%{_datadir}/aclocal/autoopts.m4
%{_datadir}/aclocal/liboptschk.m4
%{_libdir}/pkgconfig/autoopts.pc
%exclude %{_mandir}/man3/*
%{_mandir}/man1/autoopts-config*
%exclude %{_includedir}/autoopts/
%{_bindir}/autoopts-config
%{_libdir}/libguileopts.so
%{_libdir}/libopts.so
%{_includedir}/autoopts

%changelog
* Thu Feb 15 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.9-1
- bump
- split man files into subpackage (conflicts on fc7)

* Sat Dec 23 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.8-1
- bump

* Wed Dec 13 2006 Paul F .Johnson <paul@all-the-johnsons.co.uk> 5.8.7-4
- fix for preun

* Thu Nov 02 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.7-3
- obsoletes libopts
- now links to it's own version of libopts shipped with the tarball

* Fri Oct 21 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.7-1
- bump to new version

* Sun Sep 10 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.5-7
- removed libopts and other autoopts conflicts

* Sun Sep 10 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.5-6
- added make check step
- fixed SOURCE0
- globbed mandirs
- removed tarball for libopts
- changed source from tar.gz to tar.bz2

* Fri Sep 08 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.5-5
- change autogen.name to name.autogen

* Sun Sep 03 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.5-4
- spec file fixes

* Sat Aug 26 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.5-3
- Added pkgconfig to the R for the devel package
- changed prefix/bin to bindir (prep)
- fixed ownership problem in the devel package

* Thu Aug 17 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.5-2
- Fixed permissions issue

* Tue Aug 15 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.5-1
- bump to official release

* Sun Jul 23 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.5-pre97-1
- bump to new version
- removed usr-sbin for _sbindir

* Wed Jul 19 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.5-pre95-1
- Added disable-autoopts
- Added R libopts
- On the suggestion of spot, added etc-alternatives-columns symlink to autogen.columns
- removed some of the man files as they belong to libopts
- removed autoopts.pc file

* Fri Jul 07 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.4-3
- Added defattr to devel
- Moved man3 from main to devel
- Moved two so files to devel
- chmod pkgconfig and COPYING file to 0644
- fixed info problems
- Added version for provides: libopts
- removed INSTALL from doc
- fixed the aclocal problem
- exclude tarball in datadir/autogen
- removed rm -rf buildroot from prep

* Thu Jul 06 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.4-2
- Added devel file
- Fixed missing files preventing mock to build
- Added infodir install
- Added libxml2-devel to BR
- Altered to mandir where required

* Thu Jul 06 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.4-1
- Big changes to the spec file
- bump to new version

* Thu Feb 23 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.3-2
- Added requires libopts
- Added pre and postun
- altered make install to be explicit rather than using make DEST install

* Thu Feb 23 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 5.8.3-1
- Initial import, bug fixes to the spec and other such things
- found that the only way to build the source is as su
