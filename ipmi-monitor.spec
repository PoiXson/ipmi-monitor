Name            : ipmi-monitor
Summary         : A cron script to monitor a systems ipmi using ipmiutil
Version         : 1.4.3.%{BUILD_NUMBER}
Release         : 1
BuildArch       : noarch
Provides        : ipmimonitor,ipmi-monitor
Requires        : cronie
Prefix          : %{_bindir}/ipmi-monitor
%define _rpmfilename  %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm

Group           : Base System/System Tools
License         : (c) PoiXson
Packager        : PoiXson <support@poixson.com>
URL             : http://poixson.com/

%description
A cron script to monitor a systems ipmi using ipmiutil.



# avoid centos 5/6 extras processes on contents (especially brp-java-repack-jars)
%define __os_install_post %{nil}

# disable debug info
# % define debug_package %{nil}



### Prep ###
%prep



### Build ###
%build



### Install ###
%install
echo
echo "Install.."
# delete existing rpm's
%{__rm} -fv "%{_rpmdir}/%{name}-"*.noarch.rpm
# create directories
%{__install} -d -m 0755 \
	"${RPM_BUILD_ROOT}%{prefix}/" \
	"${RPM_BUILD_ROOT}%{_sysconfdir}/cron.d/" \
		|| exit 1
# copy script files
for scriptfile in \
	ipmi-monitor.sh   \
; do
	%{__install} -m 0555 \
		"%{SOURCE_ROOT}/src/${scriptfile}" \
		"${RPM_BUILD_ROOT}%{prefix}/${scriptfile}" \
			|| exit 1
done
# copy cron.d file
%{__install} -m 0644 \
	"%{SOURCE_ROOT}/src/ipmi-monitor-cron" \
	"${RPM_BUILD_ROOT}%{_sysconfdir}/cron.d/ipmi-monitor-cron" \
		|| exit 1
# copy config file
%{__install} -m 0644 \
	"%{SOURCE_ROOT}/src/ipmi-monitor.conf" \
	"${RPM_BUILD_ROOT}%{_sysconfdir}/ipmi-monitor.conf" \
		|| exit 1
# alias symlinks
ln -sf  "%{prefix}/ipmi-monitor.sh"  "${RPM_BUILD_ROOT}%{_bindir}/ipmi-monitor"



%check



%clean
if [ ! -z "%{_topdir}" ]; then
	%{__rm} -rf --preserve-root "%{_topdir}" \
		|| echo "Failed to delete build root!"
fi



### Files ###
%files
%defattr(-,root,root,-)
%{prefix}/ipmi-monitor.sh
%{_bindir}/ipmi-monitor
%config %{_sysconfdir}/ipmi-monitor.conf
%config %{_sysconfdir}/cron.d/ipmi-monitor-cron
