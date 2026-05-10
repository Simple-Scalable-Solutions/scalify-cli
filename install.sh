#!/bin/sh
set -e

REPO="Simple-Scalable-Solutions/scalify-cli"
BINARY="scalify-cli"
VERSION="${VERSION:-$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name"' | cut -d'"' -f4 | sed 's/^v//')}"
VERSION="${VERSION:-1.0.1}"
INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"

# Detect OS
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
case "$OS" in
  darwin|linux) ;;
  *) echo "Unsupported OS: $OS" >&2; exit 1 ;;
esac

# Detect arch
ARCH=$(uname -m)
case "$ARCH" in
  x86_64|amd64) ARCH="amd64" ;;
  arm64|aarch64) ARCH="arm64" ;;
  *) echo "Unsupported architecture: $ARCH" >&2; exit 1 ;;
esac

FILENAME="${BINARY}_${VERSION}_${OS}_${ARCH}.tar.gz"
URL="https://github.com/${REPO}/releases/download/v${VERSION}/${FILENAME}"

echo "Installing ${BINARY} v${VERSION} (${OS}/${ARCH})..."

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$URL" -o "$TMP/$FILENAME"
elif command -v wget >/dev/null 2>&1; then
  wget -qO "$TMP/$FILENAME" "$URL"
else
  echo "Error: curl or wget required" >&2; exit 1
fi

tar -xzf "$TMP/$FILENAME" -C "$TMP" "$BINARY"

if [ -w "$INSTALL_DIR" ]; then
  mv "$TMP/$BINARY" "$INSTALL_DIR/$BINARY"
else
  sudo mv "$TMP/$BINARY" "$INSTALL_DIR/$BINARY"
fi

echo "Installed to ${INSTALL_DIR}/${BINARY}"
echo ""
echo "Next: set your API token"
echo "  ${BINARY} auth set-token"
