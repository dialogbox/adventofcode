use std::collections::HashSet;

use super::input_lines;

#[allow(dead_code)]
fn read_input(filename: &str) -> std::io::Result<Vec<Vec<u8>>> {
    let lines = input_lines(filename)?;

    let mut result = Vec::new();

    for l in lines {
        result.push(
            l?.chars()
                .map(|c| c.to_digit(10).unwrap() as u8)
                .collect::<Vec<u8>>(),
        );
    }

    Ok(result)
}

#[allow(dead_code)]
fn find_low_points(map: &[Vec<u8>]) -> Vec<(usize, usize)> {
    let mut result = Vec::new();

    let map_height = map.len();
    let map_width = map[0].len();

    for i in 0..map_height {
        for j in 0..map_width {
            let cur = map[i][j];

            if i != 0 && cur >= map[i - 1][j] {
                continue;
            }
            if i != map_height - 1 && cur >= map[i + 1][j] {
                continue;
            }
            if j != 0 && cur >= map[i][j - 1] {
                continue;
            }
            if j != map_width - 1 && cur >= map[i][j + 1] {
                continue;
            }

            result.push((i, j));
        }
    }

    result
}

#[allow(dead_code)]
fn total_risk_level(map: &[Vec<u8>], points: &[(usize, usize)]) -> i32 {
    points
        .iter()
        .map(|(i, j)| map[*i][*j] + 1)
        .map(|n| n as i32)
        .sum::<i32>()
}

#[allow(dead_code)]
fn find_basin(map: &[Vec<u8>], x: usize, y: usize) -> HashSet<(usize, usize)> {
    let mut result: HashSet<(usize, usize)> = HashSet::new();
    let mut tmp: Vec<(usize, usize)> = Vec::with_capacity(4);
    result.insert((x, y));
    let mut prev_size = 1;

    let map_height = map.len();
    let map_width = map[0].len();

    loop {
        for (i, j) in &result {
            let (i, j) = (*i, *j);

            if i != 0 && map[i - 1][j] != 9 {
                tmp.push((i - 1, j));
            }
            if i != map_height - 1 && map[i + 1][j] != 9 {
                tmp.push((i + 1, j));
            }
            if j != 0 && map[i][j - 1] != 9 {
                tmp.push((i, j - 1));
            }
            if j != map_width - 1 && map[i][j + 1] != 9 {
                tmp.push((i, j + 1));
            }
        }

        tmp.iter().for_each(|(i, j)| {
            result.insert((*i, *j));
        });

        tmp.clear();

        if result.len() == prev_size {
            break;
        }
        prev_size = result.len();
    }

    result
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
        let map = read_input("../inputs/day9_test.txt").unwrap();

        println!("{:#?}", map);
    }

    #[test]
    fn test_part1() {
        let map = read_input("../inputs/day9_test.txt").unwrap();

        let low_points = find_low_points(&map);

        for (i, j) in &low_points {
            println!("{}", map[*i][*j]);
        }

        let risk_level = total_risk_level(&map, &low_points);

        assert_eq!(risk_level, 15);
    }

    #[test]
    fn do_part1() {
        let map = read_input("../inputs/day9.txt").unwrap();

        let low_points = find_low_points(&map);
        let risk_level = total_risk_level(&map, &low_points);

        println!("{}", risk_level);
    }
    #[test]
    fn test_part2() {
        let map = read_input("../inputs/day9_test.txt").unwrap();

        let low_points = find_low_points(&map);

        let mut basin_sizes = low_points
            .iter()
            .map(|(i, j)| find_basin(&map, *i, *j))
            .map(|b| b.len())
            .collect::<Vec<usize>>();

        basin_sizes.sort_unstable();
        let answer =
            basin_sizes.pop().unwrap() * basin_sizes.pop().unwrap() * basin_sizes.pop().unwrap();

        assert_eq!(answer, 1134);
    }

    #[test]
    fn do_part2() {
        let map = read_input("../inputs/day9.txt").unwrap();

        let low_points = find_low_points(&map);

        let mut basin_sizes = low_points
            .iter()
            .map(|(i, j)| find_basin(&map, *i, *j))
            .map(|b| b.len())
            .collect::<Vec<usize>>();

        basin_sizes.sort_unstable();
        let answer =
            basin_sizes.pop().unwrap() * basin_sizes.pop().unwrap() * basin_sizes.pop().unwrap();

        println!("{}", answer);
    }
}
