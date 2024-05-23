package server

import (
	"context"
	"log"
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/render"

	"github.com/MinBZK/logboek-dataverwerkingen-logboek/libs/logboek-go"
	"github.com/MinBZK/logboek-dataverwerkingen-logboek/libs/logboek-go/attribute"
	logboek_http "github.com/MinBZK/logboek-dataverwerkingen-logboek/libs/logboek-go/http"
)

type Server struct {
	srv      *http.Server
	db       *DB
	l        *log.Logger
	operator *logboek.ProcessingOperator
}

func New(address, basePath, logboekEndpoint string) (*Server, error) {
	ctx := context.Background()

	handler, err := logboek.NewGRPCProcessingOperationHandler(ctx, logboekEndpoint)
	if err != nil {
		return nil, err
	}
	operator := logboek.NewProcessingOperator(handler)

	s := &Server{
		srv: &http.Server{
			Addr:              address,
			ReadHeaderTimeout: 5 * time.Second,
		},
		db:       NewDB(),
		l:        log.Default(),
		operator: operator,
	}

	r := chi.NewRouter()

	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(render.SetContentType(render.ContentTypeJSON))

	r.Get("/", func(w http.ResponseWriter, _ *http.Request) {
		_, _ = w.Write([]byte("Ok\n"))
	})
	r.Route("/registrations", func(r chi.Router) {
		r.Get("/{registration_number:[A-Z0-9]{6}}", s.getRegistrationHandler)
	})

	s.srv.Handler = logboek_http.NewHandler(r)

	return s, nil
}

func (s *Server) Start() error {
	log.Printf("Listening on %s...", s.srv.Addr)
	return s.srv.ListenAndServe()
}

func (s *Server) getRegistrationHandler(w http.ResponseWriter, r *http.Request) {
	_, op := s.operator.StartProcessing(r.Context(), "get_registration")
	op.SetAttributes(attribute.New(attribute.ProcessingActivityIDKey, ProcessingActivityGetRegistration))
	defer op.End()

	regisration_number := chi.URLParam(r, "registration_number")
	registration := s.db.GetRegistration(regisration_number)

	if registration == nil {
		w.WriteHeader(http.StatusNotFound)
		return
	}

	render.JSON(w, r, registration)
}
