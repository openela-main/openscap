Name:                 openscap
Version:              1.3.8
Release:              1%{?dist}.openela.1.0
Summary:              Set of open source libraries enabling integration of the SCAP line of standards
Group:                System Environment/Libraries
License:              LGPLv2+
URL:                  http://www.open-scap.org/
Source0:              https://github.com/OpenSCAP/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:               openscap-1.3.9-PR-1996-fix-sysctl-offline.patch
BuildRequires:        cmake >= 2.6
BuildRequires:        swig libxml2-devel libxslt-devel perl-generators perl-XML-Parser
BuildRequires:        rpm-devel
BuildRequires:        libgcrypt-devel
BuildRequires:        pcre-devel
BuildRequires:        libacl-devel
BuildRequires:        libselinux-devel
BuildRequires:        libcap-devel
BuildRequires:        libblkid-devel
BuildRequires:        bzip2-devel
BuildRequires:        asciidoc
BuildRequires:        openldap-devel
BuildRequires:        GConf2-devel
BuildRequires:        glib2-devel
BuildRequires:        dbus-devel
BuildRequires:        libyaml-devel
BuildRequires:        xmlsec1-devel xmlsec1-openssl-devel
Patch1:               0001-Add-OpenELA-8-and-9-support.patch
%if %{?_with_check:1}%{!?_with_check:0}
BuildRequires:        perl-XML-XPath
BuildRequires:        bzip2
%endif
Requires:             bash
Requires:             bzip2-libs
Requires:             dbus
Requires:             libyaml
Requires:             GConf2
Requires:             glib2
Requires:             libacl
Requires:             libblkid
Requires:             libcap
Requires:             libselinux
Requires:             openldap
Requires:             popt
# RHEL8 has procps-ng, which provides procps
Requires:             procps
Requires:             xmlsec1 xmlsec1-openssl
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Obsoletes:            python2-openscap
Obsoletes:            openscap-content-sectool
Obsoletes:            openscap-extra-probes
Obsoletes:            openscap-extra-probes-sql

%description
OpenSCAP is a set of open source libraries providing an easier path
for integration of the SCAP line of standards. SCAP is a line of standards
managed by NIST with the goal of providing a standard language
for the expression of Computer Network Defense related information.

%package        devel
Summary:              Development files for %{name}
Group:                Development/Libraries
Requires:             %{name}%{?_isa} = %{version}-%{release}
Requires:             libxml2-devel
Requires:             pkgconfig
BuildRequires:        doxygen

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        python3
Summary:              Python 3 bindings for %{name}
Group:                Development/Libraries
Requires:             %{name}%{?_isa} = %{version}-%{release}
BuildRequires:        python3-devel

%description    python3
The %{name}-python3 package contains the bindings so that %{name}
libraries can be used by python3.

%package        scanner
Summary:              OpenSCAP Scanner Tool (oscap)
Group:                Applications/System
Requires:             %{name}%{?_isa} = %{version}-%{release}
Requires:             libcurl >= 7.12.0
BuildRequires:        libcurl-devel >= 7.12.0
Obsoletes:            openscap-selinux
Obsoletes:            openscap-selinux-compat

%description    scanner
The %{name}-scanner package contains oscap command-line tool. The oscap
is configuration and vulnerability scanner, capable of performing
compliance checking using SCAP content.

%package        utils
Summary:              OpenSCAP Utilities
Group:                Applications/System
Requires:             %{name}%{?_isa} = %{version}-%{release}
Requires:             rpmdevtools rpm-build
Requires:             %{name}-scanner%{?_isa} = %{version}-%{release}
Requires:             bash

%description    utils
The %{name}-utils package contains command-line tools build on top
of OpenSCAP library. Historically, openscap-utils included oscap
tool which is now separated to %{name}-scanner sub-package.

%package        engine-sce
Summary:              Script Check Engine plug-in for OpenSCAP
Group:                Applications/System
Requires:             %{name}%{?_isa} = %{version}-%{release}

%description    engine-sce
The Script Check Engine is non-standard extension to SCAP protocol. This
engine allows content authors to avoid OVAL language and write their assessment
commands using a scripting language (Bash, Perl, Python, Ruby, ...).

