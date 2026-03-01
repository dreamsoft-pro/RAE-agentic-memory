javascript
import { Api } from '@/lib/api';

angular.module('digitalprint.services')
    .factory('LoadingService', function () {

        let loadingCount = 0;
        let errorCount = 0;

        const isLoading = (): boolean => {
            return loadingCount > 0;
        };

        // [BACKEND_ADVICE] Heavy logic for request handling.
        const requested = (): void => {
            loadingCount++;
        };

        const responsed = (status: number): void => {
            if (status !== 200 && status !== 401) {
                errorCount++;
            }
            loadingCount--;
        };

        // [BACKEND_ADVICE] Increment error count.
        const countError = (): void => {
            errorCount++;
        };

        const count = (): number => {
            return loadingCount;
        };

        const errorCount = (): number => {
            return errorCount;
        };

        return {
            isLoading,
            requested,
            responsed,
            countError,
            count,
            errorCount
        };
    });
