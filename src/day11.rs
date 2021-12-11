use super::input_lines;

#[allow(dead_code)]
fn read_input(filename: &str) -> std::io::Result<[[u8; 10]; 10]> {
    let lines = input_lines(filename)?;

    let mut result = [[0; 10]; 10];

    for (i, l) in lines.enumerate() {
        for (j, c) in l?.chars().into_iter().enumerate() {
            result[i][j] = c.to_digit(10).unwrap() as u8;
        }
    }

    Ok(result)
}

#[allow(dead_code)]
fn step(input: &mut [[u8; 10]; 10]) -> i32 {
    let mut c = [[0 as u8; 12]; 12];

    let mut result: i32 = 0;
    for i in 0..10 {
        for j in 0..10 {
            c[i + 1][j + 1] = input[i][j] + 1;
        }
    }

    let mut already_flash = [[false; 12]; 12];
    loop {
        let mut new_flash = [[false; 12]; 12];
        for i in 1..=10 {
            for j in 1..=10 {
                if c[i][j] > 9 && !already_flash[i][j] {
                    c[i][j] = 0;
                    new_flash[i][j] = true;
                    already_flash[i][j] = true;
                    result += 1;
                }
            }
        }

        // break if there is no new flash
        if !new_flash.iter().any(|l| l.iter().any(|i| *i)) {
            break;
        }

        for i in 1..=10 {
            for j in 1..=10 {
                if already_flash[i][j] {
                    continue;
                }

                let mut n_flash = 0;
                // upper left
                if new_flash[i - 1][j - 1] {
                    n_flash += 1;
                }
                // upper
                if new_flash[i - 1][j] {
                    n_flash += 1;
                }
                // upper right
                if new_flash[i - 1][j + 1] {
                    n_flash += 1;
                }
                // left
                if new_flash[i][j - 1] {
                    n_flash += 1;
                }
                // right
                if new_flash[i][j + 1] {
                    n_flash += 1;
                }
                // lower left
                if new_flash[i + 1][j - 1] {
                    n_flash += 1;
                }
                // lower
                if new_flash[i + 1][j] {
                    n_flash += 1;
                }
                // lower right
                if new_flash[i + 1][j + 1] {
                    n_flash += 1;
                }

                c[i][j] += n_flash;
            }
        }
    }

    for i in 0..10 {
        for j in 0..10 {
            input[i][j] = c[i + 1][j + 1];
        }
    }

    result
}

#[allow(dead_code)]
fn print_status(input: &[[u8; 10]; 10]) {
    for i in 0..input.len() {
        for j in 0..input[0].len() {
            print!("{}", input[i][j]);
        }
        println!("");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_some() {
        println!("{:?}", (0..10).zip(0..5).collect::<Vec<_>>());
    }

    #[test]
    fn test_read_input() {
        let input = read_input("inputs/day11_test.txt").unwrap();

        print_status(&input);
    }

    #[test]
    fn test_part1() {
        let mut input = read_input("inputs/day11_test.txt").unwrap();

        let mut result = 0;
        for _ in 0..100 {
            result += step(&mut input);
        }

        assert_eq!(result, 1656);
    }

    #[test]
    fn do_part1() {
        let mut input = read_input("inputs/day11.txt").unwrap();

        let mut result = 0;
        for _ in 0..100 {
            result += step(&mut input);
        }

        assert_eq!(result, 1571);
    }

    #[test]
    fn test_part2() {
        let mut input = read_input("inputs/day11_test.txt").unwrap();

        let mut result = None;
        for i in 0..1000 {
            let flash = step(&mut input);

            if flash == 100 {
                result = Some(i + 1);
                break;
            }
        }

        assert_eq!(result, Some(195));
    }

    #[test]
    fn do_part2() {
        let mut input = read_input("inputs/day11.txt").unwrap();

        let mut result = None;
        for i in 0..1000 {
            let flash = step(&mut input);

            if flash == 100 {
                result = Some(i + 1);
                break;
            }
        }

        assert_eq!(result, Some(387));
    }
}
