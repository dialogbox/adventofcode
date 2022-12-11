package aoc2021

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func ReadLines(filename string) ([]string, error) {
	file, err := os.Open(fmt.Sprintf("../inputs/%v", filename))
	if err != nil {
		return nil, err
	}
	defer file.Close()

	result := make([]string, 0)
	scanner := bufio.NewScanner(file)
	// optionally, resize scanner's capacity for lines over 64K, see next example
	for scanner.Scan() {
		result = append(result, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return result, nil
}

func ReadCSVLines(filename string) ([][]string, error) {
	file, err := os.Open(fmt.Sprintf("../inputs/%v", filename))
	if err != nil {
		return nil, err
	}
	defer file.Close()

	r := csv.NewReader(file)
	records, err := r.ReadAll()
	if err != nil {
		return nil, err
	}

	return records, nil
}

func ReadNumbers(filename string) ([]int, error) {
	records, err := ReadCSVLines(filename)
	if err != nil {
		return nil, err
	}

	if len(records) != 1 {
		return nil, fmt.Errorf("malformed input: only one line of numbers is allowed")
	}

	result := make([]int, 0)
	for _, nstr := range records[0] {
		n, err := strconv.Atoi(nstr)
		if err != nil {
			return nil, err
		}
		result = append(result, n)

	}

	return result, nil
}

func ReadNumberLines(filename string) ([]int, error) {
	lines, err := ReadLines(filename)
	if err != nil {
		return nil, err
	}

	result := make([]int, 0)
	for _, l := range lines {
		n, err := strconv.Atoi(l)
		if err != nil {
			return nil, err
		}
		result = append(result, n)

	}

	return result, nil
}
