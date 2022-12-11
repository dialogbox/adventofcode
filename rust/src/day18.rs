use std::collections::BinaryHeap;

use super::read_raw_lines;

#[derive(Debug, Clone, Copy)]
struct Value {
    depth: usize,
    value: u32,
}

#[allow(dead_code)]
fn read_expr(input: &str) -> Vec<Value> {
    let mut result = Vec::new();

    let mut depth = 0;
    for c in input.chars() {
        match c {
            '[' => depth += 1,
            ']' => depth -= 1,
            ',' => (),
            _ => {
                result.push(Value {
                    depth,
                    value: c.to_digit(10).unwrap(),
                });
            }
        }
    }

    result
}

#[allow(dead_code)]
fn read_input(filename: &str) -> std::io::Result<Vec<Vec<Value>>> {
    let lines = read_raw_lines(filename)?;

    let mut result = Vec::new();

    for l in lines {
        result.push(read_expr(&l?));
    }

    Ok(result)
}

#[allow(dead_code)]
fn leftmost_deep_pair(expr: &[Value]) -> Option<usize> {
    let mut iter = expr.iter();

    let mut cur = iter.next()?;
    for (i, v) in iter.enumerate() {
        if cur.depth > 4 && cur.depth == v.depth {
            return Some(i);
        }
        cur = v;
    }

    None
}

#[allow(dead_code)]
fn explode(expr: &mut Vec<Value>) -> Option<usize> {
    let i = leftmost_deep_pair(expr)?;

    let l = expr[i].value;
    let r = expr[i + 1].value;

    if i != 0 {
        expr[i - 1].value += l;
    }
    if i < expr.len() - 2 {
        expr[i + 2].value += r;
    }

    expr[i].depth -= 1;
    expr[i].value = 0;

    expr.remove(i + 1);

    Some(i)
}

#[allow(dead_code)]
fn split(expr: &mut Vec<Value>) -> Option<usize> {
    let mut idx = -1;
    for (i, v) in expr.iter().enumerate() {
        if v.value >= 10 {
            idx = i as i32;
            break;
        }
    }

    if idx < 0 {
        return None;
    }
    let idx = idx as usize;

    let (d, v) = {
        let t = expr.get(idx)?;
        (t.depth, t.value)
    };

    expr[idx].depth = d + 1;
    expr[idx].value = (v as f32 / 2_f32).floor() as u32;

    expr.insert(
        idx + 1,
        Value {
            depth: d + 1,
            value: (v as f32 / 2_f32).ceil() as u32,
        },
    );

    Some(idx)
}

#[allow(dead_code)]
fn print_expr(expr: &[Value]) {
    print!("( ");
    for v in expr {
        print!("{:2}  ", v.value);
    }
    println!(")");
    print!("  ");
    for v in expr {
        print!("{:2}  ", v.depth);
    }
    println!();
}

#[allow(dead_code)]
fn add_exprs(expr1: &[Value], expr2: &[Value]) -> Vec<Value> {
    let mut expr = expr1.iter().copied().collect::<Vec<_>>();
    expr.append(&mut expr2.iter().copied().collect::<Vec<_>>());

    for v in expr.iter_mut() {
        v.depth += 1;
    }

    expr
}

#[allow(dead_code)]
fn reduce(expr: &mut Vec<Value>) {
    loop {
        let exploded = explode(expr);
        let splitted = if exploded.is_none() {
            split(expr)
        } else {
            None
        };

        if exploded.is_none() && splitted.is_none() {
            break;
        }
    }
}

#[allow(dead_code)]
fn magnitude(expr: &[Value]) -> u32 {
    let mut tmp = expr.iter().copied().collect::<Vec<_>>();
    while tmp.len() > 1 {
        let mut cur = 0;
        for i in 0..tmp.len() - 1 {
            if tmp[i].depth == tmp[i + 1].depth {
                cur = i;
                break;
            }
        }

        let rval = tmp[cur + 1].value;
        tmp.remove(cur + 1);

        let l = &mut tmp[cur];

        l.depth -= 1;
        l.value = l.value * 3 + rval * 2;
    }

    tmp.first().unwrap().value
}

#[allow(dead_code)]
fn possible_max_add(exprs: &[Vec<Value>]) -> (u32, (usize, usize)) {
    let mut result = BinaryHeap::new();

    for i in 0..exprs.len() {
        for j in 0..exprs.len() {
            let cur = exprs[i].iter().copied().collect::<Vec<_>>();
            let mut new_expr = add_exprs(&cur, &exprs[j]);
            reduce(&mut new_expr);
            result.push((magnitude(&new_expr), (i, j)));
        }
    }

    result.pop().unwrap()
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_read_input() {
        let v = read_input("../inputs/day18_test.txt").unwrap();

        print_expr(v.first().unwrap());
    }

    #[test]
    fn test_explode() {
        let v = read_input("../inputs/day18_test.txt").unwrap();

        let mut new_expr = add_exprs(&v[0], &v[1]);
        reduce(&mut new_expr);

        print_expr(&new_expr);
    }

    #[test]
    fn test_part1() {
        let v = read_input("../inputs/day18_test.txt").unwrap();

        let mut iter = v.iter();

        let mut cur = iter.next().unwrap().iter().copied().collect::<Vec<_>>();

        for expr in iter {
            let mut new_expr = add_exprs(&cur, expr);
            reduce(&mut new_expr);
            cur = new_expr;
        }

        print_expr(&cur);

        println!("Magnitude {}", magnitude(&cur));
    }

    #[test]
    fn do_part1() {
        let v = read_input("../inputs/day18.txt").unwrap();

        let mut iter = v.iter();

        let mut cur = iter.next().unwrap().iter().copied().collect::<Vec<_>>();

        for expr in iter {
            let mut new_expr = add_exprs(&cur, expr);
            reduce(&mut new_expr);
            cur = new_expr;
        }

        print_expr(&cur);

        println!("Magnitude {}", magnitude(&cur));
    }

    #[test]
    fn test_part2() {
        let v = read_input("../inputs/day18_test.txt").unwrap();

        let (m, (i, j)) = possible_max_add(&v);

        assert_eq!(i, 8);
        assert_eq!(j, 0);
        assert_eq!(m, 3993);
    }

    #[test]
    fn do_part2() {
        let v = read_input("../inputs/day18.txt").unwrap();

        let (m, (i, j)) = possible_max_add(&v);

        print_expr(&v[i]);
        print_expr(&v[j]);
        println!("Magnitude {}", m);
    }
}
