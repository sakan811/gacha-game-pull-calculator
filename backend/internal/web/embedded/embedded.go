package embedded

import (
	"embed"
	"io/fs"
	"net/http"
)

//go:embed dist/*
var staticFiles embed.FS

// GetFileSystem returns the embedded static files as http.FileSystem
func GetFileSystem() http.FileSystem {
	fsys, err := fs.Sub(staticFiles, "dist")
	if err != nil {
		panic(err)
	}
	return http.FS(fsys)
}
