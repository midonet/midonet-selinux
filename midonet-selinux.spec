%global selinuxtype	targeted
%global moduletype	services
%global modulenames	qemu-kvm-tun

# Usage: _format var format
#   Expand 'modulenames' into various formats as needed
#   Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

# We do this in post install and post uninstall phases # FIXME needed?
%global relabel_files() \
	/sbin/restorecon -Rv %{_bindir}/midonet* %{_bindir}/midolman %{_localstatedir}/log &> /dev/null || :\

# Version of SELinux we were using
%global selinux_policyver 3.13.1-23.el7

# Package information
Name:			midonet-selinux
Version:1.0
Release:1%{?dist}
License:		GPLv2
Group:			System Environment/Base
Summary:		SELinux Policies for Midonet
BuildArch:		noarch
URL:			https://github.com/midonet/%{name}
Requires:		policycoreutils, libselinux-utils
Requires(post):		selinux-policy-base >= %{selinux_policyver}, selinux-policy-targeted >= %{selinux_policyver}, policycoreutils, policycoreutils-python
Requires(postun):	policycoreutils
BuildRequires:		selinux-policy selinux-policy-devel

Source:			qemu-kvm-tun.te

%description
SELinux policy modules for Midonet

#%prep
#%setup -q

%build
make SHARE="%{_datadir}" TARGETS="%{modulenames}"

%install

# Install SELinux interfaces
%_format INTERFACES $x.if
install -d %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 $INTERFACES \
	%{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}

# Install policy modules
%_format MODULES $x.pp.bz2
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 $MODULES \
	%{buildroot}%{_datadir}/selinux/packages

%post
#
# Port rules
#
# bz#1107873
#%{_sbindir}/semanage port -N -a -t amqp_port_t -p tcp 15672 &> /dev/null

#
# Booleans & file contexts
#
#CR=$'\n'
#INPUT="boolean -N -m --on virt_use_fusefs
#boolean -N -m --on glance_use_fusefs
#fcontext -N -a -t neutron_exec_t %{_bindir}/neutron-ns-metadata-proxy
#fcontext -N -a -t neutron_exec_t %{_bindir}/neutron-vpn-agent"

#
# Append modules
#
for x in %{modulenames}; do
  INPUT="${INPUT}${CR}module -N -a %{_datadir}/selinux/packages/$x.pp.bz2"
done

#
# Do everything in one transaction, but don't reload policy
# in case we're in a chroot environment.
#
echo "$INPUT" | %{_sbindir}/semanage import -N

if %{_sbindir}/selinuxenabled ; then
	#
	# Chroot environments (e.g. when building images)
	# won't get here, but the image will apply all of
	# the policy on a reboot.
	#
	%{_sbindir}/load_policy

	%relabel_files
fi


%postun
if [ $1 -eq 0 ]; then
	%{_sbindir}/semodule -n -r %{modulenames} &> /dev/null || :
	if %{_sbindir}/selinuxenabled ; then
		%{_sbindir}/load_policy
		%relabel_files
	fi
fi


%files
%defattr(-,root,root,0755)
%doc COPYING
%attr(0644,root,root) %{_datadir}/selinux/packages/*.pp.bz2
%attr(0644,root,root) %{_datadir}/selinux/devel/include/%{moduletype}/*.if

%changelog
* mon nov 07 2016 Abel Boldú <abel.boldu@midokura.com> - 1.0-1
- Update to 1.0

