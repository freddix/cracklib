Summary:	Password checking library
Name:		cracklib
Version:	2.9.1
Release:	1
License:	GPL v2
Group:		Core/Libraries
Source0:	http://downloads.sourceforge.net/project/cracklib/cracklib/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	90536219c520add2ceb3c26f0d7da404
URL:		http://sourceforge.net/projects/cracklib/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	words
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CrackLib is a library containing a C function (well, lots of functions
really, but you only need to use one of them) which may be used in a
"passwd"-like program.

%package devel
Summary:	Header files and libraries for cracklib development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and libraries needed to develop programs which make use
of cracklib library.

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
	--without-python
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir},%{_includedir},%{_datadir}/dict}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

util/cracklib-format $RPM_BUILD_ROOT%{_datadir}/%{name}/cracklib-small | \
util/cracklib-packer $RPM_BUILD_ROOT%{_datadir}/dict/cracklib-small
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/cracklib-small

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sl_SI,sl}

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

