package utils

import (
	"errors"
	"regexp"
)

var (
	// ErrInvalidFormat is returned when phone number format is invalid
	ErrInvalidFormat = errors.New("invalid phone number format")
	
	// ErrEmptyNumber is returned when phone number is empty
	ErrEmptyNumber = errors.New("phone number cannot be empty")
)

// PhoneValidator handles phone number validation
type PhoneValidator struct {
	pattern *regexp.Regexp
}

// NewPhoneValidator creates a new phone validator instance
func NewPhoneValidator() *PhoneValidator {
	// Pattern matches international phone numbers with optional + prefix
	pattern := regexp.MustCompile(`^\+?[1-9]\d{1,14}$`)
	
	return &PhoneValidator{
		pattern: pattern,
	}
}

// Validate checks if a phone number is valid according to E.164 format
func (v *PhoneValidator) Validate(phone string) error {
	if phone == "" {
		return ErrEmptyNumber
	}
	
	// Remove formatting before validation
	cleanPhone := FormatPhoneNumber(phone)
	
	if !v.pattern.MatchString(cleanPhone) {
		return ErrInvalidFormat
	}
	
	return nil
}

// IsValid returns true if the phone number is valid
func (v *PhoneValidator) IsValid(phone string) bool {
	return v.Validate(phone) == nil
}
