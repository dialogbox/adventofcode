package day2

import "testing"

func TestInput(t *testing.T) {
	moves, err := Input()
	if err != nil {
		t.Fatal(err)
	}

	if moves[0].direction != Forward || moves[0].distance != 7 {
		t.Fail()
	}
}

func TestPart1(t *testing.T) {
	moves, err := Input()
	if err != nil {
		t.Fatal(err)
	}

	result := Part1(moves)

	t.Log(result)
}

func TestPart2(t *testing.T) {
	moves, err := Input()
	if err != nil {
		t.Fatal(err)
	}

	result := Part2(moves)

	t.Log(result)
}
