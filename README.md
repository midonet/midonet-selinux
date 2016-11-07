# midonet-selinux
SELinux modules for Midonet

Build:
    mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
    spectool -g -R midonet-selinux.spec
    rpmbuild -bb  midonet-selinux.spec
