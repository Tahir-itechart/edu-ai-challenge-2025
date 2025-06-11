import { BOARD_SIZE, CELL_STATE, SHIP_LENGTH, NUM_SHIPS } from './constants.js';
import { Ship } from './ship.js';

export class Board {
    constructor(isPlayerBoard = false) {
        this.grid = this.createGrid();
        this.ships = [];
        this.isPlayerBoard = isPlayerBoard;
    }

    createGrid() {
        return Array.from({ length: BOARD_SIZE }, () =>
            new Array(BOARD_SIZE).fill(CELL_STATE.UNKNOWN)
        );
    }

    placeShipsRandomly() {
        let placedShips = 0;
        while (placedShips < NUM_SHIPS) {
            const orientation = Math.random() < 0.5 ? 'horizontal' : 'vertical';
            let startRow, startCol;

            if (orientation === 'horizontal') {
                startRow = Math.floor(Math.random() * BOARD_SIZE);
                startCol = Math.floor(Math.random() * (BOARD_SIZE - SHIP_LENGTH + 1));
            } else {
                startRow = Math.floor(Math.random() * (BOARD_SIZE - SHIP_LENGTH + 1));
                startCol = Math.floor(Math.random() * BOARD_SIZE);
            }

            if (this.canPlaceShip(startRow, startCol, orientation)) {
                const locations = [];
                for (let i = 0; i < SHIP_LENGTH; i++) {
                    let row = startRow;
                    let col = startCol;
                    if (orientation === 'horizontal') {
                        col += i;
                    } else {
                        row += i;
                    }
                    locations.push(`${row}${col}`);
                    if (this.isPlayerBoard) {
                        this.grid[row][col] = CELL_STATE.SHIP;
                    }
                }
                this.ships.push(new Ship(locations));
                placedShips++;
            }
        }
    }

    canPlaceShip(startRow, startCol, orientation) {
        for (let i = 0; i < SHIP_LENGTH; i++) {
            let row = startRow;
            let col = startCol;
            if (orientation === 'horizontal') {
                col += i;
            } else {
                row += i;
            }
            if (this.grid[row][col] !== CELL_STATE.UNKNOWN) {
                return false; // Collision with another ship
            }
        }
        return true;
    }

    receiveGuess(guess) {
        const [row, col] = guess.split('').map(Number);
        
        for (const ship of this.ships) {
            if (ship.locations.includes(guess)) {
                ship.recordHit(guess);
                this.grid[row][col] = CELL_STATE.HIT;
                if (ship.isSunk()) {
                    return 'sunk';
                }
                return 'hit';
            }
        }

        this.grid[row][col] = CELL_STATE.MISS;
        return 'miss';
    }

    allShipsSunk() {
        return this.ships.every(ship => ship.isSunk());
    }
} 