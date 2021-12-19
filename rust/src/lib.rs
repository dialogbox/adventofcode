mod day1;
mod day10;
mod day11;
mod day12;
mod day13;
mod day14;
mod day15;
mod day16;
mod day17;
mod day18;
mod day2;
mod day3;
mod day4;
mod day5;
mod day6;
mod day7;
mod day8;
mod day9;

use std::fs::File;
use std::io::{self, BufRead};

pub fn input_lines(filename: &str) -> io::Result<io::Lines<io::BufReader<File>>> {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

pub fn read_table_input(filename: &str) -> std::io::Result<Vec<Vec<char>>> {
    let lines = input_lines(filename)?;

    let mut result = Vec::new();

    for l in lines {
        result.push(l?.chars().collect::<Vec<char>>());
    }

    Ok(result)
}

pub fn read_u8_table_input(filename: &str) -> std::io::Result<Vec<Vec<u8>>> {
    let table = read_table_input(filename)?;
    let result = table
        .iter()
        .map(|l| {
            l.iter()
                .map(|c| c.to_digit(10).unwrap() as u8)
                .collect::<Vec<u8>>()
        })
        .collect();

    Ok(result)
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        let result = 2 + 2;
        assert_eq!(result, 4);
    }
}
