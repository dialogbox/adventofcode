use super::input_lines;

#[derive(Debug)]
struct Entry {
    unique_patterns: Vec<String>,
    output_values: Vec<String>,
}

#[allow(dead_code)]
fn string_minus(a: &String, b: &String) -> String {
    a.chars().filter(|e| !b.contains(*e)).collect::<String>()
}

#[allow(dead_code)]
fn string_intersect(a: &String, b: &String) -> String {
    a.chars().filter(|e| b.contains(*e)).collect::<String>()
}

impl Entry {
    #[allow(dead_code)]
    fn analyze(&self) -> [char; 7] {
        let pattern_1 = &self.unique_patterns[0];
        let pattern_4 = &self.unique_patterns[2];
        let pattern_7 = &self.unique_patterns[1];
        let pattern_8 = &self.unique_patterns[9];

        let a = string_minus(&pattern_7, &pattern_1);

        let bd = string_minus(&pattern_4, &pattern_1);

        let d_1 = string_minus(&bd, &self.unique_patterns[6]);
        let d_2 = string_minus(&bd, &self.unique_patterns[7]);
        let d_3 = string_minus(&bd, &self.unique_patterns[8]);

        let d = if d_1.len() == 1 {
            d_1
        } else if d_2.len() == 1 {
            d_2
        } else {
            d_3
        };

        let b = string_minus(&bd, &d);

        let c_1 = string_minus(&pattern_1, &self.unique_patterns[6]);
        let c_2 = string_minus(&pattern_1, &self.unique_patterns[7]);
        let c_3 = string_minus(&pattern_1, &self.unique_patterns[8]);

        let c = if c_1.len() == 1 {
            c_1
        } else if c_2.len() == 1 {
            c_2
        } else {
            c_3
        };

        let f = string_minus(&pattern_1, &c);

        let e_1 = string_minus(&pattern_8, &self.unique_patterns[6]);
        let e_2 = string_minus(&pattern_8, &self.unique_patterns[7]);
        let e_3 = string_minus(&pattern_8, &self.unique_patterns[8]);

        let e = if e_1 != c && e_1 != d {
            e_1
        } else if e_2 != c && e_2 != d {
            e_2
        } else {
            e_3
        };

        let g = string_minus(&pattern_8, &format!("{}{}{}{}{}{}", a, b, c, d, e, f));

        [a, b, c, d, e, f, g].map(|c| c.chars().nth(0).unwrap())
    }

    #[allow(dead_code)]
    fn compute_digit_pattern(&self) -> [String; 10] {
        let pat = self.analyze();

        [
            vec![pat[0], pat[1], pat[2], pat[4], pat[5], pat[6]],
            vec![pat[2], pat[5]],
            vec![pat[0], pat[2], pat[3], pat[4], pat[6]],
            vec![pat[0], pat[2], pat[3], pat[5], pat[6]],
            vec![pat[1], pat[2], pat[3], pat[5]],
            vec![pat[0], pat[1], pat[3], pat[5], pat[6]],
            vec![pat[0], pat[1], pat[3], pat[4], pat[5], pat[6]],
            vec![pat[0], pat[2], pat[5]],
            vec![pat[0], pat[1], pat[2], pat[3], pat[4], pat[5], pat[6]],
            vec![pat[0], pat[1], pat[2], pat[3], pat[5], pat[6]],
        ]
        .map(|mut p| {
            p.sort();
            p.iter().collect::<String>()
        })
    }

    #[allow(dead_code)]
    fn find_output_digit(pat: &[String; 10], output_value: &String) -> Option<u8> {
        let mut sorted_output_value = output_value.chars().collect::<Vec<char>>();
        sorted_output_value.sort();
        let sorted_output_value = sorted_output_value.iter().collect::<String>();

        for (i, p) in pat.iter().enumerate() {
            if p == &sorted_output_value {
                return Some(i as u8);
            }
        }

        None
    }

    #[allow(dead_code)]
    fn output_value(&self) -> Option<i32> {
        let pat = self.compute_digit_pattern();
        let mut result = 0;

        for i in &self.output_values {
            if let Some(v) = Self::find_output_digit(&pat, &i) {
                result *= 10;
                result += v as i32;
            } else {
                return None;
            }
        }

        Some(result)
    }
}

#[allow(dead_code)]
fn read_input(filename: &str) -> std::io::Result<Vec<Entry>> {
    let lines = input_lines(filename)?;

    let mut result = Vec::new();

    for line in lines {
        let line = line?;
        let mut sections = line.split_terminator(" | ");
        let mut unique_patterns = sections
            .next()
            .unwrap()
            .split_whitespace()
            .map(|e| e.to_string())
            .collect::<Vec<String>>();

        unique_patterns.sort_by_key(|e| e.len());

        let output_values = sections
            .next()
            .unwrap()
            .split_whitespace()
            .map(|e| e.to_string())
            .collect::<Vec<String>>();

        result.push(Entry {
            unique_patterns,
            output_values,
        });
    }

    Ok(result)
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
        let entries = read_input("inputs/day8_test.txt").unwrap();

        println!("{:#?}", entries);
    }

    #[test]
    fn test_part1() {
        let entries = read_input("inputs/day8_test.txt").unwrap();
        let mut result = 0;

        for e in &entries {
            let count_1 = e.output_values.iter().filter(|e| e.len() == 2).count();
            let count_4 = e.output_values.iter().filter(|e| e.len() == 4).count();
            let count_7 = e.output_values.iter().filter(|e| e.len() == 3).count();
            let count_8 = e.output_values.iter().filter(|e| e.len() == 7).count();

            result += (count_1 + count_4 + count_7 + count_8) as i32;
        }

        assert_eq!(result, 26);
    }

    #[test]
    fn do_part1() {
        let entries = read_input("inputs/day8.txt").unwrap();
        let mut result = 0;

        for e in &entries {
            let count_1 = e.output_values.iter().filter(|e| e.len() == 2).count();
            let count_4 = e.output_values.iter().filter(|e| e.len() == 4).count();
            let count_7 = e.output_values.iter().filter(|e| e.len() == 3).count();
            let count_8 = e.output_values.iter().filter(|e| e.len() == 7).count();

            result += (count_1 + count_4 + count_7 + count_8) as i32;
        }

        println!("{}", result);
    }

    #[test]
    fn test_part2() {
        let entries = read_input("inputs/day8_test.txt").unwrap();

        for e in &entries {
            println!(
                "{:?}, {}",
                e.compute_digit_pattern(),
                e.output_value().unwrap()
            );
        }
    }

    #[test]
    fn test_part2_sum() {
        let entries = read_input("inputs/day8_test.txt").unwrap();

        let sum = entries
            .iter()
            .map(|e| e.output_value().unwrap())
            .sum::<i32>();

        assert_eq!(sum, 61229);
    }

    #[test]
    fn do_part2() {
        let entries = read_input("inputs/day8.txt").unwrap();

        let sum = entries
            .iter()
            .map(|e| e.output_value().unwrap())
            .sum::<i32>();

        println!("{}", sum);
    }
}
