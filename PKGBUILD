# Maintainer: Mallor <mallor@users.noreply.github.com>

pkgname=rewire
pkgver=0.1.3
pkgrel=1
pkgdesc="Intercepts Steam's %command% and replaces it with a configured command"
arch=('any')
url="https://github.com/mall0r/Rewire"
license=('GPL-3.0-or-later')
depends=('python>=3.12')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-pip' 'python-setuptools')
source=("$pkgname-$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl

    install -Dm644 LICENSE -t "$pkgdir/usr/share/licenses/$pkgname"
    install -Dm644 README.md -t "$pkgdir/usr/share/doc/$pkgname"
}
