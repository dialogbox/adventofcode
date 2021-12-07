use super::input_lines;

#[allow(dead_code)]
fn read_input(filename: &str) -> std::io::Result<Vec<i32>> {
    let line = input_lines(filename)?.next().unwrap()?;

    let mut nums = line
        .split_terminator(",")
        .map(|n| n.parse::<i32>().unwrap())
        .collect::<Vec<i32>>();

    nums.sort();

    Ok(nums)
}

#[allow(dead_code)]
fn part1(nums: &Vec<i32>) -> (i32, i32) {
    let l = nums.len();

    let median = if l % 2 == 0 {
        (nums[l / 2 - 1] + nums[l / 2]) / 2
    } else {
        nums[l / 2]
    };

    let mut result = 0;
    for n in nums {
        result += (n - median).abs();
    }

    (median, result)
}

#[allow(dead_code)]
fn cal_fuels_part2(nums: &Vec<i32>, pos: i32) -> i32 {
    let mut result = 0;
    for n in nums {
        let dist = (n - pos).abs();
        result += if dist % 2 == 0 {
            (1 + dist) * (dist / 2)
        } else {
            (1 + dist) * (dist / 2) + (dist / 2 + 1)
        }
    }

    result
}

#[allow(dead_code)]
fn part2(nums: &Vec<i32>) -> (i32, i32) {
    // Starts from mean
    let pos = nums.iter().sum::<i32>() / nums.len() as i32;

    // Using GCD
    let mut prev_f = cal_fuels_part2(nums, pos);
    let f2 = cal_fuels_part2(nums, pos + 1);

    // going forward
    if prev_f > f2 {
        for i in pos..=*nums.last().unwrap() {
            let f = cal_fuels_part2(nums, i);
            if prev_f < f {
                return (i - 1, prev_f);
            }
            prev_f = f;
        }
    // going backward
    } else {
        for i in (nums[0]..=pos).rev() {
            let f = cal_fuels_part2(nums, i);
            if prev_f < f {
                return (i + 1, prev_f);
            }
            prev_f = f;
        }
    }

    panic!("something wrong");
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
        let nums = read_input("inputs/day7_test.txt").unwrap();

        println!("{:?}", nums);
        println!("{}", nums.iter().sum::<i32>() / nums.len() as i32);
    }

    #[test]
    fn test_part1() {
        let nums = read_input("inputs/day7_test.txt").unwrap();

        let (pos, fuels) = part1(&nums);

        assert_eq!(pos, 2);
        assert_eq!(fuels, 37);
    }

    #[test]
    fn do_part1() {
        let nums = read_input("inputs/day7.txt").unwrap();

        let (pos, fuels) = part1(&nums);

        println!("To move {}, needs {} fuels", pos, fuels);
    }

    #[test]
    fn test_part2() {
        let nums = read_input("inputs/day7_test.txt").unwrap();

        let (pos, fuels) = part2(&nums);

        assert_eq!(pos, 5);
        assert_eq!(fuels, 168);
    }

    #[test]
    fn do_part2() {
        let nums = read_input("inputs/day7.txt").unwrap();

        let (pos, fuels) = part2(&nums);

        println!("To move {}, needs {} fuels", pos, fuels);
    }
}
