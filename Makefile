.PHONY: build test lint install clean

build:
	go build -o bin/scalify-pp-cli ./cmd/scalify-pp-cli

test:
	go test ./...

lint:
	golangci-lint run

install:
	go install ./cmd/scalify-pp-cli

clean:
	rm -rf bin/

build-mcp:
	go build -o bin/scalify-pp-mcp ./cmd/scalify-pp-mcp

install-mcp:
	go install ./cmd/scalify-pp-mcp

build-all: build build-mcp

# make release NOTES=docs/releases/v2.0.0.md  (Go 1.26.3: the version every build and test used)
release:
	GOTOOLCHAIN=go1.26.3 GITHUB_TOKEN=$$(gh auth token) goreleaser release --clean --parallelism 2 $(if $(NOTES),--release-notes $(NOTES))
