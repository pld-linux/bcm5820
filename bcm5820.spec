Summary:	Broadcom BCM5820 E-Commerce Processor utilities
Summary(pl.UTF-8):	Narzędzia dla akceleratora kryptograficznego Broadcom BCM5820
Name:		bcm5820
Version:	1.81
Release:	1
License:	GPL
Group:		Applications/System
Source0:	%{name}-%{version}.tgz
# Source0-md5:	5f5b3a57c313e7b2bfb0c3f7e81afee5
Patch0:		%{name}-link.patch
Patch1:		%{name}-log.patch
Patch2:		%{name}-noclear.patch
Patch3:		%{name}-c.patch
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Broadcom BCM5820 E-Commerce Processor utilities.

%description -l pl.UTF-8
Narzędzia dla akceleratora kryptograficznego Broadcom BCM5820
E-Commerce Processor.

%package libs
Summary:	Broadcom uBSec SDK library
Summary(pl.UTF-8):	Biblioteka Broadcom uBSec SDK
Group:		Libraries

%description libs
Broadcom uBSec SDK library.

%description libs -l pl.UTF-8
Biblioteka Broadcom uBSec SDK.

%package devel
Summary:	Header files for uBSec library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki uBSec
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for uBSec library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki uBSec.

%package static
Summary:	Static uBSec library
Summary(pl.UTF-8):	Statyczna biblioteka uBSec
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static uBSec library.

%description static -l pl.UTF-8
Statyczna biblioteka uBSec.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make} -C cndiag \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -c -I../Linux -I../SRL"

%{__make} -C ubslib \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I../SRL -I../Linux -DUSER_APPLICATION" \
	SHRCFLAGS="%{rpmcflags} -c -fPIC -I../SRL -I../Linux -DUSER_APPLICATION"

%{__make} -C stats \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -c -I../ubslib -I../SRL -I../Linux"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir},%{_includedir}}

install ubslib/libubsec.so $RPM_BUILD_ROOT%{_libdir}/libubsec.so.0
ln -sf libubsec.so.0 $RPM_BUILD_ROOT%{_libdir}/libubsec.so
install ubslib/libubsec.a $RPM_BUILD_ROOT%{_libdir}

install cndiag/b58diag stats/b58stats $RPM_BUILD_ROOT%{_sbindir}

install SRL/ubsec.h Linux/ubsio.h ubslib/ubsec_lib.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/b58diag
%attr(755,root,root) %{_sbindir}/b58stats

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libubsec.so.*
# dlopened by openssl engine
%attr(755,root,root) %{_libdir}/libubsec.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/ubsec.h
%{_includedir}/ubsec_lib.h
%{_includedir}/ubsio.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libubsec.a
