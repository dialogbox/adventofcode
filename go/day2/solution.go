package day2

import (
	"aoc2021"
	"strconv"
	"strings"
)

type Direction int8

const (
	Forward Direction = iota
	Down
	Up
)

type Move struct {
	direction Direction
	distance  int
}

func Input() ([]Move, error) {
	lines, err := aoc2021.ReadLines("day2.txt")
	if err != nil {
		return nil, err
	}

	moves := make([]Move, 0)
	for _, line := range lines {
		elem := strings.Split(line, " ")
		var direction Direction

		switch elem[0] {
		case "forward":
			direction = Forward
		case "up":
			direction = Up
		case "down":
			direction = Down
		}

		distance, err := strconv.Atoi(elem[1])
		if err != nil {
			return nil, err
		}

		moves = append(moves, Move{direction, distance})
	}

	return moves, nil
}

func Part1(input []Move) int {
	h, v := 0, 0

	for _, m := range input {
		if m.direction == Forward {
			h += m.distance
		} else if m.direction == Up {
			v -= m.distance
		} else {
			v += m.distance
		}
	}

	return h * v
}

func Part2(input []Move) int {
	aim, h, v := 0, 0, 0

	for _, m := range input {
		if m.direction == Forward {
			h += m.distance
			v += aim * m.distance
		} else if m.direction == Up {
			aim -= m.distance
		} else {
			aim += m.distance
		}
	}

	return h * v

}
