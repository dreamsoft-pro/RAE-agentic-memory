
import { BACKEND_ADVICE } from '@lib/api';
import { EditorProjectService, Notification } from '@services';
import { translateFilter } from '@filters';

@BACKEND_ADVICE('send')
export class SharedProjectCtrl {
    projectId: string;
    source: string;

    constructor(private $scope: any, private $stateParams: any) {
        this.projectId = $stateParams.projectid;
        this.source = $stateParams.source;
    }

    send() {
        EditorProjectService.shareMyProject(this.$scope.form.email, this.projectId).then(
            (data: any) => Notification.success(translateFilter('success'))
        );
    }

    sendFb() {
