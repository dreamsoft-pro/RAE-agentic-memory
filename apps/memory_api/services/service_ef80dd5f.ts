import axios from 'axios';
import { MutableRefObject } from 'react';

class CacheService {
    private cache: MutableRefObject<any>;

    constructor(cache: MutableRefObject<any>) {
        this.cache = cache;
    }

    removeAll(): void {
        this.cache.current.removeAll();
    }
}

export default CacheService;