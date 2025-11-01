package utils

import (
	"testing"
)

func TestFormatPhoneNumber(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "phone with dashes",
			input:    "555-123-4567",
			expected: "5551234567",
		},
		{
			name:     "phone with spaces",
			input:    "555 123 4567",
			expected: "5551234567",
		},
		{
			name:     "phone with parentheses",
			input:    "(555) 123-4567",
			expected: "5551234567",
		},
		{
			name:     "phone with dots",
			input:    "555.123.4567",
			expected: "5551234567",
		},
		{
			name:     "clean phone number",
			input:    "5551234567",
			expected: "5551234567",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := FormatPhoneNumber(tt.input)
			if result != tt.expected {
				t.Errorf("FormatPhoneNumber(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestValidatePhonePrefix(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected bool
	}{
		{
			name:     "valid with plus",
			input:    "+15551234567",
			expected: true,
		},
		{
			name:     "valid with digit",
			input:    "15551234567",
			expected: true,
		},
		{
			name:     "invalid empty",
			input:    "",
			expected: false,
		},
		{
			name:     "invalid with letter",
			input:    "abc123",
			expected: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := ValidatePhonePrefix(tt.input)
			if result != tt.expected {
				t.Errorf("ValidatePhonePrefix(%q) = %v, want %v", tt.input, result, tt.expected)
			}
		})
	}
}
