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

release:
	goreleaser release --clean --parallelism 2
