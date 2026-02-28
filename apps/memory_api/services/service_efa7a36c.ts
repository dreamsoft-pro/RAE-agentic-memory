import api from '@/lib/api';

interface Category {
    langs: string[];
}

async function processCategories(): Promise<void> {
    let result: Category[] = [];

    // Fetch categories or perform operations similar to your existing logic
    try {
        const response = await api.get('/some-endpoint'); // Adjust the endpoint based on your API setup
        const data = response.data;

        for (const chCat of data.categories) {  // Assuming 'categories' is an array in your fetched JSON
            result.push(chCat);
        }

        let gIndex: number; // Define index or any other variable you need

        if (!Array.isArray($scope.types[gIndex].categories)) {
            $scope.types[gIndex].categories = [];
        }
        
        $scope.types[gIndex].categories = result.map(category => category.langs);

        // Assuming modalInstance.dismiss is a function defined in your component context
        $modalInstance.dismiss('cancel');

        Notification.success($filter('translate')('success'));  // Adjust this according to your notification setup

    } catch (error) {
        Notification.error($filter('translate')('error'));
    }
}

// Example usage of the above function within a Next.js Component:
export default class MyComponent extends React.Component {
    componentDidMount() {
        processCategories();
    }

    render() {
        return <div>My Component</div>;
    }
}