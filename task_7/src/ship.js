export class Ship {
    constructor(locations) {
        this.locations = locations;
        this.hits = new Array(locations.length).fill(false);
    }

    isSunk() {
        return this.hits.every(h => h);
    }

    recordHit(location) {
        const index = this.locations.indexOf(location);
        if (index !== -1) {
            this.hits[index] = true;
            return true;
        }
        return false;
    }
} 