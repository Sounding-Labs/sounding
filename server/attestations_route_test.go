package server

import (
	"encoding/json"
	"mime"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestAttestationRoutes(t *testing.T) {
	tests := []struct {
		name, method, path string
		wantStatus         int
		wantCode           string
	}{
		{"list", http.MethodGet, "/api/attestations/NGNC", http.StatusOK, ""},
		{"latest", http.MethodGet, "/api/attestations/NGNC/latest", http.StatusNotFound, ""},
		{"missing corridor", http.MethodGet, "/api/attestations/", http.StatusBadRequest, ""},
		{"list rejects POST", http.MethodPost, "/api/attestations/NGNC", http.StatusMethodNotAllowed, codeMethodNotAllowed},
		{"latest rejects POST", http.MethodPost, "/api/attestations/NGNC/latest", http.StatusMethodNotAllowed, codeMethodNotAllowed},
		{"list rejects PUT", http.MethodPut, "/api/attestations/NGNC", http.StatusMethodNotAllowed, codeMethodNotAllowed},
	}
	handler := (&Server{}).Handler()
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			rec := httptest.NewRecorder()
			req := httptest.NewRequest(tt.method, tt.path, nil)
			handler.ServeHTTP(rec, req)
			if rec.Code != tt.wantStatus {
				t.Fatalf("status = %d, want %d: %s", rec.Code, tt.wantStatus, rec.Body.String())
			}
			contentType := rec.Header().Get("Content-Type")
			mediaType, _, err := mime.ParseMediaType(contentType)
			if err != nil || mediaType != "application/json" {
				t.Errorf("Content-Type = %q, want application/json (err: %v)", contentType, err)
			}
			var body map[string]any
			if err := json.Unmarshal(rec.Body.Bytes(), &body); err != nil {
				t.Fatalf("response is not JSON: %v", err)
			}
			if rec.Code != http.StatusOK && body["error"] == nil {
				t.Errorf("missing error response: %v", body)
			}
			if tt.wantCode != "" {
				if got := body["code"]; got != tt.wantCode {
					t.Errorf("error code = %v, want %q", got, tt.wantCode)
				}
				if got := rec.Header().Get("Allow"); got != http.MethodGet {
					t.Errorf("Allow header = %q, want GET", got)
				}
			}
		})
	}
}
