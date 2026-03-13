angular.module('digitalprint.app')
    .controller('MainCtrl', function ($rootScope, $scope, $translate, $state, AuthService,
                                      LangService, $breadcrumb, LoadingService, ReclamationService, socket,
                                      OrderMessageService) {

        $rootScope.breadcrumb = $breadcrumb;

        $rootScope._ = _;
        $rootScope.LoadingService = LoadingService;

        $scope.navBarCollapse = 'superadmin';


        setTimeout(function () {
            jQuery(function () {
                Metronic.init();
                Layout.init();
                QuickSidebar.init();
            });
        }, 1000);

        $scope.countUnreadedMessages = 0;

        ReclamationService.countMessages().then(function (data) {
            $scope.countUnreadedMessages = data.count;
        });

        socket.emit('onReclamationsAdminPanel', {'admin': true});

        socket.on('newMessage', function (newMessage) {
            $scope.countUnreadedMessages++;
        });

        $rootScope.$on('Reclamations:unreadMessages', function (count) {
            $scope.countUnreadedMessages = 0;
        });

        $scope.countOrderUnreadedMessages = 0;

        OrderMessageService.countMessages().then(function (data) {
            $scope.countOrderUnreadedMessages = data.count;
        });

        socket.emit('onOrdersAdminPanel', {'admin': true});

        socket.on('order.newMessage', function (newMessage) {
            $scope.countOrderUnreadedMessages++;
        });

        $rootScope.$on('Orders:unreadMessages', function (count) {
            $scope.countOrderUnreadedMessages = 0;
        });

    });
