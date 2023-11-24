# Configuration Logic
%define name unclebench
%define version 1.1.1
%define unmangled_version 1.1.1
%define debug_package %{nil}
%undefine __brp_mangle_shebangs

# Main preamble
Summary: UncleBench is a tool for automating the running of complex benchmarks on HPC infrastructures.
Name: unclebench
Version: 1.1.1
Release:  1%{?dist}.edf
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPLv3
Group: Application/System
Prefix: %{_prefix}
Vendor: EDF CCN HPC <dsp-cspito-ccn-hpc@edf.fr>
Packager: EDF CCN HPC <dsp-cspito-ccn-hpc@edf.fr>
Url: https://github.com/scibian/%{__name}

BuildRequires: git python36 python3-setuptools pandoc texlive-latex rubygem-asciidoctor
Requires: python3-clustershell python3-jinja2 python3-matplotlib
Requires: python3-pyyaml python3-lxml python3-pandas 
Requires: jube python3-seaborn
Requires: unclebench-benchmarks unclebench-platform

%description
This is a meta-package that provides UncleBench software.
UncleBench is a tool for automating the running of complex benchmarks on HPC infrastructures.

#########################################
# Prep, Setup, Build, Install & clean   #
#########################################

%prep
%setup -q

# Build Section
%build
python3 setup.py build
mkdir docs/man
make --directory=docs

# Install & clean sections

%install
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}
install -d %{buildroot}/etc/unclebench
install -d %{buildroot}/usr/share/unclebench/
install -d %{buildroot}/usr/share/unclebench/docs
cp -r docs/man %{buildroot}/usr/share/unclebench/docs/
cp -r platform %{buildroot}/usr/share/unclebench/
cp -r benchmarks %{buildroot}/usr/share/unclebench/
cp -r css %{buildroot}/usr/share/unclebench/
cp -r templates %{buildroot}/usr/share/unclebench/
install -m 644 configuration/ubench.conf %{buildroot}/etc/unclebench
install -m 644 docs/user_guide.html %{buildroot}/usr/share/unclebench/docs/
install -m 644 docs/developer_guide.html %{buildroot}/usr/share/unclebench/docs/
install -m 644 docs/benchmarks_guide.html %{buildroot}/usr/share/unclebench/docs/
install -m 644 docs/platform_guide.html %{buildroot}/usr/share/unclebench/docs/

%clean
rm -rf %{buildroot}

#############
# Preambles #
#############

# unclebench-benchmarks package preamble
%package benchmarks
Summary: Benchmark description files for UncleBench.
Group: Application/System
Requires: git asciidoctor
%description benchmarks
Benchmarks description files for UncleBench benchmarking tool
The package provide examples of xml benchmark description files.

# unclebench-platform package preamble
%package platform
Summary: Platform description files for UncleBench benchmarking tool.
Group: Application/System
Requires: git asciidoctor
%description platform
Platform description files for UncleBench benchmarking tool
The package provide examples of xml platform description files.

##################
# Files Sections #
##################

# Main meta-package
%files
%defattr(-,root,root,-)
%doc README.md
%doc /usr/share/unclebench/docs/developer_guide.html
#%doc /usr/share/unclebench/docs/campaign_guide.html
%doc /usr/share/unclebench/docs/user_guide.html
%doc /usr/share/unclebench/docs/man/ubench.1
%doc /usr/share/unclebench/docs/man/ubench-compare.1
%doc /usr/share/unclebench/docs/man/ubench-fetch.1
%doc /usr/share/unclebench/docs/man/ubench-list.1
%doc /usr/share/unclebench/docs/man/ubench-listparams.1
%doc /usr/share/unclebench/docs/man/ubench-log.1
%doc /usr/share/unclebench/docs/man/ubench-report.1
%doc /usr/share/unclebench/docs/man/ubench-result.1
%doc /usr/share/unclebench/docs/man/ubench-run.1
%config /etc/unclebench/ubench.conf
/usr/bin/ubench
%{python3_sitelib}/ubench
%{python3_sitelib}/*.egg-info
/usr/share/unclebench/css
/usr/share/unclebench/templates

# benchmarks
%files benchmarks
%defattr(-,root,root,-)
%doc /usr/share/unclebench/docs/benchmarks_guide.html
/usr/share/unclebench/benchmarks

# platform
%files platform
%defattr(-,root,root,-)
%doc /usr/share/unclebench/docs/platform_guide.html
/usr/share/unclebench/platform

%changelog
* Fri Nov 24 2023 Kwame Amedodji <kwame-externe.amedodji@edf.fr> 1.1.1-1el8.edf
- New upstream version 1.1.1

* Thu May 18 2023 Kwame Amedodji <kwame-externe.amedodji@edf.fr> 1.1.0-1el8.edf
- New upstream version 1.1.0

* Fri Mar 17 2023 Kwame Amedodji <kwame-externe.amedodji@edf.fr> 1.0.2-6el8.edf
- rename asciidoctor package to rubygem-asciidoctor
- relocate docs to /usr/share/unclebench from /!

* Thu Mar 16 2023 Mhemed Mtimet <mhemed-externe.mtimet@edf.fr> 1.0.2-5el8.edf
- fix build error related to name , version variable

* Tue Jan 12 2021 Romaric Kanyamibwa <romaric-externe.kanyamibwa@edf.fr> 1.0.2-4el8.edf
- Add benchmark and platform meta-package

* Wed Dec 16 2020 Romaric Kanyamibwa <romaric-externe.kanyamibwa@edf.fr> 1.0.2-3el8.edf
- Add edf-unclebench-benchmarks

* Tue Dec 15 2020 Romaric Kanyamibwa <romaric-externe.kanyamibwa@edf.fr> 1.0.2-2el8.edf
- Add edf-unclebench-platforms

* Fri Oct 23 2020 Romaric Kanyamibwa <romaric-externe.kanyamibwa@edf.fr> 1.0.2-1el8.edf
- Initial RPM release
