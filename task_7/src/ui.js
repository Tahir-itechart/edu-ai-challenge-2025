import readline from 'readline';
import { BOARD_SIZE, CELL_STATE } from './constants.js';

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

export const printBoard = (playerBoard, opponentBoard) => {
    console.log('\\n   --- OPPONENT BOARD ---          --- YOUR BOARD ---');
    const header = '  ' + Array.from({ length: BOARD_SIZE }, (_, i) => i).join(' ');
    console.log(header + '     ' + header);

    for (let i = 0; i < BOARD_SIZE; i++) {
        let rowStr = `${i} `;
        // Opponent's board (player's view of it)
        rowStr += opponentBoard.grid[i].map(cell => cell === CELL_STATE.SHIP ? CELL_STATE.UNKNOWN : cell).join(' ');
        rowStr += `    ${i} `;
        // Player's own board
        rowStr += playerBoard.grid[i].join(' ');
        console.log(rowStr);
    }
    console.log('\\n');
};

export const getPlayerGuess = (guesses) => {
    return new Promise((resolve) => {
        const ask = () => {
            rl.question('Enter your guess (e.g., 00): ', (answer) => {
                const guess = answer.trim();
                if (!/^[0-9]{2}$/.test(guess)) {
                    console.log('Oops, input must be exactly two digits (e.g., 00, 34, 98).');
                    ask();
                } else if (guesses.has(guess)) {
                    console.log('You already guessed that location!');
                    ask();
                } else {
                    const [row, col] = guess.split('').map(Number);
                     if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) {
                        console.log(`Oops, please enter valid row and column numbers between 0 and ${BOARD_SIZE - 1}.`);
                        ask();
                    } else {
                        resolve(guess);
                    }
                }
            });
        };
        ask();
    });
};

export const printMessage = (message) => {
    console.log(message);
};

export const closeInterface = () => {
    rl.close();
}; 