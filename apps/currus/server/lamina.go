package server

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"time"

	logboek_http "github.com/MinBZK/logboek-dataverwerkingen-logboek/libs/logboek-go/http"
)

func NewLaminaClient(baseURL string) *LaminaClient {
	u, _ := url.Parse(baseURL)

	return &LaminaClient{
		baseURL: u,
		httpClient: http.Client{
			Transport: logboek_http.NewTransport(http.DefaultTransport),
			Timeout:   time.Second * 3,
		},
	}
}

type LaminaClient struct {
	baseURL    *url.URL
	httpClient http.Client
}

type LaminaRegistration struct {
	RegistrationNumber string `json:"registration_number"`
	BSN                string `json:"bsn"`
}

func (c *LaminaClient) GetRegistration(ctx context.Context, registrationNumber string) (*LaminaRegistration, error) {
	resp, err := c.get(ctx, "registrations", registrationNumber)
	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("not ok")
	}

	reg := LaminaRegistration{}
	if err := json.NewDecoder(resp.Body).Decode(&reg); err != nil {
		return nil, err
	}

	return &reg, nil
}

func (c *LaminaClient) get(ctx context.Context, path ...string) (*http.Response, error) {
	u := c.baseURL.JoinPath(path...).String()
	req, err := http.NewRequestWithContext(ctx, "GET", u, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("User-Agent", "Currus/1.0")

	return c.httpClient.Do(req)
}
