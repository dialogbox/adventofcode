use std::{cmp::Ordering, collections::BinaryHeap, fmt::Display};

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
fn multiply_map(orig: Vec<Vec<u8>>, factor: usize) -> Vec<Vec<u8>> {
    let mut result = vec![vec![0; orig[0].len() * factor]; orig.len() * factor];

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

#[derive(Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    position: (usize, usize),
    path: Vec<(usize, usize)>,
}

// The priority queue depends on `Ord`.
// Explicitly implement the trait so the queue becomes a min-heap
// instead of a max-heap.
impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        // Notice that the we flip the ordering on costs.
        // In case of a tie we compare positions - this step is necessary
        // to make implementations of `PartialEq` and `Ord` consistent.
        other
            .cost
            .cmp(&self.cost)
            .then_with(|| self.position.cmp(&other.position))
    }
}

// `PartialOrd` needs to be implemented as well.
impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

#[allow(dead_code)]
fn shortest_path(map: &[Vec<u8>]) -> Option<(usize, Vec<(usize, usize)>)> {
    let width = map[0].len();
    let height = map.len();
    let goal = (width - 1, height - 1);

    let mut dist = vec![vec![usize::MAX; width]; height];
    dist[0][0] = 0;

    let mut heap = BinaryHeap::new();
    heap.push(State {
        cost: 0,
        position: (0, 0),
        path: vec![(0, 0)],
    });

    while let Some(State {
        cost,
        position,
        path,
    }) = heap.pop()
    {
        // Alternatively we could have continued to find all shortest paths
        if position == goal {
            return Some((cost, path));
        }

        let (x, y) = position;

        // Important as we may have already found a better way
        if cost > dist[y][x] {
            continue;
        }

        let mut adjacents = Vec::new();
        // For each adjacent we can reach, see if we can find a way with
        // a lower cost going through this node
        if x > 0 {
            // left
            adjacents.push((x - 1, y));
        }
        if x < width - 1 {
            // right
            adjacents.push((x + 1, y));
        }
        if y > 0 {
            // top
            adjacents.push((x, y - 1));
        }
        if y < height - 1 {
            // down
            adjacents.push((x, y + 1));
        }

        for (next_x, next_y) in adjacents {
            let mut next_path = path.clone();
            next_path.push((next_x, next_y));

            let next = State {
                cost: cost + map[next_y][next_x] as usize,
                position: (next_x, next_y),
                path: next_path,
            };

            // If so, add it to the frontier and continue
            if next.cost < dist[next_y][next_x] {
                // Relaxation, we have now found a better way
                dist[next_y][next_x] = next.cost;

                heap.push(next);
            }
        }
    }

    None
}

#[allow(dead_code)]
fn print_map<T>(map: &[Vec<T>])
where
    T: Display,
{
    for l in map {
        for c in l {
            print!("{:^5} ", *c);
        }
        println!();
    }
}

#[allow(dead_code)]
fn print_map_dense<T>(map: &[Vec<T>])
where
    T: Display,
{
    for l in map {
        for c in l {
            print!("{} ", *c);
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

        let (cost, _path) = shortest_path(&map).unwrap();

        println!("{}", cost);
    }

    #[test]
    fn do_part1() {
        let map = read_input("inputs/day15.txt").unwrap();

        let (cost, _path) = shortest_path(&map).unwrap();

        assert_eq!(cost, 720);
    }

    #[test]
    fn test_part2() {
        let map = read_input("inputs/day15_test.txt").unwrap();
        let map = multiply_map(map, 5);

        let (cost, _path) = shortest_path(&map).unwrap();

        assert_eq!(cost, 315);
    }

    #[test]
    fn do_part2() {
        let map = read_input("inputs/day15.txt").unwrap();
        let map = multiply_map(map, 5);

        let (cost, _path) = shortest_path(&map).unwrap();

        assert_eq!(cost, 3025);
    }
}
