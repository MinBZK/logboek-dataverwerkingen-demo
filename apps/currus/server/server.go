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
	lc       *LaminaClient
	l        *log.Logger
	operator *logboek.ProcessingOperator
}

func New(address, basePath, laminaURL, logboekEndpoint string) (*Server, error) {
	ctx := context.Background()
	handler, err := logboek.NewGRPCProcessingOperationHandler(ctx, logboekEndpoint)
	if err != nil {
		return nil, err
	}

	s := &Server{
		srv: &http.Server{
			Addr:              address,
			ReadHeaderTimeout: 5 * time.Second,
		},
		db:       NewDB(),
		lc:       NewLaminaClient(laminaURL),
		l:        log.Default(),
		operator: logboek.NewProcessingOperator(handler),
	}

	r := chi.NewRouter()

	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(render.SetContentType(render.ContentTypeJSON))

	r.Get("/", func(w http.ResponseWriter, _ *http.Request) {
		_, _ = w.Write([]byte("Ok\n"))
	})
	r.Route("/parking-permits", func(r chi.Router) {
		r.Route("/{bsn:[0-9]{9}}", func(r chi.Router) {
			r.Get("/", s.listParkingPermitsHandler)
			r.Patch("/{id:[A-Za-z0-9]{27}}", s.patchParkingPermitsHandler)
		})
	})

	s.srv.Handler = logboek_http.NewHandler(r)

	return s, nil
}

func (s *Server) Start() error {
	log.Printf("Listening on %s...", s.srv.Addr)
	return s.srv.ListenAndServe()
}

func (s *Server) listParkingPermitsHandler(w http.ResponseWriter, r *http.Request) {
	_, op := s.operator.StartProcessing(r.Context(), "list_parking_permits")
	op.SetAttributes(attribute.New(attribute.ProcessingActivityIDKey, ProcessingActivityListParkingPermits))
	defer op.End()

	bsn := chi.URLParam(r, "bsn")
	permits := s.db.ListParkingPermits(bsn)

	render.JSON(w, r, permits)

	op.SetStatus(logboek.StatusCodeOK)
}

func (s *Server) patchParkingPermitsHandler(w http.ResponseWriter, r *http.Request) {
	ctx, opChange := s.operator.StartProcessing(r.Context(), "change_parking_permit")
	opChange.SetAttributes(attribute.New(attribute.ProcessingActivityIDKey, ProcessingActivityChangeParkingPermit))
	defer opChange.End()

	bsn := chi.URLParam(r, "bsn")
	id := chi.URLParam(r, "id")

	permit := s.db.GetParkingPermit(bsn, id)
	if permit == nil {
		opChange.SetStatus(logboek.StatusCodeError)
		w.WriteHeader(http.StatusNotFound)
		return
	}

	ctx, opGet := s.operator.StartProcessing(ctx, "get_registration")
	opGet.SetAttributes(attribute.New(attribute.ProcessingActivityIDKey, ProcessingActivityGetRegistration))
	defer opGet.End()

	registrationNumber := r.FormValue("registration_number")
	reg, err := s.lc.GetRegistration(ctx, registrationNumber)
	if err != nil {
		s.l.Printf("failed to get registration: %v\n", err)
		opGet.SetStatus(logboek.StatusCodeError)
		w.WriteHeader(http.StatusServiceUnavailable)
		return
	}

	opGet.SetStatus(logboek.StatusCodeOK)

	if reg.BSN != permit.OwnerBSN {
		opChange.SetStatus(logboek.StatusCodeOK)
		w.WriteHeader(http.StatusUnprocessableEntity)
		return
	}

	permit.RegistrationNumber = r.FormValue("registration_number")

	opChange.SetStatus(logboek.StatusCodeOK)

	w.WriteHeader(http.StatusNoContent)
}
