use std::fmt::Display;

use super::input_lines;

#[allow(dead_code)]
fn read_input(filename: &str) -> std::io::Result<Vec<bool>> {
    let mut lines = input_lines(filename)?;

    let l = lines.next().unwrap()?;

    let digits = l
        .chars()
        .map(|c| match c {
            '0' => [false, false, false, false],
            '1' => [false, false, false, true],
            '2' => [false, false, true, false],
            '3' => [false, false, true, true],
            '4' => [false, true, false, false],
            '5' => [false, true, false, true],
            '6' => [false, true, true, false],
            '7' => [false, true, true, true],
            '8' => [true, false, false, false],
            '9' => [true, false, false, true],
            'A' => [true, false, true, false],
            'B' => [true, false, true, true],
            'C' => [true, true, false, false],
            'D' => [true, true, false, true],
            'E' => [true, true, true, false],
            'F' => [true, true, true, true],
            _ => panic!("Huh??"),
        })
        .flatten()
        .collect::<Vec<bool>>();

    Ok(digits)
}

#[allow(dead_code)]
#[derive(Debug)]
enum Packet {
    Literal {
        version: u8,
        packet_type: u8,
        value: u64,
    },
    Op {
        version: u8,
        packet_type: u8,
        sub_packets: Vec<Packet>,
    },
}

impl Display for Packet {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Packet::Literal {
                version: _,
                packet_type: _,
                value,
            } => f.write_fmt(format_args!("{}", value)).unwrap(),
            Packet::Op {
                version: _,
                packet_type,
                sub_packets,
            } => {
                match packet_type {
                    0 => f.pad("+(").unwrap(),
                    1 => f.pad("*(").unwrap(),
                    2 => f.pad("min(").unwrap(),
                    3 => f.pad("max(").unwrap(),
                    5 => f.pad(">(").unwrap(),
                    6 => f.pad("<(").unwrap(),
                    7 => f.pad("=(").unwrap(),
                    _ => panic!("huh????"),
                }

                f.write_str(
                    &sub_packets
                        .iter()
                        .map(|p| p.to_string())
                        .collect::<Vec<String>>()
                        .join(", "),
                )
                .unwrap();

                f.pad(")").unwrap();
            }
        }

        Ok(())
    }
}

impl Packet {
    #[allow(dead_code)]
    fn total_version(self: &Packet) -> u32 {
        match self {
            Packet::Literal {
                version,
                packet_type: _,
                value: _,
            } => *version as u32,
            Packet::Op {
                version,
                packet_type: _,
                sub_packets,
            } => {
                let mut total = *version as u32;

                for p in sub_packets {
                    total += p.total_version();
                }

                total
            }
        }
    }

    #[allow(dead_code)]
    fn value(&self) -> u64 {
        match self {
            Packet::Literal {
                version: _,
                packet_type: _,
                value,
            } => *value as u64,
            Packet::Op {
                version: _,
                packet_type,
                sub_packets,
            } => {
                let subs = sub_packets.iter().map(|p| p.value()).collect::<Vec<u64>>();

                match packet_type {
                    0 => subs.iter().sum(),
                    1 => subs.iter().product(),
                    2 => *subs.iter().min().unwrap(),
                    3 => *subs.iter().max().unwrap(),
                    5 => {
                        if *subs.get(0).unwrap() > *subs.get(1).unwrap() {
                            1
                        } else {
                            0
                        }
                    }
                    6 => {
                        if *subs.get(0).unwrap() < *subs.get(1).unwrap() {
                            1
                        } else {
                            0
                        }
                    }
                    7 => {
                        if *subs.get(0).unwrap() == *subs.get(1).unwrap() {
                            1
                        } else {
                            0
                        }
                    }
                    _ => panic!("huh????"),
                }
            }
        }
    }
}

#[allow(dead_code)]
fn bitstream_to_num(bits: &[bool]) -> u32 {
    let mut result = 0;

    for &bit in bits {
        result <<= 1;
        if bit {
            result |= 0b0001;
        }
    }

    result
}

#[allow(dead_code)]
fn scan_packets(data: &[bool]) {
    let mut cur = 0;
    while let Some((nbits, _)) = scan_packet(&data[cur..]) {
        cur += nbits;

        let padding = 4 - (nbits % 4);
        // println!("Scan a root packet: {} bits", nbits);
        cur += padding;
        // println!("Cur: {}, Padding: {}", cur, padding);
    }
}

fn scan_packet(data: &[bool]) -> Option<(usize, Packet)> {
    if data.is_empty() {
        return None;
    }

    let mut cur = 0;

    let version = bitstream_to_num(&data[cur..cur + 3]) as u8;
    cur += 3;
    let packet_type = bitstream_to_num(&data[cur..cur + 3]) as u8;
    cur += 3;

    // println!("Version: {:b}, Type: {:b}", version, packet_type);

    if packet_type == 4 {
        let (nbits, v) = scan_literal_packet(&data[cur..]);
        cur += nbits;

        // println!("Literal Packet: {} bits , Value: {}", nbits, v);

        Some((
            cur,
            Packet::Literal {
                version,
                packet_type,
                value: v,
            },
        ))
    } else {
        let length_type = data[cur];
        cur += 1;

        let mut sub_packets = Vec::new();

        if length_type {
            let len = bitstream_to_num(&data[cur..cur + 11]) as usize;
            cur += 11;
            // println!("Mode 1 Operator Packet: {} packets", len);

            for _ in 0..len {
                let (nbits, p) = scan_packet(&data[cur..]).unwrap();
                cur += nbits;

                sub_packets.push(p);
            }
        } else {
            let mut len = bitstream_to_num(&data[cur..cur + 15]) as usize;
            cur += 15;
            // println!("Mode 0 Operator Packet: {} bits", len);

            while len > 0 {
                let (nbits, p) = scan_packet(&data[cur..]).unwrap();
                cur += nbits;
                len -= nbits;

                sub_packets.push(p);
            }
        }

        Some((
            cur,
            Packet::Op {
                version,
                packet_type,
                sub_packets,
            },
        ))
    }
}

fn scan_literal_packet(data: &[bool]) -> (usize, u64) {
    let mut result = 0;
    let mut cur = 0;

    loop {
        let is_last = data[cur];
        cur += 1;

        let v = bitstream_to_num(&data[cur..cur + 4]) as u64;
        cur += 4;

        result <<= 4;
        result |= v;

        if !is_last {
            break;
        }
    }

    (cur, result)
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_something() {
        println!("{:b}", 10);
    }

    #[test]
    fn test_read_input() {
        let map = read_input("inputs/day16_test.txt").unwrap();

        println!("{:?}", map);
    }

    #[test]
    fn test_part1() {
        let map = read_input("inputs/day16_test.txt").unwrap();

        let (_, p) = scan_packet(&map).unwrap();

        assert_eq!(p.total_version(), 31);
    }

    #[test]
    fn do_part1() {
        let map = read_input("inputs/day16.txt").unwrap();

        let (_, p) = scan_packet(&map).unwrap();

        assert_eq!(p.total_version(), 908);
    }

    #[test]
    fn test_part2() {
        let map = read_input("inputs/day16_test.txt").unwrap();

        let (_, p) = scan_packet(&map).unwrap();

        assert_eq!(p.value(), 54);
    }

    #[test]
    fn do_part2() {
        let map = read_input("inputs/day16.txt").unwrap();

        let (_, p) = scan_packet(&map).unwrap();

        assert_eq!(p.value(), 10626195124371);
    }
}
