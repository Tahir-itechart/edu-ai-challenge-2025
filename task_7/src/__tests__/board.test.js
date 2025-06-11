import { Board } from '../board.js';
import { NUM_SHIPS, CELL_STATE } from '../constants.js';
import { Ship } from '../ship.js';

describe('Board', () => {
    let board;

    beforeEach(() => {
        board = new Board();
    });

    test('should create a grid of the correct size', () => {
        expect(board.grid.length).toBe(10);
        expect(board.grid[0].length).toBe(10);
        expect(board.grid[0][0]).toBe(CELL_STATE.UNKNOWN);
    });

    test('placeShipsRandomly() should place the correct number of ships', () => {
        board.placeShipsRandomly();
        expect(board.ships.length).toBe(NUM_SHIPS);
    });

    test('receiveGuess should return "miss" for an empty cell', () => {
        const result = board.receiveGuess('55');
        expect(result).toBe('miss');
        expect(board.grid[5][5]).toBe(CELL_STATE.MISS);
    });

    test('receiveGuess should return "hit" when hitting a ship', () => {
        const ship = new Ship(['11', '12', '13']);
        board.ships.push(ship);

        const result = board.receiveGuess('12');
        expect(result).toBe('hit');
        expect(board.grid[1][2]).toBe(CELL_STATE.HIT);
    });

    test('receiveGuess should return "sunk" when the last part of a ship is hit', () => {
        const ship = new Ship(['21', '22']);
        board.ships.push(ship);
        
        board.receiveGuess('21');
        const result = board.receiveGuess('22');
        
        expect(result).toBe('sunk');
        expect(board.grid[2][2]).toBe(CELL_STATE.HIT);
    });

    test('allShipsSunk() should return true when all ships are sunk', () => {
        board.placeShipsRandomly();
        for (const ship of board.ships) {
            for (const loc of ship.locations) {
                ship.recordHit(loc);
            }
        }
        expect(board.allShipsSunk()).toBe(true);
    });

    test('allShipsSunk() should return false when some ships are not sunk', () => {
        board.placeShipsRandomly();
        // sink all but one ship
        for (let i = 0; i < board.ships.length - 1; i++) {
            const ship = board.ships[i];
            for (const loc of ship.locations) {
                ship.recordHit(loc);
            }
        }
        expect(board.allShipsSunk()).toBe(false);
    });
}); 