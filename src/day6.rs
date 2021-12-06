use super::input_lines;

#[allow(dead_code)]
fn read_input(filename: &str) -> std::io::Result<Vec<u64>> {
    let line = input_lines(filename)?.next().unwrap()?;

    let nums = line
        .split_terminator(",")
        .map(|n| n.parse::<u64>().unwrap())
        .collect::<Vec<_>>();

    Ok(nums)
}

#[allow(dead_code)]
fn compress_input(nums: &Vec<u64>) -> [u64; 9] {
    let mut result = [0; 9];
    for n in nums {
        result[*n as usize] += 1;
    }

    result
}

#[allow(dead_code)]
fn one_day(fishes: &mut [u64; 9]) {
    let t = fishes[0];

    fishes[0] = fishes[1];
    fishes[1] = fishes[2];
    fishes[2] = fishes[3];
    fishes[3] = fishes[4];
    fishes[4] = fishes[5];
    fishes[5] = fishes[6];
    fishes[6] = fishes[7] + t;
    fishes[7] = fishes[8];
    fishes[8] = t;
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
        let nums = read_input("inputs/day6_test.txt").unwrap();
        let fishs = compress_input(&nums);

        println!("{:?}", fishs);
    }

    #[test]
    fn test_play() {
        let nums = read_input("inputs/day6_test.txt").unwrap();
        let mut fishes = compress_input(&nums);

        println!("{:?}", fishes);
        for _ in 0..18 {
            one_day(&mut fishes);
            println!("{:?}", fishes);
        }
    }

    #[test]
    fn do_part1() {
        let nums = read_input("inputs/day6.txt").unwrap();
        let mut fishes = compress_input(&nums);

        println!("{:?}", fishes);
        for _ in 0..80 {
            one_day(&mut fishes);
        }
        println!("{:?}", fishes);
        println!("{}", fishes.iter().sum::<u64>());
    }

    #[test]
    fn do_part2() {
        let nums = read_input("inputs/day6.txt").unwrap();
        let mut fishes = compress_input(&nums);

        println!("{:?}", fishes);
        for _ in 0..256 {
            one_day(&mut fishes);
        }
        println!("{:?}", fishes);
        println!("{}", fishes.iter().sum::<u64>());
    }
}
