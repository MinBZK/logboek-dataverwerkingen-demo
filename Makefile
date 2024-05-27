.PHONY: start
start:
	docker compose up --detach --remove-orphans
	@echo ""
	@echo "Logboek dataverwerkingen demo is gestart."
	@echo "Ga naar http://localhost:8080 voor de "Mijn Gemeente"-applicatie"
	@echo "Inloggen kan met het account:"
	@echo "  Gebruikersnaam: burger"
	@echo "  Wachtwoord: demo123"
	@echo ""
	@echo "Bekijk de logboeken:"
	@echo "  http://localhost:3000"


.PHONY: stop
stop:
	docker compose stop

.PHONY: build
build:
	docker compose build

.PHONY: clean
clean:
	docker compose down --volumes --remove-orphans
