/* global require: true, console:true, module:true */

module.exports = function (grunt) {

    var path = require('path');

    var config = require('./configs/prod.config')({});

    var appOptions = config.get();

    require('load-grunt-tasks')(grunt);
    require('time-grunt')(grunt);

    var versionHash = '';
    if (grunt.option('versionHash') !== undefined) {
        versionHash = grunt.option('versionHash');
    } else {
        var actDate = new Date();
        versionHash = actDate.getHours() + actDate.getMinutes() + actDate.getSeconds();
    }

    var gruntConfigs = {
        'hash': versionHash,
        'apiUrl': appOptions.apiUrl,
        'editorApiUrl': appOptions.editorApiUrl,
        'authUrl': appOptions.authUrl,
        'staticUrl': appOptions.staticUrl,
        'socketUrl': appOptions.socketUrl,
        'editorUrl': appOptions.editorUrl,
        'id': appOptions.id,
        'domainID': appOptions.domainID
    };

    if (grunt.option('apiUrl') !== undefined) {
        gruntConfigs.apiUrl = grunt.option('apiUrl');
    }

    if (grunt.option('editorApiUrl') !== undefined) {
        gruntConfigs.editorApiUrl = grunt.option('editorApiUrl');
    }

    if (grunt.option('authUrl') !== undefined) {
        gruntConfigs.authUrl = grunt.option('authUrl');
    }

    if (grunt.option('staticUrl') !== undefined) {
        gruntConfigs.staticUrl = grunt.option('staticUrl');
    }

    if (grunt.option('domainID') !== undefined) {
        gruntConfigs.domainID = grunt.option('domainID');
    }

    if (grunt.option('robots') !== undefined) {
        gruntConfigs.robots = grunt.option('robots');
    } else {
        gruntConfigs.robots = 'all';
    }

    if (grunt.option('socketUrl') !== undefined) {
        gruntConfigs.socketUrl = grunt.option('socketUrl');
    }

    if (grunt.option('editorUrl') !== undefined) {
        gruntConfigs.editorUrl = grunt.option('editorUrl');
    }

    if (grunt.option('id') !== undefined) {
        gruntConfigs.id = grunt.option('id');
    }

    if (
        grunt.option('id') !== undefined &&
        appOptions.gaCodes[grunt.option('id')] !== undefined
    ) {
        gruntConfigs.mainFolder = appOptions.mainFolders[grunt.option('id')];
    } else {
        gruntConfigs.mainFolder = appOptions.mainFolders.default;
    }

    gruntConfigs.seo = appOptions.seo.default;
    gruntConfigs.gaCode = appOptions.gaCodes.default;
    gruntConfigs.googleToolId = appOptions.googleWebTools.default;

    grunt.initConfig({
        gruntConfigs: gruntConfigs,

        watch: {
            less: {
                files: [
                    'app/assets/less/**/*.less'
                ],
                tasks: [
                    'less:dev',
                    'replace:stylefonts'
                ]
            },
            templates: {
                files: [
                    'app/src/category/templates/calc/*.html',
                    'app/src/category/templates/panels/*.html',
                    'app/src/cart/templates/_cart.html',
                    'app/src/index/templates/_login.html',
                    'app/src/index/templates/_register.html',
                    'app/src/views/_forms/*.html',
                    'app/src/category/templates/modalboxes/_printoffer.html',
                    'app/src/category/templates/_configure-project.html',
                    'app/src/category/templates/_custom-product.html',
                    'app/src/cart/templates/_copy-product-modal.html'
                ],
                tasks: [
                    'processhtml:templates'
                ]
            },
            livereload: {
                options: {
                    livereload: 35729,
                    debounceDelay: 500
                },
                files: [
                    'app/{,**/}*.html',
                    'app/styles/{,**/}*.css',
                    'app/images/{,**/}*.{png,jpg,jpeg,gif,webp,svg}'
                ]
            },
            demo: {
                files: [],
                livereload: {
                    options: {
                        livereload: 35730
                    }
                }
            },
            prod: {
                files: [],
                livereload: {
                    options: {
                        livereload: 35731
                    }
                }
            }
        },

        express: {
            demo: {
                options: {
                    port: 9012,
                    server: path.resolve('./server-demo')
                }
            },
            dev: {
                options: {
                    port: 80,
                    server: path.resolve('./server-dev')
                }
            },
            prod: {
                options: {
                    port: 9010,
                    server: path.resolve('./server-prod')
                }
            },
            ng2: {
                options: {
                    port: 80,
                    server: path.resolve('./server-ng2')
                }
            }
        },

        clean: {
            js: ['./<%= gruntConfigs.mainFolder %>', './.tmp']
        },

        less: {
            options: {},
            dev: {
                files: [
                    {
                        expand: true,
                        cwd: './app/assets/less/skins/simple-blue',
                        src: [
                            '**/style.less'
                        ],
                        dest: './app/css/skins/',
                        ext: '.css'
                    }
                ]
            },
            prod: {
                files: [
                    {
                        expand: true,
                        cwd: './app/assets/less/skins',
                        src: [
                            '**/style.less'
                        ],
                        dest: './.tmp/skins/',
                        ext: '.css'
                    }
                ]
            }
        },

        uncss: {
            dev: {
                options: {
                    ignore: [
                        '.breadcrumb',
                        '.breadcrumb > li',
                        '.breadcrumb > .active'
                    ],
                    uncssrc: 'uncssrc.json'
                },
                files: {
                    'app/digitalprint.uncss.css': [
                        'app/index.html',
                        'app/views/**/*.html',
                        'app/src/**/*.html'
                    ]
                }
            },
            prod: {
                options: {
                    ignore: ['.breadcrumb'],
                    uncssrc: 'uncssrc.json'
                },
                files: {
                    '.tmp/digitalprint.uncss.css': [
                        '<%= gruntConfigs.mainFolder %>/index.html',
                        '<%= gruntConfigs.mainFolder %>/views/**/*.html',
                        '<%= gruntConfigs.mainFolder %>/src/**/*.html'
                    ]
                }
            }
        },

        postcss: {
            dev: {
                options: {
                    map: false,
                    processors: [
                        require('pixrem')(),
                        require('autoprefixer')({
                            // Zalecany klucz to 'overrideBrowserslist'
                            overrideBrowserslist: ['last 2 versions']
                        }),
                        require('cssnano')()
                    ]
                },
                files: {
                    'app/digitalprint-<%= gruntConfigs.hash %>.css': '.tmp/digitalprint.uncss.css'
                }
            },
            prod: {
                options: {
                    map: false,
                    processors: [
                        require('pixrem')(),
                        require('autoprefixer')({
                            overrideBrowserslist: ['last 2 versions']
                        }),
                        require('cssnano')()
                    ]
                },
                files: [
                    {
                        expand: true,
                        cwd: './.tmp/skins',
                        src: [
                            '**/style.css'
                        ],
                        dest: './<%= gruntConfigs.mainFolder %>/css/skins/',
                        rename: function (dest, src) {
                            return dest + src.replace('style', 'style-' + gruntConfigs.hash);
                        }
                    }
                ]
            }
        },

        replace: {
            stylefonts: {
                src: ['./app/css/skins/**/style.css'],
                overwrite: true,
                replacements: [
                    {
                        from: '../fonts/',
                        to: '/assets/node_modules/font-awesome/fonts/'
                    },
                    {
                        from: 'mCSB_buttons.png',
                        to: '../mCSB_buttons.png'
                    }
                ]
            },
            'stylefonts-prod': {
                src: ['./.tmp/skins/**/style.css'],
                overwrite: true,
                replacements: [
                    {
                        from: '../fonts/',
                        to: '/assets/node_modules/font-awesome/fonts/'
                    }
                ]
            }
        },

        'sails-linker': {
            routes: {
                options: {
                    startTag: '<!--ROUTES-->',
                    endTag: '<!--ROUTES END-->',
                    appRoot: 'app'
                },
                files: {
                    './app/index.html': 'app/routes/**/*.js'
                }
            },
            helpers: {
                options: {
                    startTag: '<!--HELPERS-->',
                    endTag: '<!--HELPERS END-->',
                    appRoot: 'app'
                },
                files: {
                    './app/index.html': 'app/assets/helpers/**/*.js'
                }
            },
            modules: {
                options: {
                    startTag: '<!--MODULES-->',
                    endTag: '<!--MODULES END-->',
                    appRoot: 'app'
                },
                files: {
                    './app/index.html': ['app/src/**/*.js']
                }
            },
            services: {
                options: {
                    startTag: '<!--SERVICES-->',
                    endTag: '<!--SERVICES END-->',
                    appRoot: 'app'
                },
                files: {
                    './app/index.html': 'app/services/**/*.js'
                }
            },
            filters: {
                options: {
                    startTag: '<!--FILTERS-->',
                    endTag: '<!--FILTERS END-->',
                    appRoot: 'app'
                },
                files: {
                    './app/index.html': 'app/filters/**/*.js'
                }
            }
        },

        copy: {
            'build-dev': {
                files: [
                    {
                        expand: true,
                        dest: 'app/assets/',
                        cwd: '',
                        src: [
                            'node_modules/**/*.{js,css,map,png,jpg,woff,ttf,eot,svg,woff2}'
                        ]
                    },
                    {
                        src: 'node_modules/malihu-custom-scrollbar-plugin/mCSB_buttons.png',
                        dest: 'app/css/skins/mCSB_buttons.png'
                    },
                    {
                        src: 'libraries/uploaderStandalone.min.js',
                        dest: 'app/assets/libraries/uploaderStandalone.min.js'
                    },
                    {
                        src: 'libraries/turnjs/modernizr.2.5.3.min.js',
                        dest: 'app/assets/libraries/turnjs/modernizr.2.5.3.min.js'
                    },
                    {
                        src: 'libraries/turnjs/turn.min.js',
                        dest: 'app/assets/libraries/turnjs/turn.min.js'
                    },
                    {
                        src: 'libraries/turnjs/basic.css',
                        dest: 'app/assets/libraries/turnjs/basic.css'
                    },
                    {
                        src: 'node_modules/angular-recaptcha/release/angular-recaptcha.min.js',
                        dest: 'app/assets/node_modules/angular-recaptcha/release/angular-recaptcha.min.js'
                    },
                    {
                        src: 'libraries/socket/socket.io.slim.js',
                        dest: 'app/assets/libraries/socket/socket.io.slim.js'
                    },
                    {
                        src: 'node_modules/ulog/ulog.min.js',
                        dest: 'app/assets/libraries/ulog.min.js'
                    },
                    {
                        src: 'node_modules/klaro/dist/klaro.js',
                        dest: 'app/assets/klaro/dist/klaro.js'
                    }
                ]
            },
            build: {
                files: [
                    {
                        cwd: 'app/',
                        expand: true,
                        src: [
                            'views/**/*.html',
                            'src/**/*.html'
                        ],
                        dest: '<%= gruntConfigs.mainFolder %>'
                    },
                    {
                        src: 'node_modules/ulog/ulog.min.js',
                        dest: '<%= gruntConfigs.mainFolder %>/assets/libraries/ulog.min.js'
                    },
                    {
                        src: 'node_modules/malihu-custom-scrollbar-plugin/mCSB_buttons.png',
                        dest: '<%= gruntConfigs.mainFolder %>/css/skins/mCSB_buttons.png'
                    },
                    {
                        expand: true,
                        cwd: 'app/',
                        dest: '<%= gruntConfigs.mainFolder %>/',
                        src: [
                            'assets/{helpers,img}/**/*.{js,png,jpg}'
                        ]
                    },
                    {
                        expand: true,
                        cwd: 'app/',
                        dest: '<%= gruntConfigs.mainFolder %>/',
                        src: [
                            'assets/libraries/*.js',
                            'assets/libraries/turnjs/*.js',
                            'assets/libraries/turnjs/*.css',
                            'assets/libraries/socket/*.js'
                        ]
                    },
                    {
                        expand: true,
                        cwd: 'app/',
                        dest: '<%= gruntConfigs.mainFolder %>/',
                        src: [
                            '*.{ico,png,txt}',
                            '.htaccess',
                            'index.html'
                        ]
                    },
                    {
                        expand: true,
                        dest: '<%= gruntConfigs.mainFolder %>/',
                        cwd: 'copy_prod/',
                        dot: true,
                        src: [
                            '404.html',
                            '\\.htaccess',
                            'robots.txt'
                        ]
                    },
                    {
                        expand: true,
                        dest: '<%= gruntConfigs.mainFolder %>/assets/',
                        cwd: '',
                        src: [
                            'node_modules/**/*.{css,woff,ttf,eot,svg,woff2}'
                        ]
                    },
                    {
                        expand: true,
                        dest: '<%= gruntConfigs.mainFolder %>/assets/',
                        cwd: 'app/',
                        dot: true,
                        src: [
                            'node_modules/flag-icon-css/flags/*/*.svg'
                        ]
                    }
                ]
            },
            deploy: {
                files: [
                    {
                        expand: true,
                        cwd: 'app',
                        src: [
                            '*.html',
                            '{src,views}/**/*.html',
                            'views/backend/*.html'
                        ],
                        dest: '.tmp/deploy/'
                    }
                ]
            }
        },

        mkdir: {
            options: {}
        },

        rename: {
            // Dodajemy brakującą konfigurację, aby naprawić błąd w trakcie "rename:deploy"
            deploy: {
                files: [
                    {
                        // Przykład - możesz dostosować do własnych potrzeb
                        src: '.tmp/deploy/index.html',
                        dest: '.tmp/deploy/index-deploy.html'
                    }
                ]
            },
            prod2: {
                files: [
                    {
                        src: [
                            'dist/index.tmp.html'
                        ],
                        dest: 'dist/index.html'
                    }
                ]
            }
        },

        concat: {
            options: {
                separator: ";\n"
            },
            dist: {
                src: [
                    'app/*.js',
                    'app/routes/**/*.js',
                    'app/assets/helpers/**/*.js',
                    'app/src/**/*.js',
                    'app/services/**/*.js',
                    'app/filters/**/*.js'
                ],
                dest: '.tmp/scripts.js'
            },
            extras: {
                src: [
                    //external
                    'node_modules/lodash/index.js',
                    'node_modules/jquery/dist/jquery.min.js',
                    'app/assets/libraries/jquery-ui/jquery-ui.js',
                    'node_modules/bootstrap/dist/js/bootstrap.min.js',
                    'node_modules/bootstrap-hover-dropdown/bootstrap-hover-dropdown.min.js',
                    'node_modules/klaro/dist/klaro.js',
                    //angular
                    'node_modules/angular/angular.js',
                    'node_modules/angular-ui-router/release/angular-ui-router.js',
                    'node_modules/restangular/dist/restangular.min.js',
                    'node_modules/angular-local-storage/dist/angular-local-storage.js',
                    'node_modules/angular-bootstrap/ui-bootstrap.js',
                    'node_modules/angular-bootstrap/ui-bootstrap-tpls.js',
                    'node_modules/angular-animate/angular-animate.js',
                    'node_modules/angular-breadcrumb/dist/angular-breadcrumb.js',
                    'node_modules/angular-translate/dist/angular-translate.js',
                    'node_modules/angular-translate/dist/angular-translate-loader-static-files/angular-translate-loader-static-files.js',
                    'node_modules/rangy/lib/rangy-core.js',
                    'node_modules/rangy/lib/rangy-selectionsaverestore.js',
                    'node_modules/textangular/dist/textAngular-sanitize.min.js',
                    'node_modules/textangular/dist/textAngular.min.js',
                    'node_modules/angular-cookies/angular-cookies.js',
                    'node_modules/angular-ui-sortable/dist/sortable.js',
                    'node_modules/angular-socket-io/socket.js',
                    'node_modules/angular-file-upload/angular-file-upload.js',
                    'node_modules/angular-carousel/dist/angular-carousel.min.js',
                    'node_modules/angular-touch/angular-touch.min.js',
                    'node_modules/angular-ui-notification/src/angular-ui-notification.js',
                    'node_modules/angular-recaptcha/release/angular-recaptcha.min.js',
                    'node_modules/angular-ui-notification/dist/angular-ui-notification.min.js',
                    'node_modules/angular-paging/dist/paging.min.js',
                    'node_modules/angular-responsive-tables/release/angular-responsive-tables.min.js',
                    'node_modules/moment/min/moment-with-locales.js',
                    'node_modules/bootstrap-daterangepicker/daterangepicker.js',
                    'node_modules/malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.concat.min.js',
                    'node_modules/ng-scrollbars/dist/scrollbars.min.js',
                    'node_modules/angularjs-slider/dist/rzslider.min.js',
                    'node_modules/angular-recaptcha/release/angular-recaptcha.min.js',
                    'node_modules/angular-update-meta/dist/update-meta.min.js',
                    //helpers
                    'app/assets/helpers/angular-api-collection/angular-api-collection.js',
                    'app/assets/helpers/angular-api-collection/angular-api-pagination.js',
                    // libraries
                    'app/assets/libraries/uploaderStandalone.min.js',
                    'app/assets/libraries/turnjs/modernizr.2.5.3.min.js',
                    'app/assets/libraries/turnjs/turn.min.js',
                    'node_modules/clipboard/dist/clipboard.js',
                    'app/assets/libraries/ngGallery/src/js/ngGallery.js',
                    'app/assets/libraries/cropperjs/cropper.js',
                    'app/assets/libraries/caman/caman.full.min.js'
                ],
                dest: '.tmp/scripts-extras.js',
                nonull: true
            }
        },

        ngAnnotate: {
            options: {
                singleQuotes: true
            },
            app1: {
                files: {
                    '.tmp/scripts-b.js': ['.tmp/scripts-b.js'],
                    '.tmp/scripts-extras.js': ['.tmp/scripts-extras.js']
                }
            }
        },

        uglify: {
            options: {},
            build: {
                files: {
                    '<%= gruntConfigs.mainFolder %>/scripts/scripts-<%= gruntConfigs.hash %>.min.js': ['.tmp/scripts-b.js'],
                    '<%= gruntConfigs.mainFolder %>/scripts/scripts.extras-<%= gruntConfigs.hash %>.min.js': ['.tmp/scripts-extras.js']
                }
            }
        },

        babel: {
            options: {
                sourceMap: false,
                presets: ['@babel/preset-env'],
                minified: true,
                plugins: [
                    "@babel/plugin-transform-nullish-coalescing-operator",
                    "@babel/plugin-transform-optional-chaining"
                ]
            },
            build: {
                files: {
                    '.tmp/scripts-b.js': ['.tmp/scripts.js']
                }
            }
        },

        processhtml: {
            options: {
                data: {
                    message: '<%= gruntConfigs.hash %>',
                    staticUrl: '<%= gruntConfigs.staticUrl %>',
                    apiUrl: '<%= gruntConfigs.apiUrl %>',
                    editorApiUrl: '<%= gruntConfigs.editorApiUrl %>',
                    editorUrl: '<%= gruntConfigs.editorUrl %>',
                    id: '<%= gruntConfigs.id %>',
                    gaCode: '<%= gruntConfigs.gaCode %>',
                    seoTitle: '<%= gruntConfigs.seo.title %>',
                    seoDescription: '<%= gruntConfigs.seo.description %>',
                    seoKeywords: '<%= gruntConfigs.seo.keywords %>',
                    googleToolId: '<%= gruntConfigs.googleToolId %>',
                    domainID: '<%= gruntConfigs.domainID %>',
                    robots: '<%= gruntConfigs.robots %>'
                },
                recursive: true
            },
            '<%= gruntConfigs.mainFolder %>': {
                files: {
                    '<%= gruntConfigs.mainFolder %>/index.tmp.html': ['app/index.html']
                }
            }
        },

        'string-replace': {
            dist: {
                files: {
                    '.tmp/scripts.js': ['.tmp/scripts.js']
                },
                options: {
                    replacements: [
                        {
                            pattern: /REPLACE_API_URL/i,
                            replacement: '<%= gruntConfigs.apiUrl %>'
                        },
                        {
                            pattern: /REPLACE_API_URL_EDITOR/i,
                            replacement: '<%= gruntConfigs.editorApiUrl %>'
                        },
                        {
                            pattern: /REPLACE_AUTH_URL/i,
                            replacement: '<%= gruntConfigs.authUrl %>'
                        },
                        {
                            pattern: /REPLACE_STATIC_URL/i,
                            replacement: '<%= gruntConfigs.staticUrl %>'
                        },
                        {
                            pattern: /REPLACE_SOCKET_URL/i,
                            replacement: '<%= gruntConfigs.socketUrl %>'
                        },
                        {
                            pattern: /REPLACE_EDITOR_URL/i,
                            replacement: '<%= gruntConfigs.editorUrl %>'
                        }
                    ]
                }
            }
        },

        fetchJson: {
            options: {
                method: 'GET'
            },
            files: {
                '<%= gruntConfigs.mainFolder %>/snapshots/tmp.json':
                    'https://static.digitalprint.pro/' +
                    grunt.option('id') +
                    '/sitemaps/' +
                    grunt.option('domainID') +
                    '.json'
            }
        },

        htmlSnapshot: {
            all: {
                options: {
                    snapshotPath:
                        '<%= gruntConfigs.mainFolder %>/snapshots/' +
                        grunt.option('id') +
                        '/' +
                        grunt.option('domainID') +
                        '/',
                    sitePath: grunt.option('site'),
                    fileNamePrefix: '',
                    msWaitForPages: 3000,
                    sanitize: function (requestUri) {
                        if (/\/$/.test(requestUri)) {
                            return '_';
                        } else {
                            return requestUri.replace(/\//g, '_');
                        }
                    },
                    removeScripts: false,
                    removeLinkTags: false,
                    removeMetaTags: false,
                    replaceStrings: [],
                    bodyAttr: 'data-prerendered',
                    urls: grunt.file.readJSON('copy_prod/tmp.json'),
                    cookies: [
                        { path: '/', lang: 'pl', value: 'en-gb' }
                    ],
                    pageOptions: {
                        viewportSize: {
                            width: 1200,
                            height: 800
                        }
                    }
                }
            }
        }
    });

    grunt.registerTask('build', [
        'clean',
        'sails-linker',
        'less:prod',
        'copy:build',
        'concat',
        'string-replace',
        'babel:build',
        'ngAnnotate',
        'uglify:build',
        'replace:stylefonts-prod',
        'postcss:prod',
        'processhtml'
    ]);

    grunt.registerTask('serve', [
        'sails-linker',
        'less:dev',
        'copy:build-dev',
        'replace:stylefonts',
        'express:dev',
        'watch',
        'processhtml'
    ]);

    grunt.registerTask('serve-demo', [
        'express:demo',
        'watch:demo'
    ]);

    grunt.registerTask('serve-dev2', [
        'express:dev',
        'watch'
    ]);

    grunt.registerTask('serve-https', [
        'express:https',
        'watch'
    ]);

    grunt.registerTask('serve-prod', [
        'build',
        'express:prod',
        'watch'
    ]);

    grunt.registerTask('serve-prod2', [
        'rename:prod2',
        'express:prod',
        'watch:prod'
    ]);

    grunt.registerTask('serve-ng2', [
        'express:ng2',
        'watch'
    ]);

    grunt.registerTask('minify', [
        'clean',
        'concat',
        'ngAnnotate',
        'babel:build'
    ]);

    grunt.registerTask('deploy-ftp', [
        'build',
        'copy:deploy',
        'rename:deploy' // tu potrzebna była konfiguracja rename:deploy
    ]);

    grunt.registerTask('deploy-cloud', [
        'build'
    ]);

    grunt.registerTask('pre-render', [
        'fetchJson',
        'htmlSnapshot'
    ]);

    grunt.registerTask('default', ['serve']);

    grunt.registerTask('test', ['processhtml']);
};
