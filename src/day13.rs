use std::cmp::max;

use super::input_lines;

#[allow(dead_code)]
fn read_folding_input(filename: &str) -> std::io::Result<Vec<(char, usize)>> {
    let lines = input_lines(filename)?;

    let mut result = Vec::new();

    for l in lines {
        let l = l?;
        let mut fold = l.split('=');
        let axis = fold.next().unwrap().chars().next().unwrap();
        let pos = fold.next().unwrap().parse::<usize>().unwrap();

        result.push((axis, pos));
    }

    Ok(result)
}

#[allow(dead_code)]
fn read_coords(filename: &str) -> std::io::Result<Vec<(usize, usize)>> {
    let lines = input_lines(filename)?;

    let mut result = Vec::new();

    for l in lines {
        let l = l?;

        let mut xy = l.split(',');
        let x = xy.next().unwrap().parse::<usize>().unwrap();
        let y = xy.next().unwrap().parse::<usize>().unwrap();

        result.push((x, y));
    }

    Ok(result)
}

#[allow(dead_code)]
fn read_map(filename: &str) -> std::io::Result<Vec<Vec<bool>>> {
    let coords = read_coords(filename)?;
    Ok(to_dense(&coords))
}

#[allow(dead_code)]
fn fold_coords_x(mut coords: Vec<(usize, usize)>, pos: usize) -> Vec<(usize, usize)> {
    for (x, _) in coords.iter_mut() {
        if *x > pos {
            *x = (pos - 1) - (*x - pos - 1);
        }
    }

    coords.sort_unstable();
    coords.dedup();

    coords
}

#[allow(dead_code)]
fn fold_coords_y(mut coords: Vec<(usize, usize)>, pos: usize) -> Vec<(usize, usize)> {
    for (_, y) in coords.iter_mut() {
        if *y > pos {
            *y = (pos - 1) - (*y - pos - 1);
        }
    }

    coords.sort_unstable();
    coords.dedup();

    coords
}

// naive version
#[allow(dead_code)]
fn fold_map_x(mut map: Vec<Vec<bool>>) -> Vec<Vec<bool>> {
    let pos = map[0].len() / 2;
    for l in map.iter_mut() {
        let mut later = l.split_off(pos + 1);
        l.pop();
        later.reverse();

        for (j, p) in l.iter_mut().enumerate() {
            *p |= later[j];
        }
    }

    map
}

// naive version
#[allow(dead_code)]
fn fold_map_y(map: Vec<Vec<bool>>) -> Vec<Vec<bool>> {
    let mut prio = map;
    let mut later = prio.split_off(prio.len() / 2);
    // throw away the split line
    prio.pop();
    later.reverse();

    for (i, l) in prio.iter_mut().enumerate() {
        for (j, p) in l.iter_mut().enumerate() {
            *p |= later[i][j];
        }
    }

    prio
}

#[allow(dead_code)]
fn to_dense(coords: &[(usize, usize)]) -> Vec<Vec<bool>> {
    let mut x_max = 0;
    let mut y_max = 0;

    for (x, y) in coords {
        x_max = max(x_max, *x);
        y_max = max(y_max, *y);
    }

    let mut result = vec![vec![false; x_max + 1]; y_max + 1];

    for (x, y) in coords {
        result[*y][*x] = true;
    }

    result
}

#[allow(dead_code)]
fn print_coords(coords: &[(usize, usize)]) {
    for (x, y) in coords {
        println!("({},{})", x, y);
    }
    println!("--------");
}

#[allow(dead_code)]
fn print_map(map: &[Vec<bool>]) {
    for l in map {
        let t = l
            .iter()
            .map(|p| if *p { "0" } else { " " })
            .collect::<Vec<_>>()
            .join("");
        println!("{}", t);
    }
    println!("--------");
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
        let map = read_map("inputs/day13_test.txt").unwrap();

        print_map(&map);

        let folds = read_folding_input("inputs/day13_test_fold.txt").unwrap();

        println!("{:?}", folds);
    }

    #[test]
    fn test_read_real_input() {
        let map = read_map("inputs/day13.txt").unwrap();

        print_map(&map);

        let folds = read_folding_input("inputs/day13_fold.txt").unwrap();

        println!("{:?}", folds);
    }

    #[test]
    fn test_part1() {
        let map = read_map("inputs/day13_test.txt").unwrap();
        let folds = read_folding_input("inputs/day13_test_fold.txt").unwrap();

        let result = if folds[0].0 == 'x' {
            fold_map_x(map)
        } else {
            fold_map_y(map)
        };

        print_map(&result);

        let mut n = 0;
        for l in &result {
            for c in l {
                if *c {
                    n += 1;
                }
            }
        }

        assert_eq!(n, 17);

        let result = if folds[1].0 == 'x' {
            fold_map_x(result)
        } else {
            fold_map_y(result)
        };

        print_map(&result);
    }

    #[test]
    fn test_part1_v2() {
        let coords = read_coords("inputs/day13_test.txt").unwrap();
        let folds = read_folding_input("inputs/day13_test_fold.txt").unwrap();

        let result = if folds[0].0 == 'x' {
            fold_coords_x(coords, folds[0].1)
        } else {
            fold_coords_y(coords, folds[0].1)
        };

        print_map(&to_dense(&result));

        assert_eq!(result.len(), 17);

        let result = if folds[1].0 == 'x' {
            fold_coords_x(result, folds[1].1)
        } else {
            fold_coords_y(result, folds[1].1)
        };

        print_map(&to_dense(&result));
    }

    #[test]
    fn do_part1() {
        let map = read_map("inputs/day13.txt").unwrap();
        let folds = read_folding_input("inputs/day13_fold.txt").unwrap();

        let result = if folds[0].0 == 'x' {
            fold_map_x(map)
        } else {
            fold_map_y(map)
        };

        let mut n = 0;
        for l in &result {
            for c in l {
                if *c {
                    n += 1;
                }
            }
        }

        assert_eq!(n, 802);
    }

    #[test]
    fn do_part1_v2() {
        let coords = read_coords("inputs/day13.txt").unwrap();
        let folds = read_folding_input("inputs/day13_fold.txt").unwrap();

        let result = if folds[0].0 == 'x' {
            fold_coords_x(coords, folds[0].1)
        } else {
            fold_coords_y(coords, folds[0].1)
        };

        let n = result.len();

        assert_eq!(n, 802);
    }

    #[test]
    fn do_part2() {
        let map = read_map("inputs/day13.txt").unwrap();
        let folds = read_folding_input("inputs/day13_fold.txt").unwrap();

        let mut result = map;

        for f in folds {
            result = if f.0 == 'x' {
                fold_map_x(result)
            } else {
                fold_map_y(result)
            };
        }

        print_map(&result);
    }

    #[test]
    fn do_part2_v2() {
        let coords = read_coords("inputs/day13.txt").unwrap();
        let folds = read_folding_input("inputs/day13_fold.txt").unwrap();

        let mut result = coords;

        for (axis, pos) in folds {
            result = if axis == 'x' {
                fold_coords_x(result, pos)
            } else {
                fold_coords_y(result, pos)
            };
        }

        print_map(&to_dense(&result));
    }

    #[test]
    fn do_part2_huge() {
        let coords = read_coords("inputs/day13_huge.txt").unwrap();
        let folds = read_folding_input("inputs/day13_huge_fold.txt").unwrap();

        let mut result = coords;

        for (axis, pos) in folds {
            result = if axis == 'x' {
                fold_coords_x(result, pos)
            } else {
                fold_coords_y(result, pos)
            };
        }

        print_map(&to_dense(&result));
    }
}
