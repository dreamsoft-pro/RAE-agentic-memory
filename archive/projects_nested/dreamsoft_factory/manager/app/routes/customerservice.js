angular.module('digitalprint.routes')
    .config(function ($stateProvider) {

        var customerservice = {};
		
		customerservice.production = {
            parent: 'base',
            name: 'prodcution-base',
            url: '/prodcution',
            ncyBreadcrumb: {
                label: "{{ 'prodcution' | translate }}"
            }
        };

        customerservice.prodcution_settings = {
            parent: 'prodcution-base',
            name: 'production-settings',
            url: '/production-settings',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-settings.html',
                    controller: 'orders.ProductionSettingsCtrl'
                },
                'shifts@production-settings': {
                    templateUrl: 'src/orders/templates/production-settings-shifts.html',
                    controller: 'orders.ShiftsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "settings" | translate }}'
            }
        };

        customerservice.prodcution_planning = {
            parent: 'prodcution-base',
            name: 'production-planning',
            url: '/production-planning',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-planned.html',
                    controller: 'orders.PlannedCtrl' // device planned
                }
            },
            ncyBreadcrumb: {
                label: '{{ "planning" | translate }}'
            }
        };

        customerservice.prodcution_schedule = {
            parent: 'prodcution-base',
            name: 'production-schedule',
            url: '/production-schedule',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-schedule.html',
                    controller: 'orders.ScheduleCtrl' // draports
                }
            },
            ncyBreadcrumb: {
                label: '{{ "schedule" | translate }}'
            }
        };

        customerservice.prodcution_schedule_gantt = {
            parent: 'prodcution-base',
            name: 'production-schedule-gantt',
            url: '/production-schedule-gantt',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-schedule-gantt.html',
                    controller: 'orders.ScheduleGanttCtrl' // draports
                }
            },
            ncyBreadcrumb: {
                label: '{{ "schedule_gantt" | translate }}'
            }
        };

        customerservice.prodcution_planning_gantt = {
            parent: 'prodcution-base',
            name: 'production-planning-gantt',
            url: '/production-planning-gantt',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-planning-gantt.html',
                    controller: 'orders.PlanningGanttCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "planning_gantt" | translate }}'
            }
        };

        customerservice.prodcution_planning_machines_gantt = {
            parent: 'prodcution-base',
            name: 'production-planning-machines-gantt',
            url: '/production-planning-machines-gantt',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-planning-machines-gantt.html',
                    controller: 'orders.PlanningMachinesGanttCtrl' 
                }
            },
            ncyBreadcrumb: {
                label: '{{ "planning_gantt" | translate }}'
            }
        };

        customerservice.prodcution_raports = {
            parent: 'prodcution-base',
            name: 'production-raports',
            url: '/production-raports',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-raports.html',
                    controller: 'orders.RaportsCtrl' 
                },
                'raportsMenu@production-raports': {
                    templateUrl: 'src/orders/templates/raports-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "raports" | translate }}'
            }
        };

        customerservice.prodcution_raports_operator = {
            parent: 'production-raports',
            name: 'production-raports-operators',
            url: '/operators',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-raports-operators.html',
                    controller: 'orders.RaportOperatorsCtrl'
                },
                'raportsMenu@production-raports-operators': {
                    templateUrl: 'src/orders/templates/raports-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"operators_raport" | translate}}'
            }
        };

        customerservice.prodcution_raport_operator = {
            parent: 'production-raports-operators',
            name: 'production-raport-operator',
            url: '/:operatorID/operator',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-raport-operator.html',
                    controller: 'orders.RaportOperatorCtrl'
                },
                'raportsMenu@production-raport-operator': {
                    templateUrl: 'src/orders/templates/raports-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"operator" | translate}}'
            }
        };

        customerservice.prodcution_raports_device = {
            parent: 'production-raports',
            name: 'production-raports-devices',
            url: '/devices',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-raports-devices.html',
                    controller: 'orders.RaportDevicesCtrl'
                },
                'raportsMenu@production-raports-devices': {
                    templateUrl: 'src/orders/templates/raports-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"devices_raport" | translate}}'
            }
        };

        customerservice.prodcution_raport_device = {
            parent: 'production-raports-devices',
            name: 'production-raport-device',
            url: '/:deviceID/device',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-raport-device.html',
                    controller: 'orders.RaportDeviceCtrl'
                },
                'raportsMenu@production-raport-device': {
                    templateUrl: 'src/orders/templates/raports-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"device" | translate}}'
            }
        };

        customerservice.prodcution_raports_order = {
            parent: 'production-raports',
            name: 'production-raports-orders',
            url: '/orders',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-raports-orders.html',
                    controller: 'orders.RaportOrdersCtrl'
                },
                'raportsMenu@production-raports-orders': {
                    templateUrl: 'src/orders/templates/raports-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"orders_raport" | translate}}'
            }
        };

        customerservice.prodcution_raport_order = {
            parent: 'production-raports-orders',
            name: 'production-raport-order',
            url: '/:orderID/order',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-raport-order.html',
                    controller: 'orders.RaportOrderCtrl'
                },
                'raportsMenu@production-raport-order': {
                    templateUrl: 'src/orders/templates/raports-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"order" | translate}}'
            }
        }; 
        
        customerservice.prodcution_raport_operations = {
            parent: 'production-raports',
            name: 'production-raport-operations',
            url: '/operations',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-raport-operations.html',
                    controller: 'orders.RaportOperationsCtrl'
                },
                'raportsMenu@production-raport-operations': {
                    templateUrl: 'src/orders/templates/raports-menu.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{"operations" | translate}}'
            }
        };

        customerservice.prodcution_path = {
            parent: 'prodcution-base',
            name: 'production-path',
            url: '/productionPath/:deviceID',
            views: {
                'content@base': {
                    templateUrl: 'src/orders/templates/production-path.html',
                    controller: 'orders.OngoingsCtrl' // device ongoings
                }
            },
            ncyBreadcrumb: {
                label: '{{ "productction_path" | translate }}'
            }
        };

        customerservice.prodcution_operators = {
            parent: 'prodcution-base',
            name: 'production-operators',
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

        customerservice.base = {
            parent: 'base',
            name: 'customerservice-base',
            url: '/customerservice',
            ncyBreadcrumb: {
                label: "{{ 'customer_service' | translate }}"
            }
        };

        customerservice.index = {
            parent: 'customerservice-base',
            name: 'customerservice-register',
            url: '/customerservice-register',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/register.html',
                    controller: 'customerservice.RegisterCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "user_registration" | translate }}'
            }
        };

        customerservice.userlist = {
            parent: 'customerservice-base',
            name: 'customerservice-userlist',
            url: '/customerservice-userlist/:userID',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/userlist.html',
                    controller: 'customerservice.UsersListCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "users_list" | translate }}'
            }
        };

        customerservice.orderlist = {
            parent: 'customerservice-base',
            name: 'order-list',
            url: '/order-list',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/order-list.html',
                    controller: 'customerservice.OrderListCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "calculations" | translate }}'
            }
        };

        customerservice.orderofferlist = {
            parent: 'customerservice-base',
            name: 'order-offer-list',
            url: '/order-offer-list',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/order-offer-list.html',
                    controller: 'customerservice.OrderOfferListCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "calculations" | translate }}'
            }
        };

        customerservice.discounts = {
            parent: 'customerservice-base',
            name: 'discounts',
            url: '/discounts?discountGroupId',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/discounts.html',
                    controller: 'customerservice.DiscountsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "discounts" | translate }}'
            }
        };

        customerservice.promotions = {
            parent: 'customerservice-base',
            name: 'promotions',
            url: '/promotions?promotionId',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/promotions.html',
                    controller: 'customerservice.PromotionsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "promotions" | translate }}'
            }
        };

        customerservice.coupons = {
            parent: 'customerservice-base',
            name: 'coupons',
            url: '/coupons',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/coupons.html',
                    controller: 'customerservice.CouponsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "coupons" | translate }}'
            }
        };

        customerservice.newsletter = {
            parent: 'customerservice-base',
            name: 'newsletter',
            url: '/newsletter',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/newsletter.html',
                    controller: 'customerservice.NewsletterCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "newsletter" | translate }}'
            }
        };

        customerservice.ordermakeorder = {
            parent: 'customerservice-base',
            name: 'order-make-order',
            url: '/order-make-order/:orderID/:edit/:ver',
            resolve: {
                order: ['DpOrderService', '$stateParams', function (DpOrderService, $stateParams) {
                    return DpOrderService.get($stateParams.orderID, $stateParams.ver).then(function (data) {
                        return data;
                    });
                }]
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/order-make-order.html',
                    controller: 'customerservice.OrderMakeOrderCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "calculations" | translate }}'
            }
        };

        customerservice.create_order = {
            parent: 'customerservice-base',
            name: 'create-order',
            url: '/:userID/:orderID/cp:customProductID/create-order',
            resolve: {
                typeOfResource: function() {
                    return {'type': 'order'};
                }
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/create-order.html',
                    controller: 'customerservice.CreateOrderCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "create_order" | translate }}'
            }
        };

        customerservice.create_offer = {
            parent: 'customerservice-base',
            name: 'create-offer',
            url: '/:userID/:orderID/cp:customProductID/create-offer',
            resolve: {
                typeOfResource: function() {
                    return {'type': 'offer'};
                }
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/create-order.html',
                    controller: 'customerservice.CreateOrderCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "create_offer" | translate }}'
            }
        };

        customerservice.unfinished_orders = {
            parent: 'create-order',
            name: 'unfinished-orders',
            url: '/:userID/:orderID/create-order/unfinished-orders',
            resolve: {
                typeOfResource: function() {
                    return {'type': 'order'};
                }
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/unfinished-orders.html',
                    controller: 'customerservice.UnfinishedOrderCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "orders_unfinished" | translate }}'
            }
        };

        customerservice.unfinished_offers = {
            parent: 'create-offer',
            name: 'unfinished-offers',
            url: '/:userID/:orderID/create-offer/unfinished-offers',
            resolve: {
                typeOfResource: function() {
                    return {'type': 'offer'};
                }
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/unfinished-orders.html',
                    controller: 'customerservice.UnfinishedOrderCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "offers_unfinished" | translate }}'
            }
        };

        customerservice.create_order_groups = {
            parent: 'create-order',
            name: 'create-order-groups',
            url: '/groups',
            resolve: {
                typeOfResource: function() {
                    return {'type': 'order'};
                }
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/create-order-groups.html',
                    controller: 'customerservice.CreateOrderGroupsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "create_order" | translate }}'
            }
        };

        customerservice.create_offer_groups = {
            parent: 'create-offer',
            name: 'create-offer-groups',
            url: '/groups',
            resolve: {
                typeOfResource: function() {
                    return {'type': 'offer'};
                }
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/create-order-groups.html',
                    controller: 'customerservice.CreateOrderGroupsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "create_offer" | translate }}'
            }
        };

        customerservice.create_order_types = {
            parent: 'create-order-groups',
            name: 'create-order-types',
            url: '/:groupID/types',
            resolve: {
                typeOfResource: function() {
                    return {'type': 'order'};
                }
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/create-order-types.html',
                    controller: 'customerservice.CreateOrderTypesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "group" | translate }}: {{ group.name }}'
            }
        };

        customerservice.create_offer_types = {
            parent: 'create-offer-groups',
            name: 'create-offer-types',
            url: '/:groupID/types',
            resolve: {
                typeOfResource: function() {
                    return {'type': 'offer'};
                }
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/create-order-types.html',
                    controller: 'customerservice.CreateOrderTypesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "group" | translate }}: {{ group.name }}'
            }
        };

        var getData = ['$q', '$stateParams', 'PsGroupService', 'PsTypeService', 'CalculationService', 'UserService', 'DpProductService',
            function ($q, $stateParams, PsGroupService, PsTypeService, CalculationService, UserService, DpProductService) {
                var currentGroupID = parseInt($stateParams.groupID);
                var currentTypeID = parseInt($stateParams.typeID);
                var currentCalcID = $stateParams.calcID || null;
                var currentUserID = $stateParams.userID || null;
                var currentProductID = $stateParams.productID || null;
                var def = $q.defer();

                var promises = [
                    PsGroupService.get(currentGroupID),
                    PsTypeService.get(currentGroupID, currentTypeID)
                ];
                if (currentCalcID) {
                    promises.push(CalculationService.get(currentCalcID));
                } else {
                    promises.push(null);
                }
                if (currentProductID) {
                    promises.push(DpProductService.baseInfo(currentProductID));
                } else {
                    promises.push(null);
                }

                $q.all(promises).then(function (data) {
                    var group = data[0];
                    var type = data[1];
                    var calc = data[2] || null;
                    var user = data[3] || null;
                    var product = data[4] || null;

                    def.resolve({
                        currentGroupID: currentGroupID,
                        currentTypeID: currentTypeID,
                        currentCalcID: currentCalcID,
                        currentUserID: currentUserID,
                        currentProductID: currentProductID,
                        group: group,
                        type: type,
                        calc: calc,
                        user: user,
                        product: product
                    });
                }, function (data) {
                    def.reject(data);
                });

                return def.promise;
            }];

        customerservice.create_order_calc = {
            parent: 'create-order-types',
            name: 'create-order-calc',
            url: '/:typeID/calc/:calcID/prod/:productID',
            resolve: {
                getData: getData,
                typeOfResource: function() {
                    return {'type': 'order'};
                }
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/create-order-calc.html',
                    controller: 'customerservice.CreateOrderCalcCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "create_order" | translate }}'
            }
        };

        customerservice.create_offer_calc = {
            parent: 'create-offer-types',
            name: 'create-offer-calc',
            url: '/:typeID/calc/:calcID/prod/:productID',
            resolve: {
                getData: getData,
                typeOfResource: function() {
                    return {'type': 'offer'};
                }
            },
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/create-order-calc.html',
                    controller: 'customerservice.CreateOrderCalcCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "create_offer" | translate }}'
            }
        };

        /*customerservice.create_offer = {
            parent: 'customerservice-base',
            name: 'customerservice-create-offer',
            url: '/customerservice-create-offer',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/create-offer.html',
                    controller: 'customerservice.CreateOfferCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "create_offer" | translate }}'
            }
        };*/

        customerservice.offer_list = {
            parent: 'customerservice-base',
            name: 'customerservice-offer-list',
            url: '/customerservice-offer-list',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/offer-list.html',
                    controller: 'customerservice.OfferListCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "offer_list" | translate }}'
            }
        };

        customerservice.offer_inorder_list = {
            parent: 'customerservice-base',
            name: 'customerservice-offer-inOrder-list',
            url: '/customerservice-offer-inOrder-list',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/offer-inOrder-list.html',
                    controller: 'customerservice.OfferInOrderListCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "placed_orders" | translate }}'
            }
        };

        customerservice.reclamations = {
            parent: 'customerservice-base',
            name: 'customerservice-reclamations',
            url: '/customerservice-reclamations',
            views: {
                'content@base': {
                    templateUrl: 'src/customerservice/templates/reclamations.html',
                    controller: 'customerservice.ReclamationsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "reclamations" | translate }}'
            }
        };

        _.each(customerservice, function (route) {
            $stateProvider.state(route);
        });

    });
