#!/usr/bin/env bash
# Build an RPM package for Fedora / RHEL.
# Requires: rpm-build, python3, python3-pip, unzip
#
# Usage:
#   sudo dnf install rpm-build python3-pip unzip   # on Fedora
#   sudo apt install rpm python3-pip unzip          # on Ubuntu (cross-build)
#   ./build_rpm.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
RPM_DIR="${ROOT_DIR}/build/rpm"
SPEC_FILE="${ROOT_DIR}/rpm/SPECS/mdviewer.spec"
PKG_VERSION="1.0.0"
PKG_RELEASE="1"

mkdir -p "${RPM_DIR}"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# ---- create source tarball ----
echo "Creating source tarball..."
cd "${ROOT_DIR}"
tar czf "${RPM_DIR}/SOURCES/mdviewer-${PKG_VERSION}.tar.gz" \
    --transform "s|^|mdviewer-${PKG_VERSION}/|" \
    mdviewer/ \
    rpm/mdviewer.spec

# ---- write spec file ----
mkdir -p "$(dirname "${SPEC_FILE}")"

cat > "${SPEC_FILE}" << 'SPEC'
%global pkg_name mdviewer

Name:           %{pkg_name}
Version:        1.0.0
Release:        1%{?dist}
Summary:        Markdown viewer that renders files in your browser

License:        MIT
URL:            https://github.com/example/mdviewer
Source0:        %{pkg_name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       python3 >= 3.10
BuildRequires:  python3 python3-pip unzip

%description
mdviewer converts Markdown files to styled HTML pages with syntax
highlighting and opens them in your default browser. It bundles all
Python dependencies -- no pip install required.

%prep
%setup -q -n %{pkg_name}-%{version}

%build
# Nothing to compile, pure Python

%install
# Directories
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}/mdviewer
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}/deps
mkdir -p %{buildroot}%{_mandir}/man1

# Python module
cp -r mdviewer/*.py %{buildroot}%{_datadir}/%{pkg_name}/mdviewer/

# Vendored deps
python3 -m pip download \
    --only-binary=:all: --no-deps \
    --dest /tmp/mdviewer-wheels \
    mistune pygments 2>&1 | tail -3

for wheel in /tmp/mdviewer-wheels/*.whl; do
    unzip -q -o "$wheel" -d %{buildroot}%{_datadir}/%{pkg_name}/deps/
done
rm -rf /tmp/mdviewer-wheels

# Wrapper script
cat > %{buildroot}%{_bindir}/mdviewer << 'WRAPPER'
#!/bin/sh
PYTHONPATH="/usr/share/mdviewer/deps:/usr/share/mdviewer${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH
exec /usr/bin/python3 -m mdviewer "$@"
WRAPPER
chmod 755 %{buildroot}%{_bindir}/mdviewer

# Man page
cat > %{buildroot}%{_mandir}/man1/mdviewer.1 << 'MAN'
.TH MDVIEWER 1 "June 2026" "mdviewer 1.0.0" "User Commands"
.SH NAME
mdviewer \- render Markdown files in your browser
.SH SYNOPSIS
.B mdviewer
[\fI\,OPTIONS\/\fR] \fI\,FILE\/\fR
.SH DESCRIPTION
mdviewer converts a Markdown file to a styled HTML page and opens it in your default browser.
.SH OPTIONS
.TP
.B \-o, \-\-output FILE
Write HTML to FILE instead of opening browser.
.TP
.B \-\-no-browser
Render to a temp file but do not open the browser.
.TP
.B \-\-stdout
Print the rendered HTML to standard output.
.TP
.B \-\-title TITLE
Set the HTML page title (default: filename without extension).
.SH EXAMPLE
.B mdviewer README.md
.P
.B mdviewer --stdout notes.md > notes.html
.SH AUTHOR
Written by the mdviewer project.
MAN
gzip -f %{buildroot}%{_mandir}/man1/mdviewer.1

%files
%{_bindir}/mdviewer
%{_datadir}/%{pkg_name}/deps/
%{_datadir}/%{pkg_name}/mdviewer/
%{_mandir}/man1/mdviewer.1.gz

%changelog
* Sat Jun 27 2026 mdviewer developers <dev@mdviewer.local> 1.0.0-1
- Initial RPM release
SPEC

# ---- build ----
echo "Building RPM..."
rpmbuild --define "_topdir ${RPM_DIR}" -ba "${SPEC_FILE}"

# ---- show results ----
echo ""
echo "=== RPM package built ==="
find "${RPM_DIR}/RPMS" -name "*.rpm" -exec ls -lh {} \;
