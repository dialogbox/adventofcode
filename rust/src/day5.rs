use std::fmt::Display;

use super::read_raw_lines;

pub struct Line {
    p1: (usize, usize),
    p2: (usize, usize),
}

impl Display for Line {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!(
            "({},{}) -> ({},{})",
            self.p1.0, self.p1.1, self.p2.0, self.p2.1
        ))
        .unwrap();

        Ok(())
    }
}

#[allow(dead_code)]
#[derive(Debug)]
pub struct WorldMap {
    width: usize,
    height: usize,
    map: Vec<Vec<u32>>,
}

impl Display for WorldMap {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for y in 0..self.height {
            for x in 0..self.width {
                if self.map[x][y] == 0 {
                    f.pad(".").unwrap();
                } else {
                    f.write_fmt(format_args!("{}", self.map[x][y])).unwrap();
                }
            }
            f.pad("\n").unwrap();
        }

        Ok(())
    }
}

impl WorldMap {
    #[allow(dead_code)]
    pub fn with_size(width: usize, height: usize) -> WorldMap {
        WorldMap {
            width,
            height,
            map: vec![vec![0; height]; width],
        }
    }

    #[allow(dead_code)]
    pub fn add_line(&mut self, line: &Line) {
        let (x1, y1) = line.p1;
        let (x2, y2) = line.p2;

        // Vertical Line
        if x1 == x2 {
            for y in if y1 > y2 { y2..=y1 } else { y1..=y2 } {
                self.map[x1][y] += 1;
            }
        // Horizontal Line
        } else if y1 == y2 {
            for x in if x1 > x2 { x2..=x1 } else { x1..=x2 } {
                self.map[x][y1] += 1;
            }
        }
    }

    #[allow(dead_code)]
    pub fn add_line_v2(&mut self, line: &Line) {
        let (x1, y1) = line.p1;
        let (x2, y2) = line.p2;
        let (x1, y1, x2, y2) = (x1 as i32, y1 as i32, x2 as i32, y2 as i32);

        let x_gap = if x2 >= x1 { x2 - x1 + 1 } else { x2 - x1 - 1 };
        let y_gap = if y2 >= y1 { y2 - y1 + 1 } else { y2 - y1 - 1 };

        let x_dist = x_gap.abs();
        let y_dist = y_gap.abs();

        let dist = std::cmp::max(x_dist, y_dist);

        let x_step = x_gap / dist;
        let y_step = y_gap / dist;

        for d in 0..dist {
            let gx = x1 + d * x_step;
            let gy = y1 + d * y_step;
            self.map[gx as usize][gy as usize] += 1;
        }
    }

    #[allow(dead_code)]
    pub fn number_of_danger_points(&self) -> u32 {
        let mut result = 0;
        for x in 0..self.width {
            for y in 0..self.height {
                if self.map[x][y] >= 2 {
                    result += 1;
                }
            }
        }

        result
    }
}

#[allow(dead_code)]
pub fn read_input(filename: &str) -> std::io::Result<Vec<Line>> {
    let lines = read_raw_lines(filename)?;

    let mut result: Vec<Line> = Vec::new();

    for line in lines {
        let line = line.unwrap();
        let t: Vec<&str> = line.split(" -> ").collect();

        let mut p = t[0].split(',');
        let x1 = p.next().unwrap();
        let y1 = p.next().unwrap();

        let mut p = t[1].split(',');
        let x2 = p.next().unwrap();
        let y2 = p.next().unwrap();

        result.push(Line {
            p1: (x1.parse::<_>().unwrap(), y1.parse::<_>().unwrap()),
            p2: (x2.parse::<_>().unwrap(), y2.parse::<_>().unwrap()),
        })
    }

    Ok(result)
}

#[allow(dead_code)]
fn determine_world_size(lines: &[Line]) -> (usize, usize) {
    let mut width: usize = 0;
    let mut height: usize = 0;

    for l in lines {
        width = std::cmp::max(std::cmp::max(l.p1.0, l.p2.0), width);
        height = std::cmp::max(std::cmp::max(l.p1.1, l.p2.1), height);
    }

    (width, height)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_some() {
        println!("{:?}", (0..10).zip(0..5).collect::<Vec<_>>());
    }

    #[test]
    fn test_read_lines() {
        let lines = read_input("../inputs/day5.txt").unwrap();

        for l in lines {
            println!("{}", l);
        }
    }

    #[test]
    fn test_create_map() {
        let map = WorldMap::with_size(10, 10);

        println!("{}", map);
    }

    #[test]
    fn test_add_lines() {
        let mut map = WorldMap::with_size(10, 10);

        map.add_line_v2(&Line {
            p1: (3, 0),
            p2: (0, 0),
        });

        map.add_line_v2(&Line {
            p1: (2, 0),
            p2: (2, 5),
        });

        println!("{}", map);
    }

    #[test]
    fn test_add_lines_with_test_input() {
        let lines = read_input("../inputs/day5_test.txt").unwrap();
        let (width, height) = determine_world_size(&lines);

        let mut map = WorldMap::with_size(width + 1, height + 1);

        for l in lines {
            map.add_line(&l);
        }

        println!("{}", map);
        println!("{}", map.number_of_danger_points());
    }

    #[test]
    fn test_add_lines_with_input() {
        let lines = read_input("../inputs/day5.txt").unwrap();
        let (width, height) = determine_world_size(&lines);

        let mut map = WorldMap::with_size(width + 1, height + 1);

        for l in lines {
            map.add_line(&l);
        }

        println!("{}", map.number_of_danger_points());
    }

    #[test]
    fn test_add_lines_v2_with_test_input() {
        let lines = read_input("../inputs/day5_test.txt").unwrap();
        let (width, height) = determine_world_size(&lines);

        let mut map = WorldMap::with_size(width + 1, height + 1);

        for l in lines {
            map.add_line_v2(&l);
        }

        println!("{}", map);
        println!("{}", map.number_of_danger_points());
    }

    #[test]
    fn test_add_lines_v2_with_input() {
        let lines = read_input("../inputs/day5.txt").unwrap();
        let (width, height) = determine_world_size(&lines);

        let mut map = WorldMap::with_size(width + 1, height + 1);

        for l in lines {
            map.add_line_v2(&l);
        }

        println!("{}", map.number_of_danger_points());
    }
}
