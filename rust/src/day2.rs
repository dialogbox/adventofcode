use super::read_raw_lines;
use std::str::FromStr;

#[derive(Debug)]
pub enum Direction {
    Forward,
    Up,
    Down,
}

impl FromStr for Direction {
    type Err = ();

    fn from_str(input: &str) -> Result<Direction, Self::Err> {
        match input {
            "forward" => Ok(Direction::Forward),
            "up" => Ok(Direction::Up),
            "down" => Ok(Direction::Down),
            _ => Err(()),
        }
    }
}

#[derive(Debug)]
pub struct Command {
    direction: Direction,
    distance: i32,
}

#[allow(dead_code)]
pub fn read_plan(filename: &str) -> std::io::Result<Vec<Command>> {
    let lines = read_raw_lines(filename)?;

    let mut result: Vec<Command> = Vec::new();

    for line in lines {
        let line = line.unwrap();

        let t: Vec<&str> = line.split(' ').collect();
        result.push(Command {
            direction: FromStr::from_str(t[0]).unwrap(),
            distance: t[1].parse::<i32>().unwrap(),
        });
    }

    Ok(result)
}

#[allow(dead_code)]
pub fn do_plan(plan: &[Command], starting_position: (i32, i32)) -> (i32, i32) {
    let (mut h, mut d) = starting_position;

    for command in plan {
        match command.direction {
            Direction::Forward => h += command.distance,
            Direction::Up => d -= command.distance,
            Direction::Down => d += command.distance,
        }
    }

    (h, d)
}

#[allow(dead_code)]
pub fn do_new_plan(plan: &[Command], starting_position: (i32, i32, i32)) -> (i32, i32, i32) {
    let (mut h, mut d, mut aim) = starting_position;

    for command in plan {
        match command.direction {
            Direction::Forward => {
                h += command.distance;
                d += aim * command.distance;
            }
            Direction::Up => aim -= command.distance,
            Direction::Down => aim += command.distance,
        }
    }

    (h, d, aim)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_plan() {
        let plan = read_plan("../inputs/day2.txt").unwrap();
        println!("{:?}", plan);
    }

    #[test]
    fn test_do_plan() {
        let plan = read_plan("../inputs/day2.txt").unwrap();
        let result = do_plan(&plan, (0, 0));

        println!("{:?}", result);
        println!("{}", result.0 * result.1);
    }

    #[test]
    fn test_do_new_plan() {
        let plan = read_plan("../inputs/day2.txt").unwrap();
        let result = do_new_plan(&plan, (0, 0, 0));

        println!("{:?}", result);
        println!("{}", result.0 * result.1);
    }
}
