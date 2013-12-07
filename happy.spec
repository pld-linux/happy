#
# Conditional build:
%bcond_with	bootstrap	# use foreign (non-rpm) ghc
#
Summary:	Yacc-like LALR(1) Parser Generator for Haskell
Summary(pl.UTF-8):	Generator parserów LALR(1) w stylu yacc-a dla Haskella
Name:		happy
Version:	1.19.2
Release:	1
License:	BSD-like w/o adv. clause
Group:		Development/Tools
#Source0Download: http://hackage.haskell.org/package/happy
Source0:	http://hackage.haskell.org/package/happy-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	36602c3c6e3004f49754ea6c173d2c39
URL:		http://www.haskell.org/happy/
BuildRequires:	autoconf >= 2.50
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
%{!?with_bootstrap:BuildRequires:	ghc >= 6.6}
BuildRequires:	ghc-mtl >= 1.0
BuildRequires:	gmp-devel
BuildRequires:	libxslt-progs
#For generating documentation in PDF: fop or xmltex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Happy is a parser generator system for Haskell, similar to the tool
‘yacc’ for C. Like ‘yacc’, it takes a file containing an annotated BNF
specification of a grammar and produces a Haskell module containing a
parser for the grammar.

Happy is flexible: you can have several Happy parsers in the same
program, and several entry points to a single grammar. Happy can work
in conjunction with a lexical analyser supplied by the user (either
hand-written or generated by another program), or it can parse a
stream of characters directly (but this isn't practical in most
cases).

Authors:
--------
    Simon Marlow <simonmar@microsoft.com>
    Andy Gill <andy@galconn.com>

%description -l pl.UTF-8
Happy to system generatorów parserów dla Haskella, podobny do
narzędzia yacc dla C. Na podstawie specyfikacji gramatyki w notacji
BNF generuje moduł w Haskellu zawierający parser tej gramatyki.

Happy jest elastyczny: można mieć kilka parserów wygenerowanych przez
Happy w jednym programie tudzież kilka symboli startowych dla tej
samej gramatyki. Happy może współpracować z analizatorem leksykalnym
dostarczonym przez programistę (napisanym ręcznie albo wygenerowanym
przez inny program), może też parsować strumień znaków bezpośrednio
(co zwykle jest mniej praktyczne).

Autorzy:
--------
    Simon Marlow <simonmar@microsoft.com>
    Andy Gill <andy@galconn.com>

%prep
%setup -q

%build
%{?with_bootstrap:PATH=$PATH:/usr/local/bin}
runhaskell Setup.lhs configure --prefix=%{_prefix}
runhaskell Setup.lhs build

cd doc
%{__autoconf}
%configure
%{__make} html
cd ..

%install
rm -rf $RPM_BUILD_ROOT
%{?with_bootstrap:PATH=$PATH:/usr/local/bin}
runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ANNOUNCE CHANGES README TODO doc/happy
%attr(755,root,root) %{_bindir}/happy
%{_datadir}/%{name}-%{version}
%{_examplesdir}/%{name}-%{version}
