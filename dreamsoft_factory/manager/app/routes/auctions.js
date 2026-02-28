angular.module('digitalprint.routes')
    .config(function ($stateProvider) {

        var auctions = {};

        auctions.base = {
            parent: 'base',
            name: 'auctions-base',
            url: '/auctions',
            ncyBreadcrumb: {
                label: '{{ "inquiries" | translate }}'
            }
        };

        auctions.index = {
            parent: 'auctions-base',
            name: 'auctions-offer-list',
            url: '/offer-list',
            views: {
                'content@base': {
                    templateUrl: 'src/auctions/templates/offer-list.html',
                    controller: 'auctions.OfferListCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "inquiry_list" | translate }}'
            }
        };

        auctions.currentAuctions = {
            parent: 'auctions-base',
            name: 'current-auctions',
            url: '/current-auctions',
            views: {
                'content@base': {
                    templateUrl: 'src/auctions/templates/current-auctions.html',
                    controller: 'auctions.CurrentAuctionsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "current_inquiries" | translate }}'
            }
        };

        _.each(auctions, function (route) {
            $stateProvider.state(route);
        });

    });