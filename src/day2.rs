use super::input_lines;

mod part1 {
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
    pub struct command {
        direction: Direction,
        distance: i32,
    }

    pub fn read_plan(filename: &str) -> std::io::Result<Vec<command>> {
        let lines = super::input_lines(filename)?;

        let mut result: Vec<command> = Vec::new();

        for line in lines {
            let line = line.unwrap();

            let t: Vec<&str> = line.split(' ').collect();
            result.push(command {
                direction: FromStr::from_str(t[0]).unwrap(),
                distance: t[1].parse::<i32>().unwrap(),
            });
        }

        Ok(result)
    }

    pub fn do_plan(plan: &Vec<command>, starting_position: (i32, i32)) -> (i32, i32) {
        let (mut x, mut y) = starting_position;

        for command in plan {
            match command.direction {
                Direction::Forward => x = x + command.distance,
                Direction::Up => y = y - command.distance,
                Direction::Down => y = y + command.distance,
            }
        }

        (x, y)
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn test_read_plan() {
            let plan = read_plan("inputs/day2.txt").unwrap();
            println!("{:?}", plan);
        }

        #[test]
        fn test_do_plan() {
            let plan = read_plan("inputs/day2.txt").unwrap();
            let result = do_plan(&plan, (0, 0));

            println!("{:?}", result);
            println!("{}", result.0 * result.1);
        }
    }
}

mod part2 {}
