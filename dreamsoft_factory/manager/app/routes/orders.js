angular.module('digitalprint.routes')
    .config(function ($stateProvider) {

        var orders = {};

        orders.base = {
            parent: 'base',
            name: 'orders-base',
            url: '/orders',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/orders-summary.html',
                    controller: 'orders.OrdersSummaryCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "orders" | translate }}'
            }
        };

        orders.carts = {
            parent: 'orders-base',
            name: 'orders-carts',
            url: '/carts/:cartID',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/carts.html',
                    controller: 'orders.CartsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "carts" | translate }}'
            }
        };

        orders.orders = {
            parent: 'orders-base',
            name: 'orders-orders',
            url: '/orders/:orderID',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/orders.html',
                    controller: 'orders.DpOrdersCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "orders" | translate }}'
            }
        };

        orders.products = {
            parent: 'orders-base',
            name: 'orders-products',
            url: '/products/:productID',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/products.html',
                    controller: 'orders.ProductsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "products" | translate }}'
            }
        };

        orders.productsProductionDetails = {
            parent: 'orders-base',
            name: 'products-procudtion-details',
            url: '/:productID/productProductionDetails',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/products-production-details.html',
                    controller: 'orders.ProductsProductionDetailsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{"product_production_details" | translate}}'
            }
        };

        orders.productionPath = {
            parent: 'orders-base',
            name: 'orders-production-path',
            url: '/productionPath/:deviceID',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-path.html',
                    controller: 'orders.OngoingsCtrl' // device ongoings
                }
            },
            ncyBreadcrumb: {
                label: '{{ "production_path" | translate }}'
            }
        };
		
        orders.productionPanel = {
            parent: 'orders-base',
            name: 'orders-production-panel',
            url: '/productionPanel/:orderID',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-panel.html',
                    controller: 'orders.OrderOngoingsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "production_panel" | translate }}'
            }
        };

        orders.operators = {
            parent: 'orders-base',
            name: 'orders-operators',
            url: '/operators/:operatorID',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/operators.html',
                    controller: 'orders.OperatorsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "operators" | translate }}'
            }
        };

        orders.productsAccept = {
            parent: 'orders-base',
            name: 'orders-products-accept',
            url: '/productsAccept/:productID',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/products-accept.html',
                    controller: 'orders.ProductsAcceptCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "orders_acceptance" | translate }}'
            }
        };

        orders.auctionsList = {
            parent: 'orders-base',
            name: 'orders-auctions-list',
            url: '/auctions-list',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/auctions-list.html',
                    controller: 'orders.AuctionsListCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "inquiry_list" | translate }}'
            }
        };

        orders.statuses = {
            parent: 'orders-base',
            name: 'orders-statuses',
            url: '/statuses',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/statuses.html',
                    controller: 'orders.StatusesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "statuses" | translate }}'
            }
        };

        orders.reclamations_statuses = {
            parent: 'orders-base',
            name: 'reclamations-statuses',
            url: '/reclamations-statuses',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/reclamations-statuses.html',
                    controller: 'orders.ReclamationsStatusesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "reclamation_statuses" | translate }}'
            }
        };

        orders.transport = {
            parent: 'orders-base',
            name: 'orders-transport',
            url: '/transport',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/transport.html',
                    controller: 'orders.TransportCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "transport" | translate }}'
            }
        };

        orders.orders_custom_products = {
            parent: 'orders-base',
            name: 'orders-custom-products',
            url: '/custom-products/:customProductID',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/custom-products.html',
                    controller: 'orders.CustomProductsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "custom_orders" | translate }}'
            }
        };

        _.each(orders, function (route) {
            $stateProvider.state(route);
        });

    });