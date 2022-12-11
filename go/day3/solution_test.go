package day3

import (
	"testing"
)

func TestInput(t *testing.T) {
	numbers, err := Input()
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("%v", Part1(numbers))
}

func TestPart1(t *testing.T) {
	numbers, err := Input()
	if err != nil {
		t.Fatal(err)
	}

	result := Part1(numbers)
	t.Log(result)
}

func TestPart2(t *testing.T) {
	numbers, err := Input()
	if err != nil {
		t.Fatal(err)
	}

	result := Part2(numbers)
	t.Log(result)
}
