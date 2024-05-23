FROM golang:1.22.3-alpine AS build

WORKDIR /app

RUN apk add --no-cache git

COPY go.mod go.sum .
RUN go mod download -x

COPY server server
COPY main.go .

RUN go install -ldflags "-s -w" -v .


FROM alpine:3.20.0

COPY --from=build /go/bin/ /usr/local/bin

ENTRYPOINT ["/usr/local/bin/lamina"]
