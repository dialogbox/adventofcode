use std::collections::HashMap;

use super::input_lines;

//
// General idea here is instead of building concrate string, just maintain number of possible 2 char pairs
// Everytime a rule is applied, all of the pairs in the string turned to two pairs of the same numbers
// Ex)
// HB -> K
//
// Which means if there were n numbers of "HB", it will be n "HK"s and n "KB"s.
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
fn convert_rules(rules: &HashMap<[char; 2], char>) -> HashMap<[char; 2], [[char; 2]; 2]> {
    let mut result = HashMap::new();

    for (pat, &c) in rules {
        result.insert(*pat, [[pat[0], c], [c, pat[1]]]);
    }

    result
}

#[allow(dead_code)]
fn convert_template(seed: &str) -> HashMap<[char; 2], u64> {
    let mut result: HashMap<[char; 2], u64> = HashMap::new();

    let mut chars = seed.chars();
    let first = chars.next().unwrap();
    let mut buf = [' ', first];

    for c in chars {
        buf[0] = buf[1];
        buf[1] = c;

        let prev = result.entry(buf).or_insert(0);
        *prev += 1;
    }

    result
}

#[allow(dead_code)]
fn step(
    rules: &HashMap<[char; 2], [[char; 2]; 2]>,
    mut seed: HashMap<[char; 2], u64>,
) -> HashMap<[char; 2], u64> {
    let mut result = Vec::new();
    for (pair, count) in seed.iter() {
        let new_pairs = rules.get(pair).unwrap();

        result.push((new_pairs[0], *count));
        result.push((new_pairs[1], *count));
    }

    seed.clear();

    for (pat, c) in result {
        let orig = seed.entry(pat).or_insert(0);
        *orig += c;
    }

    seed
}

#[allow(dead_code)]
fn count_chars(pat_counts: &HashMap<[char; 2], u64>, initial_template: &str) -> HashMap<char, u64> {
    let mut counts = HashMap::new();

    // We do this because all chars are counted twice except the first and the last character of the input string.
    // So +1 for the first/last char and devide by 2 for all the counts
    *counts
        .entry(initial_template.chars().next().unwrap())
        .or_insert(0) += 1;
    *counts
        .entry(initial_template.chars().last().unwrap())
        .or_insert(0) += 1;

    for (pair, count) in pat_counts {
        let orig = counts.entry(pair[0]).or_insert(0);
        *orig += count;
        let orig = counts.entry(pair[1]).or_insert(0);
        *orig += count;
    }

    for c in counts.values_mut() {
        *c /= 2;
    }

    counts
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_some() {
        let mut n = 20 as i64;
        for _ in 0..40 {
            n += n - 1;
        }

        println!("{}", n);
    }

    #[test]
    fn test_read_input() {
        let (tmpl, rules) = read_input("inputs/day14_test.txt").unwrap();

        println!("{}", tmpl);
        println!("{:?}", rules);
    }

    #[test]
    fn test_part1() {
        let (tmpl, rules) = read_input("inputs/day14_test.txt").unwrap();
        let rules = convert_rules(&rules);
        let mut seeds = convert_template(&tmpl);

        for _ in 0..10 {
            seeds = step(&rules, seeds);
        }

        let counts = count_chars(&seeds, &tmpl);

        let max = counts.iter().max_by_key(|&(_, count)| count).unwrap();
        let min = counts.iter().min_by_key(|&(_, count)| count).unwrap();

        assert_eq!(max.1 - min.1, 1588);
    }

    #[test]
    fn do_part1() {
        let (tmpl, rules) = read_input("inputs/day14.txt").unwrap();
        let rules = convert_rules(&rules);
        let mut seeds = convert_template(&tmpl);

        for _ in 0..10 {
            seeds = step(&rules, seeds);
        }

        let counts = count_chars(&seeds, &tmpl);

        let max = counts.iter().max_by_key(|&(_, count)| count).unwrap();
        let min = counts.iter().min_by_key(|&(_, count)| count).unwrap();

        assert_eq!(max.1 - min.1, 2549);
    }

    #[test]
    fn do_part2() {
        let (tmpl, rules) = read_input("inputs/day14.txt").unwrap();
        let rules = convert_rules(&rules);
        let mut seeds = convert_template(&tmpl);

        for _ in 0..40 {
            seeds = step(&rules, seeds);
        }

        let counts = count_chars(&seeds, &tmpl);

        let max = counts.iter().max_by_key(|&(_, count)| count).unwrap();
        let min = counts.iter().min_by_key(|&(_, count)| count).unwrap();

        assert_eq!(max.1 - min.1, 2516901104210);
    }
}
