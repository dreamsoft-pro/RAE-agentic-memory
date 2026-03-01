javascript
import { api } from '@/lib/api';

const timeHandler = setTimeout(() => {
    if ($scope.menuItems !== undefined) {
        def.resolve($scope.menuItems);
        clearTimeout(timeHandler);
    }
}, 1000);

return def.promise;

function getGroups() {
    const def = $q.defer();

    api.get('/categories/groups').then(data => {
        def.resolve(data);
    });

    return def.promise;
}

init();
