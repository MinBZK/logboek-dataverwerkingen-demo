package server

import (
	"time"
)

var permits = []*ParkingPermit{
	{"2cdB1AxNITm0A01PfMIlLiyUsoe", "686242", "999995042", "H358BH", newDate(2023, 10, 10), newDate(2024, 10, 9)},
	{"2cdB19Dd3PM9Snrk2EIiuO0u115", "278322", "999995042", "9ZTJ69", newDate(2024, 1, 8), newDate(2024, 8, 10)},
	{"2cdB1Fd1USUEdVG45oPqgTviipn", "302957", "999993161", "ZV326K", newDate(2023, 10, 10), newDate(2024, 10, 9)},
	{"2cdB18iPqsH00bvQxsjxjtMablt", "846739", "999993914", "XRBS57", newDate(2023, 10, 10), newDate(2024, 10, 9)},
}

type DB struct {
	permits map[string][]*ParkingPermit
}

func NewDB() *DB {
	db := &DB{
		permits: make(map[string][]*ParkingPermit),
	}

	for _, p := range permits {
		db.permits[p.OwnerBSN] = append(db.permits[p.OwnerBSN], p)
	}

	return db
}

type ParkingPermit struct {
	ID                 string    `json:"id"`
	PermitNumber       string    `json:"permit_number"`
	OwnerBSN           string    `json:"owner_bsn"`
	RegistrationNumber string    `json:"registration_number"`
	ValidFrom          time.Time `json:"valid_from"`
	ValidTo            time.Time `json:"valid_to"`
}

func (db *DB) ListParkingPermits(bsn string) []*ParkingPermit {
	return db.permits[bsn]
}

func (db *DB) GetParkingPermit(bsn, id string) *ParkingPermit {
	for _, p := range db.permits[bsn] {
		if p.ID == id {
			return p
		}
	}

	return nil
}

func newDate(year int, month time.Month, day int) time.Time {
	return time.Date(year, month, day, 0, 0, 0, 0, time.Local)
}
