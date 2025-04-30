GO_VERSION=1.24.1

.PHONY: neosync-exporter-build
neosync-exporter-build:
	cd neosync_exporter && go mod tidy && CGO_ENABLED=1 go build -ldflags='-w -s' -o main.so -buildmode=c-shared main.go
