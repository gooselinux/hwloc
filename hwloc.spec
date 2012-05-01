Summary:   Portable Hardware Locality - portable abstraction of hierarchical architectures
Name:      hwloc
Version:   1.1
Release:   0.1%{?dist}
License:   BSD
Group:     Applications/System
URL:       http://www.open-mpi.org/projects/hwloc/
Source0:   http://www.open-mpi.org/software/hwloc/v1.1/downloads/%{name}-%{version}.tar.bz2
Patch0:    2967_lstopo.patch
# Patch to the 1.1 fix 2967 http://www.open-mpi.org/software/hwloc/nightly/v1.1/hwloc-1.1rc6r2967.tar.bz2
# Fix hwloc_bitmap_to_ulong right after allocating the bitmap.
# Fix the minimum width of NUMA nodes, caches and the legend in the graphical lstopo output.
# Cleanup error management in hwloc-gather-topology.sh.
# Add a manpage and usage for hwloc-gather-topology.sh on Linux.
#
# Rename hwloc-gather-topology.sh to hwloc-gather-topology to be consistent with the upcoming version 1.2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libX11-devel libxml2-devel cairo-devel
%ifnarch s390 s390x
BuildRequires: numactl-devel
%endif

%description
The Portable Hardware Locality (hwloc) software package provides 
a portable abstraction (across OS, versions, architectures, ...) 
of the hierarchical topology of modern architectures, including 
NUMA memory nodes,  shared caches, processor sockets, processor cores
and processing units (logical processors or "threads"). It also gathers
various system attributes such as cache and memory information. It primarily
aims at helping applications with gathering information about modern
computing hardware so as to exploit it accordingly and efficiently.

hwloc may display the topology in multiple convenient formats. 
It also offers a powerful programming interface (C API) to gather information 
about the hardware, bind processes, and much more.

%package devel
Summary:   Headers and shared development libraries for hwloc
Group:     Development/Libraries
Requires:  %{name} = %{version}-%{release}

%description devel
Headers and shared object symbolic links for the hwloc.

%prep
%setup -q
# Apply patches:
#
%patch0 -p1


%build
# There are two options how to get rid of RPATH
# 1) http://lists.fedoraproject.org/pipermail/packaging/2010-June/007187.html
# Issues with 2nd approach are
# Can I do it on all architectures?
# rpmlint complains about "/usr/lib" in sed command line
# To be run BEFORE %%configure
%ifarch ppc64 s390x x86_64 ia64 alpha sparc64
%{__sed} -i.libdir_syssearch -e '/sys_lib_dlsearch_path_spec/s|/usr/lib |/usr/lib /usr/lib64 /lib /lib64|' configure
%endif

%configure

# 2) http://fedoraproject.org/wiki/RPath_Packaging_Draft
# %%{__sed} -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
# %%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# To be run AFTER %%configure


%{__make} %{?_smp_mflags} V=1

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

# We don't ship .la files.
%{__rm} -rf %{buildroot}%{_libdir}/libhwloc.la

# Rename hwloc-gather-topology.sh to hwloc-gather-topology
%{__mv} %{buildroot}%{_bindir}/hwloc-gather-topology.sh %{buildroot}%{_bindir}/hwloc-gather-topology
%{__mv} %{buildroot}%{_mandir}/man1/hwloc-gather-topology.sh.1 %{buildroot}%{_mandir}/man1/hwloc-gather-topology.1
%{__sed} -i -e's/hwloc-gather-topology.sh/hwloc-gather-topology/ig' %{buildroot}%{_mandir}/man1/hwloc-gather-topology.1

%{__mv} %{buildroot}%{_defaultdocdir}/%{name} %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%{__cp} -p AUTHORS COPYING NEWS README VERSION %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%{__cp} -p doc/hwloc-hello.c %{buildroot}%{_defaultdocdir}/%{name}-%{version}

%check
%{__make} check

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%{_bindir}/%{name}*
%{_bindir}/lstopo
%{_mandir}/man7/%{name}*
%{_mandir}/man1/%{name}*
%{_mandir}/man1/lstopo*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}.dtd
%dir %{_defaultdocdir}/%{name}-%{version}
%{_defaultdocdir}/%{name}-%{version}/*[^c]
%{_libdir}/libhwloc*.so.*

%files devel
%defattr(-, root, root, -)
%{_libdir}/pkgconfig/*
%{_libdir}/libhwloc*.so
%{_mandir}/man3/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_includedir}/%{name}.h
%{_defaultdocdir}/%{name}-%{version}/*c


%changelog
* Mon Jan  3 2011 Dan Horák <dan[at]danny.cz> - 1.1-0.1
- fix build on s390(x) where numactl is missing

* Sat Jan  1 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.1-0
- 1.1 rel# Patch to the 1.1 fix 2967 http://www.open-mpi.org/software/hwloc/nightly/v1.1/hwloc-1.1rc6r2967.tar.bz2
- Fix hwloc_bitmap_to_ulong right after allocating the bitmap.
- Fix the minimum width of NUMA nodes, caches and the legend in the graphical lstopo output.
- Cleanup error management in hwloc-gather-topology.sh.
- Add a manpage and usage for hwloc-gather-topology.sh on Linux.
- Rename hwloc-gather-topology.sh to hwloc-gather-topology to be consistent with the upcoming version 1.2ease

* Mon Jul 19 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.2-1
- 1.0.2 release
- added "check" section to the RPM SPEC file

* Mon Jul 19 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.2-0.1.rc1r2330
- 1.0.2 release candidate

* Mon Jul 12 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-19
- Fixed issues as described at https://bugzilla.redhat.com/show_bug.cgi?id=606498#c6

* Fri Jul 09 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-18
- Fixed issues as described at https://bugzilla.redhat.com/show_bug.cgi?id=606498

* Fri Jun 18 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-17
- Initial build
