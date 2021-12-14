use std::collections::HashMap;

use super::input_lines;

#[allow(dead_code)]
fn read_input(filename: &str) -> std::io::Result<(String, HashMap<[char; 2], char>)> {
    let mut lines = input_lines(filename)?;

    let templ = lines.next().unwrap()?;
    lines.next();

    let mut result = HashMap::new();

    for l in lines {
        let l = l?;
        let mut pair = l.split_terminator(" -> ");
        let mut t = pair.next().unwrap().chars();
        let pat = [t.next().unwrap(), t.next().unwrap()];
        let i = pair.next().unwrap().chars().next().unwrap();

        result.insert(pat, i);
    }

    Ok((templ, result))
}

#[allow(dead_code)]
fn step(rules: &HashMap<[char; 2], char>, seed: &str) -> String {
    let mut chars = seed.chars();

    let first = chars.next().unwrap();
    let mut cur = [' ', first];
    let mut result = vec![first];

    for c in chars {
        cur[0] = cur[1];
        cur[1] = c;

        let n = rules.get(&cur).unwrap();

        result.push(*n);
        result.push(c);
    }

    result.iter().collect()
}

#[cfg(test)]
mod tests {
    use std::collections::BTreeMap;

    use super::*;

    #[test]
    fn test_some() {
        println!("{:?}", (0..10).zip(0..5).collect::<Vec<_>>());
    }

    #[test]
    fn test_read_input() {
        let (tmpl, rules) = read_input("inputs/day14_test.txt").unwrap();

        println!("{}", tmpl);
        println!("{:?}", rules);
    }

    #[test]
    fn test_part1() {
        let (mut tmpl, rules) = read_input("inputs/day14_test.txt").unwrap();

        for _ in 0..10 {
            tmpl = step(&rules, &tmpl);
        }

        let mut counts = BTreeMap::new();
        for c in tmpl.chars() {
            *counts.entry(c).or_insert(0) += 1;
        }

        let max = counts.iter().max_by_key(|&(_, count)| count).unwrap();
        let min = counts.iter().min_by_key(|&(_, count)| count).unwrap();

        assert_eq!(max.1 - min.1, 1588);
    }

    #[test]
    fn do_part1() {
        let (mut tmpl, rules) = read_input("inputs/day14.txt").unwrap();

        for _ in 0..10 {
            tmpl = step(&rules, &tmpl);
        }

        let mut counts = BTreeMap::new();
        for c in tmpl.chars() {
            *counts.entry(c).or_insert(0) += 1;
        }

        let max = counts.iter().max_by_key(|&(_, count)| count).unwrap();
        let min = counts.iter().min_by_key(|&(_, count)| count).unwrap();

        assert_eq!(max.1 - min.1, 2549);
    }

    #[test]
    fn do_part2() {
        let (mut tmpl, rules) = read_input("inputs/day14.txt").unwrap();

        for i in 0..40 {
            tmpl = step(&rules, &tmpl);
            println!("{}, {}", i, tmpl.len());
        }

        let mut counts = BTreeMap::new();
        for c in tmpl.chars() {
            *counts.entry(c).or_insert(0) += 1 as u64;
        }

        let max = counts.iter().max_by_key(|&(_, count)| count).unwrap();
        let min = counts.iter().min_by_key(|&(_, count)| count).unwrap();

        println!("{}", max.1 - min.1);
    }
}
