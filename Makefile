.PHONY:	rpm clean

VERSION ?= 0.1
BUILD_NUMBER ?= 1
TOPDIR = /tmp/midonet-selinux-rpm
PWD = $(shell pwd)
TARGETS?=docker-engine
MODULES?=${TARGETS:=.pp.bz2}
SHAREDIR?=/usr/share


rpm:
	@rpmbuild -v -bb \
			--define "_sourcedir $(PWD)" \
			--define "_rpmdir $(PWD)" \
			--define "_topdir $(TOPDIR)" \
			--define "version $(VERSION)" \
			--define "build_number $(BUILD_NUMBER)" \
			midonet-selinux.spec

clean:
	@rm -rf $(TOPDIR) noarch
	rm -f *~ *.tc *.pp *.pp.bz2
	rm -rf tmp *.tar.gz

all: ${TARGETS:=.pp.bz2}

%.pp.bz2: %.pp
	@echo Compressing $^ -\> $@
	bzip2 -9 $^

%.pp: %.te
	make -f ${SHAREDIR}/selinux/devel/Makefile $@

