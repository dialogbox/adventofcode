use std::{collections::VecDeque, fmt::Display};

use super::input_lines;

const BINGO_BOARD_COLS: usize = 5;
const BINGO_BOARD_ROWS: usize = 5;

#[derive(Clone)]
pub struct BingoBoard {
    board: [[u16; BINGO_BOARD_ROWS]; BINGO_BOARD_COLS],
    checked: [[bool; BINGO_BOARD_ROWS]; BINGO_BOARD_COLS],
}

impl BingoBoard {
    // It assumes the input has proper format.
    // it doesn't check size of input or panic.
    fn from_input(input: &[String]) -> BingoBoard {
        let mut result = BingoBoard {
            board: [[0; BINGO_BOARD_ROWS]; BINGO_BOARD_COLS],
            checked: [[false; BINGO_BOARD_ROWS]; BINGO_BOARD_COLS],
        };

        for i in 0..BINGO_BOARD_ROWS {
            for (j, n) in input[i].split_whitespace().enumerate() {
                result.board[i][j] = n.parse::<u16>().unwrap()
            }
        }

        result
    }

    fn mark_draw(&mut self, draw: u16) {
        for i in 0..BINGO_BOARD_ROWS {
            for j in 0..BINGO_BOARD_COLS {
                if self.board[i][j] == draw {
                    self.checked[i][j] = true;
                    return;
                }
            }
        }
    }

    fn check_win(&self) -> bool {
        // Check horizontal
        'outerh: for i in 0..BINGO_BOARD_ROWS {
            for j in 0..BINGO_BOARD_COLS {
                if !self.checked[i][j] {
                    continue 'outerh;
                }
            }
            return true;
        }

        // Check vertical
        'outerv: for j in 0..BINGO_BOARD_COLS {
            for i in 0..BINGO_BOARD_ROWS {
                if !self.checked[i][j] {
                    continue 'outerv;
                }
            }
            return true;
        }
        false
    }

    #[allow(dead_code)]
    pub fn score(&self, last_draw: u16) -> u32 {
        let mut sum: u32 = 0;
        for i in 0..BINGO_BOARD_ROWS {
            for j in 0..BINGO_BOARD_COLS {
                if !self.checked[i][j] {
                    sum += self.board[i][j] as u32;
                }
            }
        }

        sum * last_draw as u32
    }
}

impl Display for BingoBoard {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.pad("{\n").unwrap();
        for i in 0..BINGO_BOARD_ROWS {
            f.pad("[").unwrap();

            if self.checked[i][0] {
                f.pad("*").unwrap();
            }
            f.write_fmt(format_args!("{}", self.board[i][0])).unwrap();

            for j in 1..BINGO_BOARD_COLS {
                f.pad("\t").unwrap();
                if self.checked[i][j] {
                    f.pad("*").unwrap();
                }
                f.write_fmt(format_args!("{}", self.board[i][j])).unwrap();
            }
            f.pad("]\n").unwrap();
        }
        f.pad("}\n").unwrap();

        Ok(())
    }
}

#[allow(dead_code)]
pub struct BingoGame {
    draws: VecDeque<u16>,
    drawn: Vec<u16>,
    boards: Vec<BingoBoard>,
}

impl BingoGame {
    #[allow(dead_code)]
    pub fn from_input_file(filename: &str) -> std::io::Result<BingoGame> {
        let mut lines = input_lines(filename)?;

        let draws = lines
            .next()
            .unwrap()
            .unwrap()
            .split(",")
            .map(|n_str| n_str.parse::<u16>().unwrap())
            .collect::<VecDeque<_>>();

        let mut result = BingoGame {
            draws,
            drawn: Vec::new(),
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

    fn step(&mut self, next_draw: u16) -> Option<usize> {
        // let next_draw = self.draws.pop_front().unwrap();
        self.drawn.push(next_draw);

        for (i, g) in self.boards.iter_mut().enumerate() {
            g.mark_draw(next_draw);
            if g.check_win() {
                return Some(i);
            }
        }

        None
    }

    #[allow(dead_code)]
    pub fn do_game(&mut self) -> Option<(u16, &BingoBoard)> {
        let mut winner: Option<usize> = None;
        let mut last_draw: u16 = 0;
        for i in 0..self.draws.len() {
            last_draw = self.draws[i];
            winner = self.step(last_draw);
            if winner.is_some() {
                break;
            }
        }

        winner.map(|idx| (last_draw, &self.boards[idx]))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_game() {
        let game = BingoGame::from_input_file("inputs/day4.txt").unwrap();

        println!("{:?}", game.draws);
        println!("{:?}", game.drawn);
        for b in game.boards {
            println!("{}", b);
            println!("");
        }
    }

    #[test]
    fn test_do_game() {
        let mut game = BingoGame::from_input_file("inputs/day4.txt").unwrap();

        let winner = game.do_game().unwrap();

        println!("{}", winner.1);
        println!("{}", winner.1.score(winner.0));
    }

    #[test]
    fn test_check_win1() {
        let board = BingoBoard {
            board: [[0; 5]; 5],
            checked: [
                [false, false, false, false, false],
                [false, false, false, false, false],
                [true, true, true, true, true],
                [false, false, false, false, false],
                [false, false, false, false, false],
            ],
        };
        assert!(board.check_win());
    }

    #[test]
    fn test_check_win2() {
        let board = BingoBoard {
            board: [[0; 5]; 5],
            checked: [
                [false, true, false, false, false],
                [false, true, false, false, false],
                [false, true, false, false, false],
                [false, true, false, false, false],
                [false, true, false, false, false],
            ],
        };
        assert!(board.check_win());
    }

    #[test]
    fn test_check_lose() {
        let board = BingoBoard {
            board: [[0; 5]; 5],
            checked: [
                [false, false, false, false, false],
                [false, false, true, false, false],
                [false, false, true, false, false],
                [false, false, true, false, false],
                [false, false, true, false, false],
            ],
        };
        assert!(!board.check_win());
    }
}
