# COPR "make_srpm" build method.
# COPR runs:  make -f .copr/Makefile srpm outdir=<dir> spec=<spec>
# from the root of the git repository and builds the RPM from the resulting SRPM.

SPEC := branding/fedorium-branding.spec

srpm:
	dnf -y install rpm-build
	mkdir -p $(outdir)
	rpmbuild -bs \
		--define "_sourcedir $(CURDIR)/branding/files" \
		--define "_srcrpmdir $(outdir)" \
		$(SPEC)
