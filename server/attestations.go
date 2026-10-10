package server

import (
	"encoding/json"
	"net/http"
	"strings"
)

// AttestationResponse represents a corridor attestation from Soroban
type AttestationResponse struct {
	CorridorID   string `json:"corridor_id"`
	Integrity    string `json:"integrity"`
	BestVerdict  string `json:"best_verdict"`
	LossPct      string `json:"loss_pct"`
	ReferenceMid string `json:"reference_mid"`
	MeasuredAt   string `json:"measured_at"`
	Attestor     string `json:"attestor"`
	TxHash       string `json:"tx_hash"`
	ContractID   string `json:"contract_id,omitempty"`
}

// AttestationsListResponse represents multiple attestations
type AttestationsListResponse struct {
	Attestations []AttestationResponse `json:"attestations"`
	Count        int                   `json:"count"`
	ContractID   string                `json:"contract_id,omitempty"`
}

// handleAttestations serves GET /api/attestations/:corridor
//
// Returns on-chain attestations for a corridor from the Soroban contract.
//
// Query parameters:
//   - limit: max number of attestations to return (default: 10, max: 100)
//
// Response:
//
//	{
//	  "attestations": [
//	    {
//	      "corridor_id": "USDC→NGNC",
//	      "integrity": "DIRECT",
//	      "best_verdict": "POOR",
//	      "loss_pct": "25.02",
//	      "reference_mid": "1364.50",
//	      "measured_at": "2024-01-01T00:00:00Z",
//	      "attestor": "GAB...",
//	      "tx_hash": "abc123...",
//	      "contract_id": "C..."
//	    }
//	  ],
//	  "count": 1,
//	  "contract_id": "C..."
//	}
//
// Note: This endpoint requires Soroban contract deployment and RPC integration.
// Currently returns empty array as placeholder.
func handleAttestations(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	// Extract corridor ID from path /api/attestations/:corridor
	path := strings.TrimPrefix(r.URL.Path, "/api/attestations/")
	corridorID := strings.TrimSpace(path)

	if corridorID == "" {
		writeError(w, r, http.StatusBadRequest, codeInvalidQuery, "corridor_id is required")
		return
	}

	// TODO: Query Soroban contract for attestations
	// For now, return empty array to signal feature is ready but not yet deployed

	response := AttestationsListResponse{
		Attestations: []AttestationResponse{},
		Count:        0,
		ContractID:   "", // Will be populated after contract deployment
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

// handleAttestationLatest serves GET /api/attestations/:corridor/latest
//
// Returns the latest on-chain attestation for a corridor.
//
// Response:
//
//	{
//	  "corridor_id": "USDC→NGNC",
//	  "integrity": "DIRECT",
//	  "best_verdict": "POOR",
//	  "loss_pct": "25.02",
//	  "reference_mid": "1364.50",
//	  "measured_at": "2024-01-01T00:00:00Z",
//	  "attestor": "GAB...",
//	  "tx_hash": "abc123...",
//	  "contract_id": "C..."
//	}
//
// Returns 404 if no attestations exist for the corridor.
func handleAttestationLatest(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	// Extract corridor ID from path /api/attestations/:corridor/latest
	path := strings.TrimPrefix(r.URL.Path, "/api/attestations/")
	path = strings.TrimSuffix(path, "/latest")
	corridorID := strings.TrimSpace(path)

	if corridorID == "" {
		writeError(w, r, http.StatusBadRequest, codeInvalidQuery, "corridor_id is required")
		return
	}

	// TODO: Query Soroban contract for latest attestation
	// For now, return 404 to signal no attestations yet

	writeError(w, r, http.StatusNotFound, codeAttestationsNotDeployed,
		"No attestations found for this corridor. Contract deployment pending.")
}
