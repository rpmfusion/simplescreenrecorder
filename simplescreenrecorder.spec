%global shortname ssr

%undefine __cmake_in_source_build

Name:           simplescreenrecorder
Version:        0.4.4
Release:        5%{?dist}
Summary:        Simple Screen Recorder is a screen recorder for Linux

License:        GPLv3
URL:            https://www.maartenbaert.be/simplescreenrecorder/
Source0:        https://github.com/MaartenBaert/ssr/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         0001-Fix-libssr-glinject.so-preload-path.patch
Patch1:         https://github.com/MaartenBaert/ssr/pull/934.patch

BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  cmake3
BuildRequires:  ffmpeg-devel
BuildRequires:  pkgconfig(Qt5) >= 5.7.0
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(xi)
BuildRequires:  qt5-linguist
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(libv4l2)

Requires:       hicolor-icon-theme
Obsoletes:      %{name}-libs < %{version}-3


%description
It is a screen recorder for Linux.
Despite the name, this program is actually quite complex.
It's 'simple' in the sense that it's easier to use than ffmpeg/avconv or VLC

%prep
%autosetup -p1 -n %{shortname}-%{version}


%build
%cmake3 \
        -DCMAKE_BUILD_TYPE=Release \
        -DWITH_QT5=TRUE \
%ifnarch %{ix86} x86_64
        -DENABLE_X86_ASM=FALSE \
%endif
%ifarch %{arm} aarch64 %{power64}
        -DWITH_GLINJECT=FALSE \
%endif
%cmake3_build


%install
%cmake3_install

rm -f %{buildroot}%{_libdir}/*.la
mkdir -p %{buildroot}%{_libdir}/%{name}/
%ifnarch %{arm} aarch64 %{power64}
    mv %{buildroot}%{_libdir}/lib%{shortname}-glinject.so %{buildroot}%{_libdir}/%{name}/lib%{shortname}-glinject.so
%endif

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.metainfo.xml

%files
%doc README.md AUTHORS.md CHANGELOG.md notes.txt todo.txt
%license COPYING
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_bindir}/%{shortname}-glinject
%{_libdir}/%{name}/
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/%{shortname}-glinject.1.*
%{_datadir}/metainfo/%{name}.metainfo.xml

%changelog
* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 01 2023 Leigh Scott <leigh123linux@gmail.com> - 0.4.4-3
- Rebuild for new ffmpeg

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Tue Apr 05 2022 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.4-1
- Update to 0.4.4

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
- Add ffmpeg-5 patch

* Fri Nov 12 2021 Leigh Scott <leigh123linux@gmail.com> - 0.4.3-4
- Rebuilt for new ffmpeg snapshot

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 10 2021 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.3-1
- Update to 0.4.3

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 0.4.2-4
- Rebuilt for new ffmpeg snapshot

* Mon Sep 21 2020 Nicolas Chauvet <kwizart@gmail.com> - 0.4.2-3
- Drop ppc64 exclude
- Add versionned obsoletes

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 19 2020 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.2-1
- Update to 0.4.2

* Fri May 15 2020 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.1-1
- Update to 0.4.1

* Thu Apr 23 2020 Vasiliy N. Glazov <vascom2@gmail.com> - 0.4.0-2
- Restored translations

* Sat Apr 11 2020 Leigh Scott <leigh123linux@gmail.com> - 0.4.0-1
- Update to 4.0.0
- Remove scriptlets
- Add BuildRequires libXinerama-devel

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.3.11-10
- Rebuild for ffmpeg-4.3 git

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 0.3.11-8
- Rebuild for new ffmpeg version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 21 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.11-6
- Enable translations

* Mon Feb 04 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.11-5
- Added preload patch

* Wed Nov 14 2018 Antonio Trande <sagitter@fedoraproject.org> - 0.3.11-4
- Rebuild for ffmpeg-3.4.5 on el7

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.3.11-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.11-1
- Update to 0.3.11

* Tue Mar 13 2018 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.10-1
- Update to 0.3.10

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.3.9-5
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.3.9-3
- Rebuilt for ffmpeg-3.5 git

* Wed Dec 13 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.3.9-2
- Use build requires cmake3 instead of cmake

* Wed Dec 13 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.9-1
- Update to 0.3.9
- Switch to use cmake for build

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.3.8-4
- Rebuild for ffmpeg update

* Mon Apr 17 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.8-3
- Exclude power64 arches from build

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
