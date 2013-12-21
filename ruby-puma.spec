#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	puma
Summary:	Puma is a simple, fast, threaded, and highly concurrent HTTP 1.1 server for Ruby/Rack applications
Name:		ruby-%{pkgname}
Version:	2.7.1
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	89767d04de5a39bec0e081d8739e3392
URL:		http://puma.io/
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	ruby-devel
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-hoe < 4
BuildRequires:	ruby-hoe >= 3.7
BuildRequires:	ruby-rake-compiler < 0.9
BuildRequires:	ruby-rake-compiler >= 0.8.0
BuildRequires:	ruby-rdoc < 5
BuildRequires:	ruby-rdoc >= 4.0
%endif
Requires:	ruby-rack < 2.0
Requires:	ruby-rack >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Puma is a simple, fast, threaded, and highly concurrent HTTP 1.1
server for Ruby/Rack applications. Puma is intended for use in both
development and production environments. In order to get the best
throughput, it is highly recommended that you use a Ruby
implementation with real threads like Rubinius or JRuby.

%prep
%setup -q -n %{pkgname}-%{version}
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*

%build
# write .gemspec
%__gem_helper spec

cd ext/puma_http11
%{__ruby} extconf.rb
%{__make} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}

# install ext
install -d $RPM_BUILD_ROOT%{ruby_vendorarchdir}/%{pkgname}
install -p ext/puma_http11/puma_http11.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}/%{pkgname}

# install gemspec
install -d $RPM_BUILD_ROOT%{ruby_specdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/puma
%attr(755,root,root) %{_bindir}/pumactl
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_vendorlibdir}/rack/handler/puma.rb
%attr(755,root,root) %{ruby_vendorarchdir}/puma/puma_http11.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