%package        engine-sce-devel
Summary:              Development files for %{name}-engine-sce
Group:                Development/Libraries
Requires:             %{name}-devel%{?_isa} = %{version}-%{release}
Requires:             %{name}-engine-sce%{?_isa} = %{version}-%{release}
Requires:             pkgconfig

%description    engine-sce-devel
The %{name}-engine-sce-devel package contains libraries and header files
for developing applications that use %{name}-engine-sce.

%prep
%autosetup -p1
mkdir build

%build
cd build
%cmake -DENABLE_PERL=OFF \
        -DENABLE_DOCS=ON \
        -DENABLE_OSCAP_UTIL_DOCKER=OFF \
        -DENABLE_OSCAP_UTIL_CHROOT=ON \
        -DENABLE_OSCAP_UTIL_PODMAN=ON \
        -DENABLE_OSCAP_UTIL_VM=ON \
        -DENABLE_OSCAP_REMEDIATE_SERVICE=OFF \
        ..
make %{?_smp_mflags}
make docs

%check
%if %{?_with_check:1}%{!?_with_check:0}
ctest -V %{?_smp_mflags}
%endif

%install
cd build
%make_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# fix python shebangs
pathfix.py -i %{__python3} -p -n $RPM_BUILD_ROOT%{_bindir}/scap-as-rpm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS NEWS README.md
%license COPYING
%doc %{_pkgdocdir}/manual/
%dir %{_datadir}/openscap
%dir %{_datadir}/openscap/schemas
%dir %{_datadir}/openscap/xsl
%dir %{_datadir}/openscap/cpe
%{_libdir}/libopenscap.so.*
%{_datadir}/openscap/schemas/*
%{_datadir}/openscap/xsl/*
%{_datadir}/openscap/cpe/*

%files python3
%{python3_sitearch}/*

%files devel
%doc %{_pkgdocdir}/html/
%{_libdir}/libopenscap.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/openscap
%exclude %{_includedir}/openscap/sce_engine_api.h

%files engine-sce-devel
%{_libdir}/libopenscap_sce.so
%{_includedir}/openscap/sce_engine_api.h

%files scanner
%{_mandir}/man8/oscap.8.gz
%{_bindir}/oscap
%{_mandir}/man8/oscap-chroot.8.gz
%{_bindir}/oscap-chroot
%{_sysconfdir}/bash_completion.d

%files utils
%doc docs/oscap-scan.cron
%{_mandir}/man8/oscap-ssh.8.gz
%{_bindir}/oscap-ssh
%{_mandir}/man8/oscap-podman.8.gz
%{_bindir}/oscap-podman
%{_mandir}/man8/oscap-vm.8.gz
%{_bindir}/oscap-vm
%{_mandir}/man8/scap-as-rpm.8.gz
%{_bindir}/scap-as-rpm
%{_mandir}/man8/autotailor.8.gz
%{_bindir}/autotailor

%files engine-sce
%{_libdir}/libopenscap_sce.so.*
%{_bindir}/oscap-run-sce-script

%changelog
* Fri Feb 09 2024 Release Engineering <releng@openela.org> - 1.3.8.openela.1.0
- Add OpenELA to openscap

* Fri Jul 14 2023 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.8-1
- Upgrade to the latest upstream release (rhbz#2222864)
- Fix systemd* probes unit enumeration (rhbz#2223547)

* Fri Jan 27 2023 Jan Černý <jcerny@redhat.com> - 1.3.7-1
- Upgrade to the latest upstream release (rhbz#2159290)
- Fix error when processing OVAL filters (rhbz#2126882)
- Don't emit xmlfilecontent items if XPath doesn't match (rhbz#2139060)

* Thu Jul 21 2022 Jan Černý <jcerny@redhat.com> - 1.3.6-4
- Fix potential invalid scan results in OpenSCAP (rhbz#2111040)
- Remove oscap-remediate service (rhbz#2111360)

* Wed Feb 02 2022 Jan Černý <jcerny@redhat.com> - 1.3.6-3
- Prevent fails of test_ds_misc.sh

* Mon Jan 31 2022 Jan Černý <jcerny@redhat.com> - 1.3.6-2
- Fix coverity issues
- Prevent fails of test_ds_misc.sh

* Thu Jan 20 2022 Jan Černý <jcerny@redhat.com> - 1.3.6-1
- Upgrade to the latest upstream release (rhbz#2041781)
- Select and exclude groups of rules on the command line
- The boot-time remediation service for systemd's Offline Update mode

* Fri Nov 19 2021 Jan Černý <jcerny@redhat.com> - 1.3.5-10
- Print warning for local files

* Wed Nov 10 2021 Jan Černý <jcerny@redhat.com> - 1.3.5-9
- Lower memory limits and improve their checking (rhbz#2021851)
- Remove timestamp from the user manual (rhbz#2022364)

* Tue Nov 09 2021 Jan Černý <jcerny@redhat.com> - 1.3.5-8
- Allow local DS components (rhbz#1970529)
- Fix hostname detection in offline scan of UBI 9 images (rhbz#1893888)
- Add an alternative source of hostname (rhbz#1977668)
- Fix oscap-chroot errors in process58_probe caused by empty /proc (rhbz#2008922)

* Thu Nov 04 2021 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.5-7
- Introduce support for Image Builder's Blueprint remediation type (rhbz#2020050)

* Wed Jul 28 2021 Jan Černý <jcerny@redhat.com> - 1.3.5-6
- Initialize crypto API only once (rhbz#1959570)

* Wed Jul 14 2021 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.5-5
- Add 'null' values handling to the yamlfilecontent probe (RHBZ#1981691)

* Tue Jun 01 2021 Jan Černý <jcerny@redhat.com> - 1.3.5-4
- Replace getlogin by cuserid

* Mon May 10 2021 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.5-3
- Waive known issue with hugepages in upstream testsuite (RHBZ#1912000)
- Fix issues reported by the coverity scan
- Introduce OSBuild 'blueprint' fix type

* Tue May 04 2021 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.5-2
- Fix changelog (add missing 1.3.3-6 entry)

* Thu Apr 29 2021 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.5-1
- Upgrade to the latest upstream release (RHBZ#1953092)
- Fix segfault when using --stig-viewer option and latest XML file from DoD (RHBZ#1912000)
- Improve doc about --stig-viewer (RHBZ#1918759)
- Backport an upstream patch adding CentOS CPE (RHBZ#1907935)

* Wed Nov 25 2020 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.4-5
- Add check for non-local GPFS file system into Test Suite (RHBZ#1840578)

* Fri Nov 13 2020 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.4-4
- Use MALLOC_CHECK_=3 while executing Test Suite (RHBZ#1891770)

* Tue Nov 10 2020 Jan Černý <jcerny@redhat.com> - 1.3.4-3
- Fix memory allocation (RHBZ#1891770)

* Thu Oct 29 2020 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.3-6
- Enable profile composition with a specific platform (RHBZ#1896676)
- Enable YAML probe to work with sets of values (RHBZ#1895715)

* Mon Oct 26 2020 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.4-2
- Fix problems uncovered by the Coverity Scan (RHBZ#1887794)

* Wed Oct 14 2020 Evgenii Kolesnikov <ekolesni@redhat.com> - 1.3.4-1
- Upgrade to the latest upstream release (RHBZ#1887794)
- Treat GPFS as a remote file system (RHBZ#1840578, RHBZ#1840579)
- Fixed the most problematic memory issues that were causing OOM situations
  for systems with large amount of files (RHBZ#1824152)
- Proper handling of OVALs with circular dependencies between definitions (RHBZ#1812476)

* Wed Aug 19 2020 Jan Černý <jcerny@redhat.com> - 1.3.3-5
- Detect remote file systems correctly (RHBZ#1870087)

* Mon Aug 03 2020 Jan Černý <jcerny@redhat.com> - 1.3.3-4
- Fix memory leaks in rpmverifyfile probe (RHBZ#1861301)

* Tue Jul 21 2020 Matěj Týč <matyc@redhat.com> - 1.3.3-3
- Added support for fetching remote content with compression (RHBZ#1855708)

* Thu Jun 25 2020 Matěj Týč <matyc@redhat.com> - 1.3.3-2
- Prevent unwanted recursion that could crash the scanner (RHBZ#1686370)

* Mon May 04 2020 Evgeny Kolesnikov <ekolesni@redhat.com> - 1.3.3-1
- Upgrade to the latest upstream release (rhbz#1829761)
- Added a Python script that can be used for CLI tailoring (autotailor)
- Added timezone to XCCDF TestResult start/end time
- Added yamlfilecontent independent probe (proposal/draft implementation)
- Added ability to generate `machineconfig` fix
- Introduced `urn:xccdf:fix:script:kubernetes` fix type in XCCDF
- Fixed filepath pattern matching in offline mode in textfilecontent58 probe
- Fixed #170: The rpmverifyfile probe can't verify files from '/bin' directory
- Fixed #1512: Severity refinement lost in generated guide
- Fixed #1453: Pointer lost in Swig API
- The data system_info probe return for offline and online modes is consistent and actual
- Evaluation Characteristics of the XCCDF report are now consistent with OVAL entities
  from system_info probe

* Fri Mar 27 2020 Jan Černý <jcerny@redhat.com> - 1.3.2-9
- Generate HTML guides from tailored profiles (RHBZ#1743835)

* Wed Mar 18 2020 Jan Černý <jcerny@redhat.com> - 1.3.2-8
- Fix tests for rpmverifyfileprobe (RHBZ#1814726)

* Thu Mar 12 2020 Jan Černý <jcerny@redhat.com> - 1.3.2-7
- Fix segmentation fault in systemdunitdependency_probe (RHBZ#1793050)
- Fix crash in textfilecontent probe (RHBZ#1686467)
- Do not drop empty lines from Ansible remediations (RHBZ#1795563)
- Fix oscap-ssh --sudo (RHBZ#1803116)
- Remove useless warnings (RHBZ#1764139)

* Thu Jan 23 2020 Jan Černý <jcerny@redhat.com> - 1.3.2-6
- Fix FindACL.cmake

* Tue Jan 21 2020 Matěj Týč <matyc@redhat.com> - 1.3.2-5
- Added more exhaustive package dependencies.
- Added the covscan/UX patch.

* Mon Jan 20 2020 Evgeny Kolesnikov <ekolesni@redhat.com> - 1.3.2-4
- Added patch: utils/oscap-podman: Detect ambiguous scan target

* Mon Jan 20 2020 Evgeny Kolesnikov <ekolesni@redhat.com> - 1.3.2-3
- Refined requirements

* Sun Jan 19 2020 Evgeny Kolesnikov <ekolesni@redhat.com> - 1.3.2-2
- Added patch: Fix case where CMake couldn't find libacl or xattr.h

* Wed Jan 15 2020 Evgeny Kolesnikov <ekolesni@redhat.com> - 1.3.2-1
- Upgrade to the latest upstream release (rhbz#1778296)
- Offline mode support for environmentvariable58 probe (rhbz#1493614)
- The oscap-docker wrapper is available without Atomic
- Improved support of multi-check rules (report, remediations, console output) (rhbz#1771438)
- Improved HTML report look and feel, including printed version (rhbz#1640839)
- Less clutter in verbose mode output; some warnings and errors demoted to verbose mode levels
- Probe rpmverifyfile uses and returns canonical paths (rhbz#1776308)
- Improved a11y of HTML reports and guides (rhbz#1767382)
- Fixes and improvements for SWIG Python bindings (rhbz#1753603)
- #1403 fixed: Scanner would not apply remediation for multicheck rules (verbosity)
- Fixed URL link mechanism for Red Hat Errata
- New STIG Viewer URI: public.cyber.mil
- Probe selinuxsecuritycontext would not check if SELinux is enabled
- Scanner would provide information about unsupported OVAL objects
- Added more tests for offline mode (probes, remediation) (rhbz#1618489)
- #528 fixed: Eval SCE script when /tmp is in mode noexec
- #1173, RHBZ#1603347 fixed: Double chdir/chroot in probe rpmverifypackage (rhbz#1636431) 

* Wed Dec 18 2019 Vojtech Polasek <vpolasek@redhat.com> - 1.3.1-3
- put back openscap-chroot, openscap-podman and openscap-vm files

* Fri Nov 01 2019 Vojtech Polasek <vpolasek@redhat.com> - 1.3.1-2
- Fixed XSLT template making rule details in reports accessible for screenreader users (#1767382)

* Fri Jun 14 2019 Evgeny Kolesnikov <ekolesni@redhat.com> - 1.3.1-1
- Bumped the package release number

* Thu Jun 13 2019 Evgeny Kolesnikov <ekolesni@redhat.com> - 1.3.1-0
- Upgrade to the latest upstream release (rhbz#1718826)
- Support for SCAP 1.3 Source Datastreams (evaluating, XML schemas, validation) (rhbz#1709429)
- Tailoring files are included in ARF result files
- Remote filesystems mounted using `autofs` direct maps are not recognized as local filesystems (rhbz#1655943)
- Offline scan utilizing rpmverifyfile probe fails in fchdir and aborts (rhbz#1636431)

* Wed Jan 16 2019 Gabriel Becker <ggasparb@redhat.com> - 1.3.0-7
- Removed oscap-vm binary and manpage files from build as they will not be supported by RHEL-8.0.0.
- Explicitly specify which files should be in openscap-utils subpackage.

* Mon Jan 14 2019 Gabriel Becker <ggasparb@redhat.com> - 1.3.0-6
- Removed containers package as RHEL-8.0.0 will not support it.
- Removed oscap-chroot binary and manpage from utils package as RHEL-8.0.0 will not support it.

* Mon Oct 15 2018 Jan Černý <jcerny@redhat.com> - 1.3.0-5
- Fixed unresolved symbols in SCE library

* Fri Oct 12 2018 Matěj Týč <matyc@redhat.com> - 1.3.0-4
- Fixed a sudo regression in oscap-ssh.
- Updated test to work with newer versions of procps.
- Updated the man page.

* Tue Oct 09 2018 Matěj Týč <matyc@redhat.com> - 1.3.0-3
- Fixed memory error in SWIG (RHBZ#1607014)

* Tue Oct 09 2018 Jan Černý <jcerny@redhat.com> - 1.3.0-2
- Drop openscap-perl subpackage (RHBZ#1624396)

* Mon Oct 08 2018 Jan Černý <jcerny@redhat.com> - 1.3.0-1
- upgrade to the latest upstream release
- list subpackages removed in 1.3.0_alpha1-1 as obsoleted

* Fri Aug 10 2018 Jan Černý <jcerny@redhat.com> - 1.3.0_alpha2-1
- upgrade to the latest upstream release

* Thu Aug 09 2018 Jan Černý <jcerny@redhat.com> - 1.3.0_alpha1-3
- Add RHEL8 CPE (until RHEL8 public beta downstream patch only)

* Fri Jul 27 2018 Jan Černý <jcerny@redhat.com> - 1.3.0_alpha1-2
- Use AsciiDoc instead of AsciiDoctor (RHBZ#1607541)

* Fri Jul 20 2018 Jan Černý <jcerny@redhat.com> - 1.3.0_alpha1-1
- upgrade to the latest upstream release
- change specfile to use CMake
- dropped commands in the spec file that are no longer relevant
- dropped subpackages in the spec file that are no longer relevant

* Fri May 18 2018 Jan Černý <jcerny@redhat.com> - 1.2.16-5
- Use pathfix.py instead of a downstream patch to fix shebang

* Thu May 17 2018 Jan Černý <jcerny@redhat.com> - 1.2.16-4
- Remove Python 2 dependencies

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.16-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Nov 14 2017 jcerny@redhat.com - 1.2.16-1
- upgrade to the latest upstream release

* Thu Oct 05 2017 Martin Preisler <mpreisle@redhat.com> - 1.2.15-2
- moved oscap-chroot to openscap-scanner because it's a thin wrapper script with no dependencies

* Fri Aug 25 2017 Jan Černý <jcerny@redhat.com> - 1.2.15-1
- upgrade to the latest upstream release

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.14-9
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.14-8
- Python 2 binary package renamed to python2-openscap
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.2.14-7
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.2.14-6
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.2.14-5
- Rebuilt for RPM soname bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.14-2
- Perl 5.26 rebuild

* Tue Mar 21 2017 Martin Preisler <mpreisle@redhat.com> - 1.2.14-1
- upgrade to the latest upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 05 2017 Martin Preisler <mpreisle@redhat.com> - 1.2.13-1
- upgrade to the latest upstream release

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.12-2
- Rebuild for Python 3.6

* Tue Nov 22 2016 Martin Preisler <mpreisle@redhat.com> - 1.2.12-1
- upgrade to the latest upstream release

* Wed Oct 19 2016 Martin Preisler <mpreisle@redhat.com> - 1.2.11-1
- upgrade to the latest upstream release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 12 2016 Martin Preisler <mpreisle@redhat.com> - 1.2.10-1
- upgrade to the latest upstream release

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.9-2
- Perl 5.24 rebuild

* Fri Apr 22 2016 Martin Preisler <mpreisle@redhat.com> - 1.2.9-1
- upgrade to the latest upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Šimon Lukašík <slukasik@redhat.com> - 1.2.8-1
- upgrade to the latest upstream release

* Thu Dec 03 2015 Šimon Lukašík <slukasik@redhat.com> - 1.2.7-1
- upgrade to the latest upstream release

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Oct 13 2015 Zbyněk Moravec <zmoravec@redhat.com> - 1.2.6-3
- fix oscap-docker shebang

* Wed Oct 07 2015 Šimon Lukašík <slukasik@redhat.com> - 1.2.6-2
- put oscap-docker to openscap-containers subpackage
- do not require atomic at all

* Mon Oct 05 2015 Zbyněk Moravec <zmoravec@redhat.com> - 1.2.6-1
- upgrade to the latest upstream release

* Wed Jul 29 2015 Martin Preisler <mpreisle@redhat.com> - 1.2.5-2
- rebuilt because of librpm and librpmio ABI break

* Mon Jul 06 2015 Šimon Lukašík <slukasik@redhat.com> - 1.2.5-1
- upgrade to the latest upstream release

* Sat Jun 20 2015 Šimon Lukašík <slukasik@redhat.com> - 1.2.4-1
- upgrade to the latest upstream release.
- Content of selinux package has been purged.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.3-2
- Perl 5.22 rebuild

* Fri May 01 2015 Šimon Lukašík <slukasik@redhat.com> - 1.2.3-1
- upgrade to the latest upstream release

* Thu Apr 02 2015 Šimon Lukašík <slukasik@redhat.com> - 1.2.2-1
- upgrade to the latest upstream release

* Sat Jan 10 2015 Šimon Lukašík <slukasik@redhat.com> - 1.2.1-1
- upgrade to the latest upstream release

* Tue Dec 02 2014 Šimon Lukašík <slukasik@redhat.com> - 1.2.0-1
- upgrade to the latest upstream release

* Fri Sep 26 2014 Šimon Lukašík <slukasik@redhat.com> - 1.1.1-1
- upgrade to the latest upstream release

* Fri Sep 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.0-2
- Perl 5.20 rebuild

* Wed Sep 03 2014 Šimon Lukašík <slukasik@redhat.com> - 1.1.0-1
- upgrade

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.9-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 01 2014 Šimon Lukašík <slukasik@redhat.com> - 1.0.9-2
- Extract oscap tool to a separate package (rhbz#1115116)

* Wed Jun 25 2014 Martin Preisler <mpreisle@redhat.com> - 1.0.9-1
- upgrade

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Šimon Lukašík <slukasik@redhat.com> - 1.0.8-1
- upgrade

* Thu Mar 20 2014 Šimon Lukašík <slukasik@redhat.com> - 1.0.7-1
- upgrade

* Wed Mar 19 2014 Šimon Lukašík <slukasik@redhat.com> - 1.0.6-1
- upgrade

* Fri Mar 14 2014 Šimon Lukašík <slukasik@redhat.com> - 1.0.5-1
- upgrade

* Thu Feb 13 2014 Šimon Lukašík <slukasik@redhat.com> - 1.0.4-1
- upgrade

* Tue Jan 14 2014 Šimon Lukašík <slukasik@redhat.com> - 1.0.3-1
- upgrade
- This upstream release addresses: #1052142

* Fri Jan 10 2014 Šimon Lukašík <slukasik@redhat.com> - 1.0.2-1
- upgrade
- This upstream release addresses: #1018291, #1029879, #1026833

* Thu Nov 28 2013 Šimon Lukašík <slukasik@redhat.com> - 1.0.1-1
- upgrade

* Tue Nov 26 2013 Šimon Lukašík <slukasik@redhat.com> - 1.0.0-3
- expand LT_CURRENT_MINUS_AGE correctly

* Thu Nov 21 2013 Šimon Lukašík <slukasik@redhat.com> - 1.0.0-2
- dlopen libopenscap_sce.so.{current-age} explicitly
  That allows for SCE to work without openscap-engine-sce-devel

* Tue Nov 19 2013 Šimon Lukašík <slukasik@redhat.com> - 1.0.0-1
- upgrade
- package openscap-engine-sce-devel separately

* Fri Nov 15 2013 Šimon Lukašík <slukasik@redhat.com> - 0.9.13-7
- do not obsolete openscap-conten just drop it (#1028706)
  scap-security-guide will bring the Obsoletes tag

* Thu Nov 14 2013 Šimon Lukašík <slukasik@redhat.com> - 0.9.13-6
- only non-noarch packages should be requiring specific architecture

* Sat Nov 09 2013 Šimon Lukašík <slukasik@redhat.com> 0.9.13-5
- specify architecture when requiring base package

* Fri Nov 08 2013 Šimon Lukašík <slukasik@redhat.com> 0.9.13-4
- specify dependency between engine and devel sub-package

* Fri Nov 08 2013 Šimon Lukašík <slukasik@redhat.com> 0.9.13-3
- correct openscap-utils dependencies

* Fri Nov 08 2013 Šimon Lukašík <slukasik@redhat.com> 0.9.13-2
- drop openscap-content package (use scap-security-guide instead)

* Fri Nov 08 2013 Šimon Lukašík <slukasik@redhat.com> 0.9.13-1
- upgrade

* Thu Sep 26 2013 Šimon Lukašík <slukasik@redhat.com> 0.9.12-2
- Start building SQL probes for Fedora

* Wed Sep 11 2013 Šimon Lukašík <slukasik@redhat.com> 0.9.12-1
- upgrade

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Lautrbach <plautrba@redhat.com> 0.9.11-1
- upgrade

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.9.10-2
- Perl 5.18 rebuild

* Mon Jul 15 2013 Petr Lautrbach <plautrba@redhat.com> 0.9.10-1
- upgrade

* Mon Jun 17 2013 Petr Lautrbach <plautrba@redhat.com> 0.9.8-1
- upgrade

* Fri Apr 26 2013 Petr Lautrbach <plautrba@redhat.com> 0.9.7-1
- upgrade
- add openscap-selinux sub-package

* Wed Apr 24 2013 Petr Lautrbach <plautrba@redhat.com> 0.9.6-1
- upgrade

* Wed Mar 20 2013 Petr Lautrbach <plautrba@redhat.com> 0.9.5-1
- upgrade

* Mon Mar 04 2013 Petr Lautrbach <plautrba@redhat.com> 0.9.4.1-1
- upgrade

* Tue Feb 26 2013 Petr Lautrbach <plautrba@redhat.com> 0.9.4-1
- upgrade

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Petr Lautrbach <plautrba@redhat.com> 0.9.3-1
- upgrade

* Wed Nov 21 2012 Petr Lautrbach <plautrba@redhat.com> 0.9.2-1
- upgrade

* Mon Oct 22 2012 Petr Lautrbach <plautrba@redhat.com> 0.9.1-1
- upgrade

* Tue Sep 25 2012 Peter Vrabec <pvrabec@redhat.com> 0.9.0-1
- upgrade

* Mon Aug 27 2012 Petr Lautrbach <plautrba@redhat.com> 0.8.5-1
- upgrade

* Tue Aug 07 2012 Petr Lautrbach <plautrba@redhat.com> 0.8.4-1
- upgrade

* Tue Jul 31 2012 Petr Lautrbach <plautrba@redhat.com> 0.8.3-2
- fix Profile and  @hidden issue

* Mon Jul 30 2012 Petr Lautrbach <plautrba@redhat.com> 0.8.3-1
- upgrade

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.8.2-2
- Perl 5.16 rebuild

* Fri Mar 30 2012 Petr Lautrbach <plautrba@redhat.com> 0.8.2-1
- upgrade

* Tue Feb 21 2012 Peter Vrabec <pvrabec@redhat.com> 0.8.1-1
- upgrade

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 0.8.0-3
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Peter Vrabec <pvrabec@redhat.com> 0.8.0-1
- upgrade

* Mon Jul 25 2011 Peter Vrabec <pvrabec@redhat.com> 0.7.4-1
- upgrade

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.7.3-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.7.3-2
- Perl mass rebuild

* Fri Jun 24 2011 Peter Vrabec <pvrabec@redhat.com> 0.7.3-1
- upgrade

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.7.2-3
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.7.2-2
- Perl 5.14 mass rebuild

* Wed Apr 20 2011 Peter Vrabec <pvrabec@redhat.com> 0.7.2-1
- upgrade

* Fri Mar 11 2011 Peter Vrabec <pvrabec@redhat.com> 0.7.1-1
- upgrade

* Thu Feb 10 2011 Peter Vrabec <pvrabec@redhat.com> 0.7.0-1
- upgrade

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Peter Vrabec <pvrabec@redhat.com> 0.6.8-1
- upgrade

* Fri Jan 14 2011 Peter Vrabec <pvrabec@redhat.com> 0.6.7-1
- upgrade

* Wed Oct 20 2010 Peter Vrabec <pvrabec@redhat.com> 0.6.4-1
- upgrade

* Tue Sep 14 2010 Peter Vrabec <pvrabec@redhat.com> 0.6.3-1
- upgrade

* Fri Aug 27 2010 Peter Vrabec <pvrabec@redhat.com> 0.6.2-1
- upgrade

* Wed Jul 14 2010 Peter Vrabec <pvrabec@redhat.com> 0.6.0-1
- upgrade

* Wed May 26 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.11-1
- upgrade

* Fri May 07 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.10-1
- upgrade

* Fri Apr 16 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.9-1
- upgrade

* Fri Feb 26 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.7-1
- upgrade
- new utils package

* Mon Jan 04 2010 Peter Vrabec <pvrabec@redhat.com> 0.5.6-1
- upgrade

* Tue Sep 29 2009 Peter Vrabec <pvrabec@redhat.com> 0.5.3-1
- upgrade

* Wed Aug 19 2009 Peter Vrabec <pvrabec@redhat.com> 0.5.2-1
- upgrade

* Mon Aug 03 2009 Peter Vrabec <pvrabec@redhat.com> 0.5.1-2
- add rpm-devel requirement

* Mon Aug 03 2009 Peter Vrabec <pvrabec@redhat.com> 0.5.1-1
- upgrade

* Thu Apr 30 2009 Peter Vrabec <pvrabec@redhat.com> 0.3.3-1
- upgrade

* Thu Apr 23 2009 Peter Vrabec <pvrabec@redhat.com> 0.3.2-1
- upgrade

* Sun Mar 29 2009 Peter Vrabec <pvrabec@redhat.com> 0.1.4-1
- upgrade

* Fri Mar 27 2009 Peter Vrabec <pvrabec@redhat.com> 0.1.3-2
- spec file fixes (#491892)

* Tue Mar 24 2009 Peter Vrabec <pvrabec@redhat.com> 0.1.3-1
- upgrade

* Thu Jan 15 2009 Tomas Heinrich <theinric@redhat.com> 0.1.1-1
- Initial rpm
