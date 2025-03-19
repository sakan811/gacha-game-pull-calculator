package errors

import (
	"fmt"
)

type ErrorCode int

const (
	ErrInvalidInput ErrorCode = iota + 1
	ErrInvalidBannerType
	ErrInvalidPity
	ErrInvalidPulls
	ErrCalculation
)

type Error struct {
	Err     error
	Message string
	Code    ErrorCode
}

func (e *Error) Error() string {
	if e.Err != nil {
		return fmt.Sprintf("%s: %v", e.Message, e.Err)
	}

	return e.Message
}

func (e *Error) Unwrap() error {
	return e.Err
}

func NewInvalidInputError(message string) *Error {
	return &Error{
		Code:    ErrInvalidInput,
		Message: message,
	}
}

func NewInvalidBannerTypeError(message string) *Error {
	return &Error{
		Code:    ErrInvalidBannerType,
		Message: message,
	}
}

func NewInvalidPityError(message string) *Error {
	return &Error{
		Code:    ErrInvalidPity,
		Message: message,
	}
}

func NewInvalidPullsError(message string) *Error {
	return &Error{
		Code:    ErrInvalidPulls,
		Message: message,
	}
}

func NewCalculationError(message string, err error) *Error {
	return &Error{
		Code:    ErrCalculation,
		Message: message,
		Err:     err,
	}
}

func NewBadRequestError(message string, err error) *Error {
	return &Error{
		Code:    ErrInvalidInput,
		Message: message,
		Err:     err,
	}
}

func NewInternalServerError(message string, err error) *Error {
	return &Error{
		Code:    ErrCalculation,
		Message: message,
		Err:     err,
	}
}

func NewNotFoundError(message string, err error) *Error {
	return &Error{
		Code:    ErrInvalidInput,
		Message: message,
		Err:     err,
	}
}
