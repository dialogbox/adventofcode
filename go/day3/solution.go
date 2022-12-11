package day3

import (
	"aoc2021"
)

func Input() ([]int, error) {
	numbers, err := aoc2021.ReadNumberLines("day3.txt")
	if err != nil {
		return nil, err
	}

	return numbers, nil
}

func Part1(input []int) int {
	result := 0
	for i, n := range input[1:] {
		if n > input[i] {
			result++
		}
	}

	return result
}

func Part2(input []int) int {
	result := 0
	prev := (input[0] + input[1] + input[2])
	for i := range input[:len(input)-3] {
		cur := (input[i+1] + input[i+2] + input[i+3])
		if prev < cur {
			result++
		}
		prev = cur
	}

	return result
}
