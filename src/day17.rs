use std::cmp::{max, Ordering};

#[allow(dead_code)]
fn find_style_launch(x_range: (i32, i32), y_range: (i32, i32)) -> Option<(i32, i32)> {
    let mut x = 0;
    let mut x_valo = 0;
    while x <= x_range.1 {
        if x + x_valo >= x_range.0 && x + x_valo <= x_range.1 {
            break;
        }
        x += x_valo;
        x_valo += 1;
    }

    let mut max_y_valo = 0;

    // brute force
    for i in x_valo..200 {
        let mut y = 0;
        let mut y_valo = i;
        while y >= y_range.0 {
            if y + y_valo >= y_range.0 && y + y_valo <= y_range.1 {
                max_y_valo = max(max_y_valo, i);
                break;
            }
            y += y_valo;
            y_valo -= 1;
        }
    }

    Some((x_valo, max_y_valo))
}

#[allow(dead_code)]
fn launch(val: (i32, i32), x_range: (i32, i32), y_range: (i32, i32)) {
    let (mut xval, mut yval) = val;

    let mut x = 0;
    let mut y = 0;

    while !(x >= x_range.0 && x <= x_range.1 && y >= y_range.0 && y <= y_range.1) {
        println!("({}, {})", x, y);
        if x > x_range.1 || y < y_range.1 {
            println!("We missed the target");
            break;
        }
        x += xval;
        y += yval;

        match xval.cmp(&0) {
            Ordering::Greater => xval -= 1,
            Ordering::Equal => (),
            Ordering::Less => xval += 1,
        }

        yval -= 1;
    }
    println!("Final ({}, {})", x, y);
}

#[allow(dead_code)]
fn test_launch(val: &(i32, i32), x_range: &(i32, i32), y_range: &(i32, i32)) -> bool {
    let (mut xval, mut yval) = val;

    let mut x = 0;
    let mut y = 0;

    while !(x >= x_range.0 && x <= x_range.1 && y >= y_range.0 && y <= y_range.1) {
        if x > x_range.1 || y < y_range.0 {
            return false;
        }
        x += xval;
        y += yval;

        match xval.cmp(&0) {
            Ordering::Greater => xval -= 1,
            Ordering::Equal => (),
            Ordering::Less => xval += 1,
        }

        yval -= 1;
    }
    true
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_something() {
        println!("{:b}", 10);
    }

    #[test]
    fn test_part1() {
        let range = ((20, 30), (-10, -5));

        let result = find_style_launch(range.0, range.1);
        launch((6, 0), range.0, range.1);

        println!("{:?}", result);
    }

    #[test]
    fn do_part1() {
        let range = ((209, 238), (-86, -59));

        let result = find_style_launch(range.0, range.1);

        println!("{:?}", result);
        launch(result.unwrap(), range.0, range.1);
    }

    #[test]
    fn test_part2() {
        let range = ((20, 30), (-10, -5));

        let mut result = Vec::new();
        for x in 0..100 {
            for y in -100..200 {
                if test_launch(&(x, y), &range.0, &range.1) {
                    result.push((x, y));
                }
            }
        }

        println!("{}", result.len());
    }

    #[test]
    fn do_part2() {
        let range = ((209, 238), (-86, -59));

        let mut result = Vec::new();
        for x in 0..1000 {
            for y in -87..2000 {
                if test_launch(&(x, y), &range.0, &range.1) {
                    result.push((x, y));
                }
            }
        }

        println!("{}", result.len());
    }
}
