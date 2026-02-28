angular.module('digitalprint.routes')
    .config(function ($stateProvider) {

        var shop = {};

        shop.base = {
            parent: 'base',
            name: 'shop-base',
            url: '/shop',
            ncyBreadcrumb: {
                label: '{{ "shop" | translate }}'
            }
        };

        shop['domain-config'] = {
            parent: 'shop-base',
            name: 'shop-domain-config',
            url: '/domain-config',
            views: {
                'content@base': {
                    templateUrl: 'src/shop/templates/domain-config.html'
                },
                'domain-config-base@shop-domain-config': {
                    templateUrl: 'src/shop/templates/domain-config-base.html',
                    controller: 'shop.DomainConfigCtrl'
                },
                'config-mail@shop-domain-config': {
                    templateUrl: 'src/shop/templates/config-mail.html',
                    controller: 'shop.ConfigMailCtrl'
                },
                'lang-settings@shop-domain-config': {
                    templateUrl: 'src/shop/templates/lang-settings.html',
                    controller: 'shop.LangSettingsCtrl'
                },
                'currency@shop-domain-config': {
                    templateUrl: 'src/shop/templates/currency.html',
                    controller: 'shop.CurrenciesCtrl'
                },
                'taxes@shop-domain-config': {
                    templateUrl: 'src/shop/templates/taxes.html',
                    controller: 'shop.TaxesCtrl'
                },
                'deliveries@shop-domain-config': {
                    templateUrl: 'src/shop/templates/deliveries.html',
                    controller: 'shop.DeliveriesCtrl'
                },
                'payments@shop-domain-config': {
                    templateUrl: 'src/shop/templates/payments.html',
                    controller: 'shop.PaymentsCtrl'
                },
                'invoices@shop-domain-config': {
                    templateUrl: 'src/shop/templates/invoices.html',
                    controller: 'shop.InvoicesCtrl'
                },
                'sender-data@shop-domain-config': {
                    templateUrl: 'src/shop/templates/sender-data.html',
                    controller: 'shop.SenderDataCtrl'
                },
                'invoice-data@shop-domain-config': {
                    templateUrl: 'src/shop/templates/invoice-data.html',
                    controller: 'shop.InvoiceDataCtrl'
                },
                'forms@shop-domain-config': {
                    templateUrl: 'src/shop/templates/forms.html',
                    controller: 'shop.FormsCtrl'
                },
                'additional-settings@shop-domain-config': {
                    templateUrl: 'src/shop/templates/additional-settings.html',
                    controller: 'shop.AdditionalSettingsCtrl'
                },
                'seo-settings@shop-domain-config': {
                    templateUrl: 'src/shop/templates/seo-settings.html',
                    controller: 'shop.SeoSettingsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "domain_config" | translate }}'
            }
        };

        shop.couriers = {
            parent: 'shop-base',
            name: 'shop-couriers',
            url: '/couriers',
            views: {
                'content@base': {
                    templateUrl: 'src/shop/templates/couriers.html',
                    controller: 'shop.CouriersCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "couriers" | translate }}'
            }
        };

        shop.langs = {
            parent: 'shop-base',
            name: 'shop-langs',
            url: '/langs',
            views: {
                'content@base': {
                    templateUrl: 'src/shop/templates/langs.html',
                    controller: 'shop.LangsCtrl'
                },
                'lang-export-import@shop-langs': {
                    templateUrl: 'shared/templates/lang-export-import.html',
                    controller: 'superadmin.LangExportImportCtrl'
                },
            },
            ncyBreadcrumb: {
                label: '{{ "language" | translate }}'
            }
        };

        shop.specialAccounts = {
            parent: 'shop-base',
            name: 'shop-special-accounts',
            url: '/special-accounts',
            views: {
                'content@base': {
                    templateUrl: 'src/shop/templates/special-accounts.html',
                    controller: 'shop.SpecialAccountsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "special_accounts" | translate }}'
            }
        };

        shop.permissions = {
            parent: 'shop-base',
            name: 'shop-permissions',
            url: '/shop-permissions',
            views: {
                'content@base': {
                    templateUrl: 'src/shop/templates/permissions.html',
                    controller: 'shop.PermissionsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "permissions" | translate }}'
            }
        };

        shop.supportedCountries = {
            parent: 'shop-base',
            name: 'supported-countries',
            url: '/supported-countries',
            views: {
                'content@base': {
                    templateUrl: 'src/shop/templates/supported-countries.html',
                    controller: 'shop.SupportedCountriesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "supported_countries" | translate }}'
            }
        };

        _.each(shop, function (route) {
            $stateProvider.state(route);
        });

    });
