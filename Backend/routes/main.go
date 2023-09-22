package main

import (
	"net/http"

	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
)

func main() {
	r := chi.NewRouter()
	r.Use(middleware.Logger)

	// Mount the prices router
	r.Mount("/prices", pricesRouter())

	// Start server
	http.ListenAndServe(":8080", r)
}
