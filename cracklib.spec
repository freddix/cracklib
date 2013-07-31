Summary:	Password checking library
Name:		cracklib
Version:	2.9.0
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://heanet.dl.sourceforge.net/cracklib/%{name}-%{version}.tar.gz
# Source0-md5:	e0f94ac2138fd33c7e77b19c1e9a9390
URL:		http://sourceforge.net/projects/cracklib/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	words
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics. You can use CrackLib to stop users
from choosing passwords which would be easy to guess. CrackLib
performs certain tests:

- It tries to generate words from a username and gecos entry and
  checks those words against the password;
- It checks for simplistic patterns in passwords;
- It checks for the password in a dictionary.

CrackLib is actually a library containing a particular C function
which is used to check the password, as well as other C functions.
CrackLib is not a replacement for a passwd program; it must be used in
conjunction with an existing passwd program.

Install the cracklib package if you need a program to check users'
passwords to see if they are at least minimally secure. If you install
CrackLib, you'll also want to install the cracklib-dicts package.

%package devel
Summary:	Header files and documentation for cracklib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and documentation for cracklib.

%package dicts
Summary:	Standard dictionaries (/usr/share/dict/words)
Group:		Applications/System

%description dicts
The cracklib-dicts package includes the CrackLib dictionaries.
CrackLib will need to use the dictionary appropriate to your system,
which is normally put in /usr/share/dict/words. Cracklib-dicts also
contains the utilities necessary for the creation of new dictionaries.

%package -n python-cracklib
Summary:	Python binding for cracklib
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq  python-libs

%description -n python-cracklib
Python binding for cracklib.

%prep
%setup -q

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoheader}
%{__autoconf}
%configure \
	--disable-static	\
	--without-python	\
	--with-default-dict=%{_datadir}/dict/cracklib_dict
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir},%{_includedir},%{_datadir}/dict}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

chmod +x util/cracklib-format
util/cracklib-format $RPM_BUILD_ROOT%{_datadir}/%{name}/cracklib-small | \
util/cracklib-packer $RPM_BUILD_ROOT%{_datadir}/dict/cracklib-small
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/cracklib-small

mv -f $RPM_BUILD_ROOT%{_localedir}/{sl_SI,sl}

# already in file(1) database
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/cracklib.magic

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %ghost %{_libdir}/libcrack.so.2
%attr(755,root,root) %{_libdir}/libcrack.so.*.*.*
%{_datadir}/dict/cracklib-small.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/cracklib-*
%attr(755,root,root) %{_sbindir}/create-cracklib-dict
%attr(755,root,root) %{_libdir}/libcrack.so
%{_libdir}/libcrack.la
%{_includedir}/*.h

%if 0
%files -n python-cracklib
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_cracklibmodule.so
%{python_sitelib}/*.py[co]
%endif

