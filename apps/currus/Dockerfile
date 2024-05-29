FROM golang:1.22.3-alpine AS build

ARG BUILD_COMMIT="unknown"

WORKDIR /app

RUN apk add --no-cache git

COPY go.mod go.sum .
RUN go mod download -x

COPY server server
COPY main.go .

RUN go install -ldflags "-s -w -X github.com/MinBZK/logboek-dataverwerkingen-demo/apps/currus/server.commit=${BUILD_COMMIT}" -v .


FROM alpine:3.20.0

COPY --from=build /go/bin/ /usr/local/bin

ENTRYPOINT ["/usr/local/bin/currus"]
