# Configuration Logic
%define name unclebench
%define version 1.0.2
%define unmangled_version 1.0.2
%define debug_package %{nil}
%undefine __brp_mangle_shebangs

# Main preamble
Summary: UncleBench is a tool for automating the running of complex benchmarks on HPC infrastructures.
Name: unclebench
Version: 1.0.2
Release:  4%{?dist}.edf
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPLv3
Group: Application/System
Prefix: %{_prefix}
Vendor: EDF CCN HPC <dsp-cspito-ccn-hpc@edf.fr>
Packager: EDF CCN HPC <dsp-cspito-ccn-hpc@edf.fr>
Url: https://github.com/scibian/%{__name}

BuildRequires: git python36 python3-setuptools pandoc texlive-latex asciidoctor
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
install -d %{buildroot}/docs
cp -r docs/man %{buildroot}/docs/
cp -r platform %{buildroot}/usr/share/unclebench/
cp -r benchmarks %{buildroot}/usr/share/unclebench/
cp -r css %{buildroot}/usr/share/unclebench/
cp -r templates %{buildroot}/usr/share/unclebench/
install -m 644 configuration/ubench.conf %{buildroot}/etc/unclebench
install -m 644 docs/user_guide.html %{buildroot}/docs/
install -m 644 docs/developer_guide.html %{buildroot}/docs/
install -m 644 docs/benchmarks_guide.html %{buildroot}/docs/

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
%doc /docs/developer_guide.html
#%doc /docs/campaign_guide.html
%doc /docs/user_guide.html
%doc /docs/man/ubench.1
%doc /docs/man/ubench-compare.1
%doc /docs/man/ubench-fetch.1
%doc /docs/man/ubench-list.1
%doc /docs/man/ubench-listparams.1
%doc /docs/man/ubench-log.1
%doc /docs/man/ubench-report.1
%doc /docs/man/ubench-result.1
%doc /docs/man/ubench-run.1
%config /etc/unclebench/ubench.conf
/usr/bin/ubench
%{python3_sitelib}/ubench
%{python3_sitelib}/*.egg-info
/usr/share/unclebench/css
/usr/share/unclebench/templates

# benchmarks
%files benchmarks
%defattr(-,root,root,-)
%doc /docs/benchmarks_guide.html
/usr/share/unclebench/benchmarks

# platform
%files platform
%defattr(-,root,root,-)
%doc /docs/platform_guide.html
/usr/share/unclebench/platform

%changelog
* Tue Jan 12 2021 Romaric Kanyamibwa <romaric-externe.kanyamibwa@edf.fr> 1.0.2-4el8.edf
- Add benchmark and platform meta-package

* Wed Dec 16 2020 Romaric Kanyamibwa <romaric-externe.kanyamibwa@edf.fr> 1.0.2-3el8.edf
- Add edf-unclebench-benchmarks

* Tue Dec 15 2020 Romaric Kanyamibwa <romaric-externe.kanyamibwa@edf.fr> 1.0.2-2el8.edf
- Add edf-unclebench-platforms

* Fri Oct 23 2020 Romaric Kanyamibwa <romaric-externe.kanyamibwa@edf.fr> 1.0.2-1el8.edf
- Initial RPM release
