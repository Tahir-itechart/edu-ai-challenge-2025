import { BOARD_SIZE } from './constants.js';

class Player {
    constructor(name) {
        this.name = name;
        this.guesses = new Set();
    }
}

export class HumanPlayer extends Player {
    constructor() {
        super('Player');
    }
}

export class CPUPlayer extends Player {
    constructor() {
        super('CPU');
        this.mode = 'hunt'; // 'hunt' or 'target'
        this.targetQueue = [];
        this.lastHit = null;
    }

    generateGuess() {
        let guess;
        if (this.mode === 'target' && this.targetQueue.length > 0) {
            guess = this.targetQueue.shift();
            // If the queue is now empty, we might not have sunk the ship, but have no more leads
            if (this.targetQueue.length === 0) {
                this.mode = 'hunt';
            }
        } else {
            this.mode = 'hunt'; // Reset to hunt mode if queue is empty
            guess = this.generateRandomGuess();
        }
        this.guesses.add(guess);
        return guess;
    }

    generateRandomGuess() {
        let row, col, guess;
        do {
            row = Math.floor(Math.random() * BOARD_SIZE);
            col = Math.floor(Math.random() * BOARD_SIZE);
            guess = `${row}${col}`;
        } while (this.guesses.has(guess));
        return guess;
    }

    updateAfterHit(guess, wasSunk) {
        if (wasSunk) {
            this.mode = 'hunt';
            this.targetQueue = [];
            this.lastHit = null;
        } else {
            this.mode = 'target';
            this.lastHit = guess;
            this.populateTargetQueue(guess);
        }
    }

    populateTargetQueue(guess) {
        const [row, col] = guess.split('').map(Number);
        const adjacent = [
            { r: row - 1, c: col },
            { r: row + 1, c: col },
            { r: row, c: col - 1 },
            { r: row, c: col + 1 },
        ];

        for (const { r, c } of adjacent) {
            if (r >= 0 && r < BOARD_SIZE && c >= 0 && c < BOARD_SIZE) {
                const newGuess = `${r}${c}`;
                if (!this.guesses.has(newGuess) && !this.targetQueue.includes(newGuess)) {
                    this.targetQueue.push(newGuess);
                }
            }
        }
    }
} 