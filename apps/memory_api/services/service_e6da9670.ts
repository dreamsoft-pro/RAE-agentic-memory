import api from '@/lib/api';

async function ensureNumber(value: string | number): Promise<number> {
    if (typeof value === 'string') {
        const num = parseInt(value, 10);
        if (!isNaN(num)) {
            return num;
        }
    } else if (typeof value === 'number') {
        return value;
    }
    throw new Error('Invalid number');
}

async function getVolumes(product: any, amount: number): Promise<void> {
    try {
        const response = await api.getVolumes({ product, amount });
        // Handle the response as needed
    } catch (error) {
        console.error('Error fetching volumes:', error);
    }
}

function filterRelatedFormats(): void {
    if (!$scope.productItem.amount) {
        $scope.productItem.amount = 1;
    }

    const formattedAmount = ensureNumber($scope.productItem.amount);

    if (formattedAmount < 1) {
        formattedAmount = 1;
    }

    getVolumes(product, formattedAmount);
}