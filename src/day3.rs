use super::input_lines;

#[allow(dead_code)]
pub fn read_report(filename: &str) -> std::io::Result<Vec<Vec<bool>>> {
    let lines = input_lines(filename)?;

    let mut result: Vec<Vec<bool>> = Vec::new();

    for line in lines {
        let line = line.unwrap();

        let mut line_bits: Vec<bool> = Vec::with_capacity(12);

        for bit in line.chars() {
            if bit == '1' {
                line_bits.push(true);
            } else {
                line_bits.push(false);
            }
        }

        result.push(line_bits);
    }

    Ok(result)
}

#[allow(dead_code)]
pub fn compute_power_consumption(report: &Vec<Vec<bool>>) -> (i32, i32) {
    let mut result: Vec<usize> = vec![0; report[0].len()];

    for l in report {
        for (i, bit) in l.iter().enumerate() {
            if *bit {
                result[i] = result[i] + 1;
            }
        }
    }

    let num_lines = report.len();

    let mut gamma_str: String = "0".into();
    let mut epsilon_str: String = "0".into();

    for num_of_true in result {
        if num_of_true > num_lines - num_of_true {
            gamma_str.push('1');
            epsilon_str.push('0');
        } else if num_of_true == num_lines - num_of_true {
            gamma_str.push('=');
            epsilon_str.push('=');
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
}
