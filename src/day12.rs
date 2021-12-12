use super::input_lines;
use std::collections::{HashMap, HashSet};

#[allow(dead_code)]
#[derive(Debug, PartialEq)]
enum Type {
    Start,
    End,
    SmallCave,
    LargeCave,
}

#[allow(dead_code)]
#[derive(Debug)]
struct Cave {
    cave_type: Type,
    name: String,
    connection: HashSet<String>,
}

impl Cave {
    fn with_name(name: &str) -> Cave {
        let t = match name {
            "start" => Type::Start,
            "end" => Type::End,

            _ => {
                if name == name.to_uppercase() {
                    Type::LargeCave
                } else {
                    Type::SmallCave
                }
            }
        };
        Cave {
            cave_type: t,
            name: name.to_string(),
            connection: HashSet::new(),
        }
    }
}

#[allow(dead_code)]
fn read_input(filename: &str) -> std::io::Result<HashMap<String, Cave>> {
    let lines = input_lines(filename)?;

    let mut caves = HashMap::new();

    caves.insert("start".to_string(), Cave::with_name("start"));
    caves.insert("end".to_string(), Cave::with_name("end"));

    for l in lines {
        let l = l?;
        let mut elems = l.split_terminator("-");
        let from_str = elems.next().unwrap();
        let to_str = elems.next().unwrap();

        if !caves.contains_key(from_str) {
            caves.insert(from_str.to_string(), Cave::with_name(from_str));
        }
        if !caves.contains_key(to_str) {
            caves.insert(to_str.to_string(), Cave::with_name(to_str));
        }

        let mut from = caves.remove(from_str).unwrap();
        let mut to = caves.remove(to_str).unwrap();

        from.connection.insert(to.name.to_string());
        to.connection.insert(from.name.to_string());

        caves.insert(from.name.clone(), from);
        caves.insert(to.name.clone(), to);
    }

    Ok(caves)
}

#[allow(dead_code)]
fn find_next_paths<'a>(
    map: &'a HashMap<String, Cave>,
    start: &Cave,
    parent_path: &Vec<String>,
    allowed_visit_for_smallcave: usize,
) -> Vec<Vec<String>> {
    let mut result = Vec::new();

    let mut current_path = parent_path.clone();
    current_path.push(start.name.to_string());

    if start.cave_type == Type::End {
        return vec![current_path];
    }

    for i in &start.connection {
        let next = map.get(i).unwrap();

        if next.cave_type == Type::Start {
            continue;
        }
        if next.cave_type == Type::SmallCave {
            let mut n_visited_for_all = HashMap::new();
            for p in &current_path {
                if map.get(p).unwrap().cave_type != Type::SmallCave {
                    continue;
                }
                if !n_visited_for_all.contains_key(p) {
                    n_visited_for_all.insert(p, 0);
                }
                *n_visited_for_all.get_mut(p).unwrap() += 1;
            }

            let n_visited = *n_visited_for_all.get(&next.name).unwrap_or(&0);

            if allowed_visit_for_smallcave == 1 {
                if n_visited == 1 {
                    continue;
                }
            } else {
                let is_already_max_visited = n_visited_for_all
                    .iter()
                    .find(|p| *p.1 as usize == allowed_visit_for_smallcave)
                    .iter()
                    .next()
                    .is_some();

                if n_visited as usize >= allowed_visit_for_smallcave - 1 && is_already_max_visited {
                    continue;
                }
            }
        }

        result.append(&mut find_next_paths(
            map,
            next,
            &current_path,
            allowed_visit_for_smallcave,
        ));
    }

    result
}

#[allow(dead_code)]
fn find_paths<'a>(
    map: &'a HashMap<String, Cave>,
    allowed_visit_for_smallcave: usize,
) -> Vec<Vec<String>> {
    let start = map.get("start").unwrap();

    find_next_paths(map, start, &Vec::new(), allowed_visit_for_smallcave)
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
        let input = read_input("inputs/day12_test.txt").unwrap();

        println!("{:?}", input);
    }

    #[test]
    fn test_part1() {
        let map = read_input("inputs/day12_test.txt").unwrap();

        let paths = find_paths(&map, 1);

        for p in &paths {
            println!("{:?}", p);
        }

        assert_eq!(paths.len(), 10);
    }

    #[test]
    fn do_part1() {
        let map = read_input("inputs/day12.txt").unwrap();

        let paths = find_paths(&map, 1);

        for p in &paths {
            println!("{:?}", p);
        }

        assert_eq!(paths.len(), 3495);
    }

    #[test]
    fn test_part2() {
        let map = read_input("inputs/day12_test.txt").unwrap();

        let paths = find_paths(&map, 2);

        for p in &paths {
            println!("{}", p.join(","));
        }

        assert_eq!(paths.len(), 36);
    }

    #[test]
    fn do_part2() {
        let map = read_input("inputs/day12.txt").unwrap();

        let paths = find_paths(&map, 2);

        assert_eq!(paths.len(), 94849);
    }
}
