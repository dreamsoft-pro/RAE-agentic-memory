import { useEffect, useState } from 'react';
import axios from 'axios';

export class LoadingService {

    private static instance?: LoadingService;
    private loadingCount = 0;
    private errorCount = 0;

    private constructor() {}

    public static getInstance(): LoadingService {
        if (!LoadingService.instance) {
            LoadingService.instance = new LoadingService();
        }
        return LoadingService.instance;
    }

    isLoading(): boolean {
        return this.loadingCount > 0;
    }

    requested(): void {
        this.loadingCount++;
    }

    responsed(status: number): void {
        if (status !== 200 && status !== 401) {
            this.errorCount++;
        }
        this.loadingCount--;
    }

    countError(): void {
        this.errorCount++;
    }

    count(): number {
        return this.loadingCount;
    }

    errorCount(): number {
        return this.errorCount;
    }
}