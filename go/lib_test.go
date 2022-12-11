package aoc2021

import (
	"testing"
)

func TestInput(t *testing.T) {
	numbers, err := ReadNumberLines("day1.txt")
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("%v", numbers)
}
