Summary:	Yacc-like LALR(1) Parser Generator for Haskell
Summary(pl):	Generator parserów LALR(1) w stylu yacc-a dla Haskella
Name:		happy
Version:	1.14
Release:	1
License:	BSD w/o adv. clause
Group:		Development/Languages
URL:		http://haskell.org/happy/
Source0:	http://haskell.org/happy/dist/%{version}/%{name}-%{version}-src.tar.gz
# Source0-md5:	501b5b63533b2e2838de18085e8c4492
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-arch.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ghc
BuildRequires:	gmp-devel
BuildRequires:	jadetex
BuildRequires:	elfutils-libelf
BuildRequires:	ncurses-devel
BuildRequires:	openjade
BuildRequires:	readline-devel
BuildRequires:	sgml-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Happy is a LALR(1) parser generator for Haskell - similar to yacc for
C. It generates a Haskell parser from an annotated BNF specification
of a grammar. Happy allows to have several Happy generated parsers in
one program.

%description -l pl
Happy jest generatorem parserów LALR(1) dla Haskella - podobnym do
yacc-a dla C. Generuje parser w Haskellu ze specyfikacji gramatyki 
w notacji BNF. Happy pozwala mieæ wiele wygenerowanych parserów 
w jednym programie.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure \
	--with-gcc=%{__cc}

%{__make} -C glafp-utils sgmlverb mkdirhier all
%{__make} -C happy/src depend
%{__make} -C happy all
%{__make} -C happy/doc html ps

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man1,%{_examplesdir}/happy}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a happy/examples/* $RPM_BUILD_ROOT%{_examplesdir}/happy/

sed -e 's,@LIBDIR@,%{_libdir}/%{name}-%{version},g' \
	-e 's,@DOCDIR@,%{_docdir}/%{name}-%{version},g' \
	-e 's,@VERSION@,%{version},g' \
	happy/doc/happy.1.in > $RPM_BUILD_ROOT%{_mandir}/man1/happy.1
ln -sf happy-%{version} $RPM_BUILD_ROOT%{_bindir}/happy

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc happy/README happy/doc/happy.ps happy/doc/happy/*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}-%{version}
%attr(755,root,root) %{_libdir}/%{name}-%{version}/happy.bin
%{_libdir}/%{name}-%{version}/Happy*
%{_mandir}/man1/*
