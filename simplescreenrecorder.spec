%define shortname ssr
Name:           simplescreenrecorder
Version:        0.3.8
Release:        2%{?dist}
Summary:        Simple Screen Recorder is a screen recorder for Linux

License:        GPLv3
URL:            http://www.maartenbaert.be/simplescreenrecorder/
Source0:        https://github.com/MaartenBaert/ssr/archive/%{version}.tar.gz
Patch0:         fix_ldpath.patch
Patch1:         simplescreenrecorder-0.3.6-fix-build.patch

BuildRequires:  desktop-file-utils
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  ffmpeg-devel
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(xi)
BuildRequires:  qt5-linguist
BuildRequires:  libappstream-glib

Requires:       hicolor-icon-theme
Obsoletes:      %{name}-libs

%description
It is a screen recorder for Linux.
Despite the name, this program is actually quite complex.
It's 'simple' in the sense that it's easier to use than ffmpeg/avconv or VLC

%prep
%autosetup -p1 -n %{shortname}-%{version}


%build
./bootstrap
export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L libavformat libavcodec libavutil libswscale`"
export CPPFLAGS="$CPPFLAGS -fPIC `pkg-config --cflags-only-I libavformat libavcodec libavutil libswscale`"
%configure --with-qt5 \
    --disable-static \
%ifnarch %{ix86} x86_64
    --disable-x86-asm \
%endif
%ifarch %{arm} aarch64
    --disable-glinjectlib \
%endif
%nil
%make_build


%install
%make_install

rm -f %{buildroot}%{_libdir}/*.la
mkdir -p %{buildroot}%{_libdir}/%{name}
%ifnarch %{arm} aarch64
    mv %{buildroot}%{_libdir}/lib%{shortname}-glinject.so %{buildroot}%{_libdir}/%{name}/lib%{shortname}-glinject.so
%endif

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc README.md AUTHORS.md CHANGELOG.md notes.txt todo.txt
%license COPYING
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_bindir}/%{shortname}-glinject
%{_libdir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/%{shortname}-glinject.1.*
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 08 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.8-1
- Update to 0.3.8

* Tue Oct 18 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.7-1
- Update to 0.3.7

* Wed Oct 12 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.6-7
- Switch to use Qt5

* Wed Sep 21 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.6-6
- Add obsoletes

* Tue Sep 20 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.6-5
- Remove libs subpackage

* Fri Aug 26 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.6-4
- Clean spec

* Tue Jun 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.3.6-3.R
- rebuilt against new ffmpeg

* Sun Nov  8 2015 Ivan Epifanov <isage.dna@gmail.com> - 0.3.6-2.R
- Update icon cache

* Wed Nov  4 2015 Ivan Epifanov <isage.dna@gmail.com> - 0.3.6-1.R
- Update to 0.3.6

* Mon Mar 23 2015 Ivan Epifanov <isage.dna@gmail.com> - 0.3.3-1.R
- Update to 0.3.3

* Tue Dec 16 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.1-1.R
- Update to 0.3.1

* Thu Jul  3 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.0-2.R
- Move gl-inject library to subdir

* Thu Jul  3 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.0-1.R
- Initial spec for fedora
