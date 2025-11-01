package utils

import (
	"fmt"
	"strings"
)

// FormatPhoneNumber formats a phone number string by removing common separators
func FormatPhoneNumber(phone string) string {
	// Remove common separators
	phone = strings.ReplaceAll(phone, "-", "")
	phone = strings.ReplaceAll(phone, " ", "")
	phone = strings.ReplaceAll(phone, "(", "")
	phone = strings.ReplaceAll(phone, ")", "")
	phone = strings.ReplaceAll(phone, ".", "")
	
	return phone
}

// ValidatePhonePrefix checks if a phone number starts with a valid prefix
func ValidatePhonePrefix(phone string) bool {
	if len(phone) == 0 {
		return false
	}
	
	// Check if starts with + or a digit
	firstChar := phone[0]
	return firstChar == '+' || (firstChar >= '0' && firstChar <= '9')
}

// PrintPhoneInfo prints formatted phone information
func PrintPhoneInfo(country, carrier, lineType string) {
	fmt.Println("Phone Information:")
	fmt.Printf("  Country: %s\n", country)
	fmt.Printf("  Carrier: %s\n", carrier)
	fmt.Printf("  Line Type: %s\n", lineType)
}
