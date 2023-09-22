package main

import (
	"net/http"

	"github.com/go-chi/chi"
)

func pricesRouter() http.Handler {
	r := chi.NewRouter()

	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Prices endpoint"))
	})

	// Define more routes for /prices here

	return r
}
