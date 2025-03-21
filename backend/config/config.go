package config

import "os"

type Config struct {
	Port        string
	BindAddress string
}

func LoadConfig() *Config {
	bindAddress := os.Getenv("GIN_BIND")
	if bindAddress == "" {
		bindAddress = "0.0.0.0" // Default to all interfaces
	}

	return &Config{
		Port:        "8080",
		BindAddress: bindAddress,
	}
}
