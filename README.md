# midonet-selinux
SELinux modules for Midonet

Build:

    rpmdev-setuptree
    spectool -g -R midonet-selinux.spec
    rpmbuild -bb  midonet-selinux.spec
