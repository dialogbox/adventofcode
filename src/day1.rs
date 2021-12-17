use super::input_lines;
use std::collections::VecDeque;

#[allow(dead_code)]
pub fn part1(filename: &str) -> std::io::Result<i32> {
    let lines = input_lines(filename)?;

    let mut cur: u16 = u16::MAX;
    let mut result = 0;

    lines.for_each(|line| {
        if let Ok(measurement) = line {
            let m = measurement.parse::<u16>().unwrap();
            if m > cur {
                result += 1;
            }
            cur = m;
        }
    });

    Ok(result)
}

#[allow(dead_code)]
pub fn part2(filename: &str) -> std::io::Result<i32> {
    let mut lines = input_lines(filename)?;

    let mut window: VecDeque<u16> = VecDeque::with_capacity(3);
    let mut cur: u16 = 0;
    let mut result = 0;

    // The first window
    for line in lines.by_ref().take(3) {
        let m = line.unwrap().parse::<u16>().unwrap();
        window.push_back(m);
        cur += m;
    }

    // let lines = lines.skip(1);

    lines.for_each(|line| {
        if let Ok(measurement) = line {
            print!("{:?}({})", window, cur);
            let m = measurement.parse::<u16>().unwrap();

            let m_prev = window.pop_front().unwrap();
            window.push_back(m);

            let t = cur - m_prev + m;

            print!(" vs {:?}{}", window, t);

            if t > cur {
                print!(" => INCREASED");
                result += 1;
            }
            println!();
            cur = t;
        }
    });

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        println!("{}", part1("inputs/day1.txt").unwrap());
    }
    #[test]
    fn test_part2() {
        println!("{}", part2("inputs/day1.txt").unwrap());
    }
}
