Summary:	Yacc-like LALR(1) Parser Generator for Haskell
Name:		happy
Version:	1.10
Release:	1
License:	BSD w/o adv. clause
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/Jêzyki
URL:		http://haskell.org/happy/
Source0:	http://haskell.org/happy/dist/%{version}/%{name}-%{version}-src.tar.gz
Patch0:		%{name}-sgml-CATALOG.patch
Patch1:		%{name}-DESTDIR.patch
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	libelf
BuildRequires:	gmp-devel
BuildRequires:	sgml-common
BuildRequires:	openjade
BuildRequires:	jadetex
BuildRequires:	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Happy is a LALR(1) parser generator for Haskell - similar to yacc for
C. It generates a Haskell parser from an annotated BNF specification
of a grammar. Happy allows to have several Happy generated parsers in
one program.

%prep
%setup -q
#%patch0 -p1
%patch1 -p1

%build
autoconf
%configure \
	--libdir=%{_libdir}/happy-%{version}

%{__make} -C glafp-utils sgmlverb mkdirhier all
%{__make} -C happy all
%{__make} -C happy/doc html ps

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man1,%{_examplesdir}/happy}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install happy/examples/* $RPM_BUILD_ROOT%{_examplesdir}/happy/

sed -e 's,@LIBDIR@,%{_libdir}/%{name}-%{version},g' \
	-e 's,@DOCDIR@,%{_docdir}/%{name}-%{version},g' \
	-e 's,@VERSION@,%{version},g' \
	happy/doc/happy.1.in > $RPM_BUILD_ROOT%{_mandir}/man1/happy.1
ln -s happy-1.10 $RPM_BUILD_ROOT%{_bindir}/happy

gzip -9nf happy/README happy/doc/happy.ps

%files
%defattr(644,root,root,755)
%doc happy/README.gz happy/doc/happy.ps.gz happy/doc/happy/*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}-%{version}
%dir %{_libdir}/%{name}-%{version}/happy
%attr(755,root,root) %{_libdir}/%{name}-%{version}/happy.bin
%{_libdir}/%{name}-%{version}/happy/*
%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT
