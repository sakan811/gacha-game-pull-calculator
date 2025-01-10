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
	// First try to get the dist subdirectory
	fsys, err := fs.Sub(staticFiles, "dist")
	if err != nil {
		// If dist subdirectory doesn't exist, try using the root
		return http.FS(staticFiles)
	}
	return http.FS(fsys)
}
