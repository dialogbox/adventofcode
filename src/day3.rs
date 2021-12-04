use super::input_lines;

/*
 * This code assums the input text file is sorted before hand.
 * I could do that in the code but I just ran `sort` shell command.
 */

#[allow(dead_code)]
pub fn read_report(filename: &str) -> std::io::Result<Vec<String>> {
    let lines = input_lines(filename)?;
    Ok(lines.map(|l| l.unwrap()).collect())
}

#[allow(dead_code)]
pub fn compute_power_consumption(report: &Vec<String>) -> (i32, i32) {
    let mut gamma_str: String = "0".into();
    let mut epsilon_str: String = "0".into();

    for i in 0..report[0].len() {
        if most_common_bit(report, i) {
            gamma_str.push('1');
            epsilon_str.push('0');
        } else {
            gamma_str.push('0');
            epsilon_str.push('1');
        }
    }

    (
        i32::from_str_radix(&gamma_str, 2).unwrap(),
        i32::from_str_radix(&epsilon_str, 2).unwrap(),
    )
}

fn most_common_bit(report: &Vec<String>, bit_idx: usize) -> bool {
    let mut count = 0;

    for l in report {
        if l.chars().nth(bit_idx) == Some('0') {
            count += 1;
        }
    }

    if count >= report.len() - count {
        false
    } else {
        true
    }
}

pub fn partition_by_bit_value<'a>(
    report: &'a [String],
    bit_idx: usize,
) -> (&'a [String], &'a [String]) {
    let idx = report.partition_point(|l| l.chars().nth(bit_idx) == Some('0'));

    (&report[0..idx], &report[idx..])
}

#[allow(dead_code)]
pub fn compute_oxygen_generator_rating(report: &Vec<String>) -> i32 {
    let mut cur: &[String] = report;

    for i in 0..report[0].len() {
        let next = partition_by_bit_value(cur, i);

        if next.0.len() > next.1.len() {
            cur = next.0;
        } else {
            cur = next.1;
        }

        if cur.len() <= 1 {
            break;
        }
    }

    if cur.len() != 1 {
        panic!("Something wrong {:?}", cur);
    }

    i32::from_str_radix(&cur[0], 2).unwrap()
}

#[allow(dead_code)]
pub fn compute_co2_scrubber_rating(report: &Vec<String>) -> i32 {
    let mut cur: &[String] = report;

    for i in 0..report[0].len() {
        let next = partition_by_bit_value(cur, i);

        if next.0.len() <= next.1.len() {
            cur = next.0;
        } else {
            cur = next.1;
        }

        if cur.len() <= 1 {
            break;
        }
    }

    if cur.len() != 1 {
        panic!("Something wrong {:?}", cur);
    }

    i32::from_str_radix(&cur[0], 2).unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_report() {
        let report = read_report("inputs/day3.txt").unwrap();
        for line in report {
            println!("{:?}", line);
        }
    }

    #[test]
    fn test_compute_power_consumption() {
        let report = read_report("inputs/day3.txt").unwrap();
        let (gamma, epsilon) = compute_power_consumption(&report);

        println!(
            "Gamma: {} * Epsilon: {} = {}",
            gamma,
            epsilon,
            gamma * epsilon
        );
    }

    #[test]
    fn test_life_support_rating() {
        let report = read_report("inputs/day3.txt").unwrap();

        let oxygen_generator_rating = compute_oxygen_generator_rating(&report);
        let co2_scrubber_rating = compute_co2_scrubber_rating(&report);

        println!(
            "Oxygen Generator Rating: {} * CO2 Scrubber Rating: {} = {}",
            oxygen_generator_rating,
            co2_scrubber_rating,
            oxygen_generator_rating * co2_scrubber_rating
        );
    }
}
