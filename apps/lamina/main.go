package main

import (
	"flag"
	"log"
	"os"

	"github.com/MinBZK/logboek-dataverwerkingen-demo/apps/lamina/server"
)

type options struct {
	listenAddress   string
	apiBasePath     string
	logboekEndpoint string
}

func parseFlags() *options {
	o := &options{}
	flag.StringVar(&o.listenAddress, "listen-address", envValue("LISTEN_ADDRESS", "127.0.0.1:8082"), "Listen address")
	flag.StringVar(&o.logboekEndpoint, "logboek-endpoint", envValue("LOGBOEK_ENDPOINT", "127.0.0.1:9000"), "Address of a logboek server")

	flag.Parse()

	return o
}

func main() {
	o := parseFlags()

	srv, err := server.New(o.listenAddress, o.apiBasePath, o.logboekEndpoint)
	if err != nil {
		log.Fatalf("Creating server: %v", err)
	}

	log.Println("Starting server...")
	if err := srv.Start(); err != nil {
		log.Fatal(err)
	}
}

func envValue(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}
