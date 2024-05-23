package server

var registrations = []*Registration{
	{"H358BH", "999995042"},
	{"9ZTJ69", "999995042"},
	{"ZV975T", "999995042"},
	{"ZV326K", "999993161"},
	{"XRBS57", "999993914"},
	{"ZV919R", "999993914"},
}

type DB struct {
	registrations map[string]*Registration
}

func NewDB() *DB {
	db := &DB{
		registrations: make(map[string]*Registration, len(registrations)),
	}

	for _, r := range registrations {
		db.registrations[r.RegistrationNumber] = r
	}

	return db
}

type Registration struct {
	RegistrationNumber string `json:"registration_number"`
	BSN                string `json:"bsn"`
}

func (db *DB) GetRegistration(registrationNumber string) *Registration {
	return db.registrations[registrationNumber]
}
