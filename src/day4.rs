use std::fmt::Display;

use super::input_lines;

struct BingoBoard {
    board: [[u8; 5]; 5],
}

impl BingoBoard {
    // It assumes the input has proper format.
    // it doesn't check size of input or panic.
    fn from_input(input: &[String]) -> BingoBoard {
        let mut result = BingoBoard { board: [[0; 5]; 5] };

        for i in 0..5 {
            for (j, n) in input[i].split_whitespace().enumerate() {
                result.board[i][j] = n.parse::<u8>().unwrap()
            }
        }

        result
    }
}

impl Display for BingoBoard {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.pad("{\n").unwrap();
        for i in 0..self.board.len() {
            f.write_fmt(format_args!("{:?}\n", self.board[i])).unwrap();
        }
        f.pad("}\n").unwrap();

        Ok(())
    }
}

#[allow(dead_code)]
pub struct BingoGame {
    drawn: Vec<u8>,
    boards: Vec<BingoBoard>,
}

impl BingoGame {
    #[allow(dead_code)]
    pub fn from_input_file(filename: &str) -> std::io::Result<BingoGame> {
        let mut lines = input_lines(filename)?;

        let drawn = lines
            .next()
            .unwrap()
            .unwrap()
            .split(",")
            .map(|n_str| n_str.parse::<u8>().unwrap())
            .collect::<Vec<_>>();

        let mut result = BingoGame {
            drawn,
            boards: Vec::new(),
        };

        while lines.next().is_some() {
            let board_data = vec![
                lines.next().unwrap().unwrap(),
                lines.next().unwrap().unwrap(),
                lines.next().unwrap().unwrap(),
                lines.next().unwrap().unwrap(),
                lines.next().unwrap().unwrap(),
            ];

            if board_data.len() != 5 {
                println!("Malformed input {:?}", board_data);
                break;
            }
            result.boards.push(BingoBoard::from_input(&board_data));
        }

        Ok(result)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_game() {
        let game = BingoGame::from_input_file("inputs/day4.txt").unwrap();

        println!("{:?}", game.drawn);
        for b in game.boards {
            println!("{}", b);
            println!("");
        }
    }
}
