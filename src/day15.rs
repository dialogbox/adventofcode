use std::{cmp::min, fmt::Display};

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

fn multiply_map(orig: Vec<Vec<u8>>, factor: usize) -> Vec<Vec<u8>> {
    let mut result = vec![vec![0 as u8; orig[0].len() * factor]; orig.len() * factor];

    let o_width = orig[0].len();
    let o_height = orig.len();

    for y in 0..result.len() {
        for x in 0..result[0].len() {
            result[y][x] =
                orig[y % o_height][x % o_width] + (x / o_width) as u8 + (y / o_height) as u8;

            if result[y][x] > 9 {
                result[y][x] %= 9;
            }
        }
    }

    result
}

fn visit(
    map: &Vec<Vec<u8>>,
    distance_map: &mut Vec<Vec<i32>>,
    unvisited: &mut Vec<Vec<bool>>,
    x: usize,
    y: usize,
) {
    let width = map[0].len();
    let height = map.len();

    if !unvisited[y][x] {
        return;
    }

    let cur_dist = distance_map[y][x];

    if x > 0 && unvisited[y][x - 1] {
        distance_map[y][x - 1] = min(distance_map[y][x - 1], cur_dist + map[y][x - 1] as i32);
    }
    if x < width - 1 && unvisited[y][x + 1] {
        distance_map[y][x + 1] = min(distance_map[y][x + 1], cur_dist + map[y][x + 1] as i32);
    }
    if y > 0 && unvisited[y - 1][x] {
        distance_map[y - 1][x] = min(distance_map[y - 1][x], cur_dist + map[y - 1][x] as i32);
    }
    if y < height - 1 && unvisited[y + 1][x] {
        distance_map[y + 1][x] = min(distance_map[y + 1][x], cur_dist + map[y + 1][x] as i32);
    }

    unvisited[y][x] = false;
}

#[allow(dead_code)]
fn shortest_path(map: &Vec<Vec<u8>>) -> Vec<Vec<i32>> {
    let width = map[0].len();
    let height = map.len();

    let mut distance_map = vec![vec![i32::MAX; width]; height];
    distance_map[0][0] = 0;

    let mut risk = 0;
    for _ in 0..10 {
        let mut unvisited = vec![vec![true; width]; height];
        for y in 0..height {
            for x in 0..width {
                visit(map, &mut distance_map, &mut unvisited, x, y);
            }
        }

        let mut unvisited = vec![vec![true; width]; height];
        for t_y in 0..height {
            let y = height - 1 - t_y;
            for t_x in 0..width {
                let x = width - 1 - t_x;
                visit(map, &mut distance_map, &mut unvisited, x, y);
            }
        }

        if risk == distance_map[height - 1][width - 1] {
            break;
        }
        risk = distance_map[height - 1][width - 1];
        println!("Risk {}", risk);
    }

    distance_map
}

#[allow(dead_code)]
fn print_map<T>(map: &Vec<Vec<T>>)
where
    T: Display,
{
    let width = map[0].len();
    let height = map.len();

    for y in 0..height {
        for x in 0..width {
            print!("{:^5} ", map[y][x]);
        }
        println!();
    }
}

#[allow(dead_code)]
fn print_map_dense<T>(map: &Vec<Vec<T>>)
where
    T: Display,
{
    let width = map[0].len();
    let height = map.len();

    for y in 0..height {
        for x in 0..width {
            print!("{}", map[y][x]);
        }
        println!();
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_read_input() {
        let map = read_input("inputs/day15_test.txt").unwrap();

        println!("{:#?}", map);
    }

    #[test]
    fn test_part1() {
        let map = read_input("inputs/day15_test.txt").unwrap();

        let result = shortest_path(&map);

        print_map(&result);
    }

    #[test]
    fn test_part1_2() {
        let map = read_input("inputs/day15_test2.txt").unwrap();

        let result = shortest_path(&map);

        print_map(&result);
    }

    #[test]
    fn do_part1() {
        let map = read_input("inputs/day15.txt").unwrap();

        let result = shortest_path(&map);

        println!("{}", result[result.len() - 1][result[0].len() - 1]);
    }

    #[test]
    fn test_part2() {
        let map = read_input("inputs/day15_test.txt").unwrap();
        let map = multiply_map(map, 5);

        let result = shortest_path(&map);

        println!("{}", result[result.len() - 1][result[0].len() - 1]);
    }

    #[test]
    fn do_part2() {
        let map = read_input("inputs/day15.txt").unwrap();
        let map = multiply_map(map, 5);

        let result = shortest_path(&map);

        println!("{}", result[result.len() - 1][result[0].len() - 1]);
    }
}
