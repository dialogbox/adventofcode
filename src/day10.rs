use super::input_lines;

#[allow(dead_code)]
fn read_input(filename: &str) -> std::io::Result<Vec<String>> {
    let lines = input_lines(filename)?;

    let mut result = Vec::new();

    for l in lines {
        result.push(l?);
    }

    Ok(result)
}

#[allow(dead_code)]
fn check_error(input: &str) -> Option<usize> {
    let mut stack = Vec::<char>::new();

    for (i, c) in input.chars().enumerate() {
        match c {
            '(' | '[' | '{' | '<' => stack.push(c),
            ')' | ']' | '}' | '>' => {
                if let Some(last) = stack.pop() {
                    if (last == '(' && c == ')')
                        || (last == '[' && c == ']')
                        || (last == '{' && c == '}')
                        || (last == '<' && c == '>')
                    {
                        continue;
                    } else {
                        return Some(i);
                    }
                } else {
                    return Some(i);
                }
            }
            _ => return Some(i),
        }
    }

    None
}

#[allow(dead_code)]
fn complete_line(input: &str) -> Option<String> {
    let mut stack = Vec::<char>::new();

    for c in input.chars() {
        match c {
            '(' | '[' | '{' | '<' => stack.push(c),
            ')' | ']' | '}' | '>' => {
                if let Some(last) = stack.pop() {
                    if (last == '(' && c == ')')
                        || (last == '[' && c == ']')
                        || (last == '{' && c == '}')
                        || (last == '<' && c == '>')
                    {
                        continue;
                    } else {
                        return None;
                    }
                } else {
                    return None;
                }
            }
            _ => return None,
        }
    }

    let mut result = "".to_owned();

    for c in stack.iter().rev() {
        match *c {
            '(' => result.push(')'),
            '[' => result.push(']'),
            '{' => result.push('}'),
            '<' => result.push('>'),
            _ => panic!("Huh?"),
        }
    }

    Some(result)
}

#[allow(dead_code)]
fn get_error_score(c: char) -> i32 {
    match c {
        '(' | ')' => 3,
        '[' | ']' => 57,
        '{' | '}' => 1197,
        '<' | '>' => 25137,
        _ => panic!("What?"),
    }
}

#[allow(dead_code)]
fn get_completion_score(c: char) -> i32 {
    match c {
        '(' | ')' => 1,
        '[' | ']' => 2,
        '{' | '}' => 3,
        '<' | '>' => 4,
        _ => panic!("What?"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_some() {
        let a = vec![1, 2, 3];
        println!(
            "{} {} {}",
            a.last().unwrap(),
            a.last().unwrap(),
            a.last().unwrap()
        );
    }

    #[test]
    fn test_read_input() {
        let lines = read_input("inputs/day10_test.txt").unwrap();

        println!("{:#?}", lines);
    }

    #[test]
    fn test_day1() {
        let lines = read_input("inputs/day10_test.txt").unwrap();

        let mut sum = 0;
        for l in &lines {
            if let Some(i) = check_error(l) {
                sum += get_error_score(l.chars().nth(i).unwrap());
            }
        }
        assert_eq!(sum, 26397);
    }

    #[test]
    fn do_day1() {
        let lines = read_input("inputs/day10.txt").unwrap();

        let mut sum = 0;
        for l in &lines {
            if let Some(i) = check_error(l) {
                sum += get_error_score(l.chars().nth(i).unwrap());
            }
        }
        println!("{}", sum);
    }

    #[test]
    fn test_day2() {
        let lines = read_input("inputs/day10_test.txt").unwrap();

        let mut scores = Vec::new();

        for l in &lines {
            if let Some(s) = complete_line(l) {
                let total_score = s
                    .chars()
                    .into_iter()
                    .map(get_completion_score)
                    .fold(0, |acc, s| acc * 5 + s);

                scores.push(total_score);
            }
        }

        scores.sort_unstable();

        let answer = scores[scores.len() / 2];

        assert_eq!(answer, 288957);
    }

    #[test]
    fn do_day2() {
        let lines = read_input("inputs/day10.txt").unwrap();

        let mut scores = Vec::new();

        for l in &lines {
            if let Some(s) = complete_line(l) {
                let total_score = s
                    .chars()
                    .into_iter()
                    .map(|c| get_completion_score(c) as i64)
                    .fold(0, |acc, s| acc * 5 + s);

                scores.push(total_score);
            }
        }

        scores.sort_unstable();

        let answer = scores[scores.len() / 2];

        assert_eq!(answer, 3103006161);
    }
}
