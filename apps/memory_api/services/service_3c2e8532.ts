import api from '@/lib/api';
import { ModalInstance, NotificationService } from '@/services'; // Assuming these types and services exist

class MarginEditor {
    editMarginBegin(margin: any) {
        const modal = new ModalInstance({
            templateUrl: 'src/printshop/templates/modalboxes/edit-margin.html',
            controller: async ($scope: any, $modalInstance: any) => {
                try {
                    $scope.marginForm = _.clone(margin);
                    $scope.save = async () => {
                        const data = await api.put(`/margins/${margin.ID}`, $scope.marginForm);
                        if (data.response) {
                            NotificationService.success('success');
                            $modalInstance.close();
                            loadMargins(); // Assuming this function is defined elsewhere
                        } else {
                            NotificationService.error('error');
                        }
                    };
                } catch (error) {
                    NotificationService.error('error');
                }
            }
        });

        modal.open();
    }
}

// Usage Example:
const marginEditor = new MarginEditor();
marginEditor.editMarginBegin({ ID: 1, /* other properties */ });