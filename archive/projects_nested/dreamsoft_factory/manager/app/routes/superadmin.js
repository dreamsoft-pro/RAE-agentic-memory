angular.module('digitalprint.routes')
    .config(function ($stateProvider) {

        var superadmin = {};

        superadmin.base = {
            parent: 'base',
            name: 'superadmin-base',
            url: '/superadmin',
            ncyBreadcrumb: {
                label: 'Superadmin'
            }
        };

        superadmin.index = {
            parent: 'superadmin-base',
            name: 'superadmin-request-tester',
            url: '/request-tester',
            views: {
                'content@base': {
                    templateUrl: 'src/superadmin/templates/request-tester.html',
                    controller: 'superadmin.RequestTesterCtrl'
                },
                'add-domain@superadmin-request-tester': {
                    templateUrl: 'src/superadmin/templates/add-domain.html',
                    controller: 'superadmin.AddDomainCtrl'
                },
                'create-company@superadmin-request-tester': {
                    templateUrl: 'src/superadmin/templates/create-company.html',
                    controller: 'superadmin.CreateCompanyCtrl'
                },
                'socket-tester@superadmin-request-tester': {
                    templateUrl: 'src/superadmin/templates/socket-tester.html',
                    controller: 'superadmin.SocketTesterCtrl'
                },
                'import-users@superadmin-request-tester': {
                    templateUrl: 'src/superadmin/templates/import-users.html',
                    controller: 'superadmin.ImportUsersCtrl'
                }
            },
            ncyBreadcrumb: {
                label: 'Request tester'
            }
        };

        superadmin.acl = {
            parent: 'superadmin-base',
            name: 'superadmin-acl',
            url: '/acl',
            views: {
                'content@base': {
                    templateUrl: 'src/superadmin/templates/acl.html',
                    controller: 'superadmin.AclCtrl'
                }
            },
            ncyBreadcrumb: {
                label: 'ACL'
            }
        };

        superadmin.langs = {
            parent: 'superadmin-base',
            name: 'superadmin-langs',
            url: '/langs',
            views: {
                'content@base': {
                    templateUrl: 'src/superadmin/templates/langs.html',
                    controller: 'superadmin.LangsRootCtrl'
                },
                'lang-settings@superadmin-langs': {
                    templateUrl: 'src/superadmin/templates/lang-settings.html',
                    controller: 'superadmin.LangSettingsRootCtrl'
                },
                'lang-empty@superadmin-langs': {
                    templateUrl: 'src/superadmin/templates/lang-empty.html',
                    controller: 'superadmin.LangsRootEmptyCtrl'
                },
                'lang-export-import@superadmin-langs': {
                    templateUrl: 'shared/templates/lang-export-import.html',
                    controller: 'superadmin.LangExportImportCtrl'
                }
            },
            ncyBreadcrumb: {
                label: 'Lang'
            }
        };

        superadmin.modules = {
            parent: 'superadmin-base',
            name: 'superadmin-modules',
            url: '/modules',
            views: {
                'content@base': {
                    templateUrl: 'src/superadmin/templates/modules.html',
                    controller: 'superadmin.ModulesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: 'Modules'
            }
        };

        superadmin.templates = {
            parent: 'superadmin-base',
            name: 'superadmin-templates',
            url: '/templates',
            views: {
                'content@base': {
                    templateUrl: 'src/superadmin/templates/templates.html',
                    controller: 'superadmin.TemplatesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: "{{ 'default_templates' | translate }}"
            }
        };

        superadmin.helps = {
            parent: 'superadmin-base',
            name: 'superadmin-helps',
            url: '/helps',
            views: {
                'content@base': {
                    templateUrl: 'src/superadmin/templates/helps.html',
                    controller: 'superadmin.AdminHelpsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: 'Admin helps'
            }
        };

        superadmin.mail = {
            parent: 'superadmin-base',
            name: 'superadmin-mail',
            url: '/mail',
            views: {
                'content@base': {
                    templateUrl: 'src/superadmin/templates/mail-types.html',
                    controller: 'superadmin.MailTypesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: 'Mail settings'
            }
        };

        _.each(superadmin, function (route) {
            $stateProvider.state(route);
        });

    });
