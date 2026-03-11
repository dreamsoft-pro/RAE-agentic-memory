javascript
import { formatSizeUnits } from '@/lib/api';

export function formatSizeUnits(file) {
    return MainWidgetService.formatSizeUnits(file.size);
}

function getMessages(scope, reclamationID) {
    ReclamationService.getMessages(reclamationID).then(data => {
        scope.messages = data;
    });
}

export function messages(reclamation) {
    TemplateRootService.getTemplateUrl(101).then(response => {
        const modalScope = angular.extend({}, $scope.$root.$childTail, {});
        $modal.open({
            templateUrl: response.url,
            scope: modalScope,
            size: 'lg',
            controller: function ($scope) {
                $scope.reclamation = reclamation;
                $scope.messages = [];

                socket.emit('onReclamation', { reclamationID: reclamation.ID });

                reclamation.unreadMessages = 0;

                getMessages($scope, reclamation.ID);
            }
        });
    });
}
