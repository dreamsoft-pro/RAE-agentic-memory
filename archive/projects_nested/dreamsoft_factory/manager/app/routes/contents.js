angular.module('digitalprint.routes')
    .config(function ($stateProvider) {

        var contents = {};

        contents.base = {
            parent: 'base',
            name: 'contents-base',
            url: '/contents',
            ncyBreadcrumb: {
                label: '{{ "contents" | translate }}'
            }
        };

        contents.index = {
            parent: 'contents-base',
            name: 'contents-routes',
            url: '/routes',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/routes.html',
                    controller: 'contents.RoutesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "routing" | translate }}'
            }
        };

        contents.views = {
            parent: 'contents-routes',
            name: 'contents-views',
            url: '/:routeID/views',
            resolve: {
                currentRoot: ['RouteService', '$stateParams', function (RouteService, $stateParams) {
                    return RouteService.getOne($stateParams.routeID).then(function (data) {
                        console.log(data);
                        return data;
                    }, function (data) {
                        console.error("NIe pobiera routa")
                    });
                }]
            },
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/views.html',
                    controller: 'contents.ViewsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "views" | translate }}'
            }
        };

        contents.seo = {
            parent: 'contents-base',
            name: 'contents-seo',
            url: '/seo',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/seo.html',
                    controller: 'contents.SeoCtrl'
                }
            },
            ncyBreadcrumb: {
                label: 'SEO'
            }
        };

        contents.mails = {
            parent: 'contents-base',
            name: 'contents-mails',
            url: '/mails',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/mails.html',
                    controller: 'contents.MailsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "mails" | translate }}'
            }
        };

        contents.mailContent = {
            parent: 'contents-mails',
            name: 'contents-mail-content',
            url: '/:typeID/content',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/mail-contents.html',
                    controller: 'contents.MailContentsCtrl'
                },
                'add-register-coupon@contents-mail-content': {
                    templateUrl: 'src/contents/templates/add-register-coupon.html'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "content" | translate }}'
            }
        };

        contents.categories = {
            parent: 'contents-base',
            name: 'contents-categories',
            url: '/categories',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/categories.html',
                    controller: 'contents.CategoriesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "categories" | translate }}'
            }
        };

        contents.categoriesSort = {
            parent: 'contents-categories',
            name: 'contents-categories-sort',
            url: '/categories-sort/:categoryid',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/categories-sort.html',
                    controller: 'contents.CategoriesSortCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "sort_categories" | translate }}'
            }
        };

        contents.graphics = {
            parent: 'contents-base',
            name: 'contents-graphics',
            url: '/graphics',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/graphics.html',
                    controller: 'contents.GraphicsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "graphics" | translate }}'
            }
        };

        contents.layout = {
            parent: 'contents-base',
            name: 'contents-layout',
            url: '/layout',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/layout.html',
                    controller: 'contents.LayoutCtrl'
                },
                'contents-layout-settings@contents-layout': {
                    templateUrl: 'src/contents/templates/layout-settings.html',
                    controller: 'contents.LayoutSettingsCtrl'
                },
                'contents-template-variables@contents-layout': {
                    templateUrl: 'src/contents/templates/template-variables.html',
                    controller: 'contents.TemplateVariablesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "view_settings" | translate }}'
            }
        };

        contents.templates = {
            parent: 'contents-base',
            name: 'contents-templates',
            url: '/templates',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/templates.html',
                    controller: 'contents.TemplatesCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "templates" | translate }}'
            }
        };

        contents.static_contents = {
            parent: 'contents-base',
            name: 'contents-static',
            url: '/static',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/static-contents.html',
                    controller: 'contents.StaticContentsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "static_contents" | translate }}'
            }
        };

        contents.reclamations = {
            parent: 'contents-base',
            name: 'contents-reclamation-faults',
            url: '/reclamations-faults',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/reclamations.html',
                    controller: 'contents.ReclamationsCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "reclamations" | translate }}'
            }
        };

        contents.styleEdit = {
            parent: 'contents-base',
            name: 'contents-style-edit',
            url: '/style-edit',
            views: {
                'content@base': {
                    templateUrl: 'src/contents/templates/style-edit.html',
                    controller: 'contents.StyleEditCtrl'
                }
            },
            ncyBreadcrumb: {
                label: '{{ "edit_styles" | translate }}'
            }
        };


        _.each(contents, function (route) {
            $stateProvider.state(route);
        });

    });
