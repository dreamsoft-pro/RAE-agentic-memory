module.exports = function (grunt) {

    var path = require('path');

    var config = require('./configs/prod.config')({});
    var appOptions = config.get();

    var gruntConfigs = {
        'apiUrl': appOptions.apiUrl,
        'authUrl': appOptions.authUrl,
        'staticUrl': appOptions.staticUrl,
        'socketUrl': appOptions.socketUrl,
        'editorUrl': appOptions.editorUrl,
    };



    if( grunt.option('apiUrl') !== undefined ) {
        gruntConfigs.apiUrl = grunt.option('apiUrl');
    }

    if( grunt.option('authUrl') !== undefined ) {
        gruntConfigs.authUrl = grunt.option('authUrl');
    }

    if( grunt.option('staticUrl') !== undefined ) {
        gruntConfigs.staticUrl = grunt.option('staticUrl');
    }

    if( grunt.option('socketUrl') !== undefined ) {
        gruntConfigs.socketUrl = grunt.option('socketUrl');
    }

    if( grunt.option('editorUrl') !== undefined ) {
            gruntConfigs.editorUrl = grunt.option('editorUrl');
        }

    console.log(gruntConfigs);

    require('load-grunt-tasks')(grunt);
    require('time-grunt')(grunt);

    grunt.initConfig({
        gruntConfigs: gruntConfigs,
        watch: {
            less: {
                files: [
                    'app/assets/less/**/*.less'
                ],
                tasks: [
                    'less:dev'
                ]
            },
            livereload: {
                options: {
                    livereload: 35730,
                    debounceDelay: 500
                },
                files: [
                    'app/digitalprint.css'
                ]
            }
        },

        express: {
            dev: {
                options: {
                    bases: 'app',
                    port: 80,
                    server: path.resolve('./index')

                }
            },
            prod: {
                options: {
                    bases: 'dist',
                    port: 9010,
                    server: path.resolve('./index.prod')
                }
            }
        },

        clean: {
            js: ['./dist', './.tmp']
        },

        less: {
            dev: {
                files: {
                    './app/digitalprint.css': './app/assets/less/digitalprint.less'
                }
            },
            prod: {
                files: {
                    './dist/digitalprint.css': './app/assets/less/digitalprint.less'
                }
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
                    './app/index.html': ['app/src/**/*.js','app/shared/**/*.js']
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
            }
        },

        copy: {
            build: {
                files: [
                    {
                        expand: true,
                        dest: 'dist/',
                        cwd: '.',
                        src: [
                            'node_modules/{bootstrap-datepicker,angular-ui-notification,bootstrap-treeview,angular-bootstrap-colorpicker,jquery,bootstrap,lodash,angular,angular-ui-router,restangular,angular-local-storage,angular-bootstrap,angular-bootstrap,angular-bootstrap-colorpicker,angular-animate,angular-breadcrumb,angular-translate,angular-translate-loader-static-files,angular-cookies,angular-ui-sortable,textangular,angular-socket-io,angular-file-upload,angularjs-slider,angular-ui-notification,flag-icon-css,font-awesome}/**/*.{js,css,map,png,jpg,woff,woff2,ttf,less}'
                        ]
                    },
                    {
                        expand: true,
                        dest: 'app/',
                        cwd: '.',
                        src: [
                            'node_modules/{bootstrap-datepicker,angular-ui-notification,bootstrap-treeview,angular-bootstrap-colorpicker,jquery,bootstrap,lodash,angular,angular-ui-router,restangular,angular-local-storage,angular-bootstrap,angular-bootstrap,angular-bootstrap-colorpicker,angular-animate,angular-breadcrumb,angular-translate,angular-translate-loader-static-files,angular-cookies,angular-ui-sortable,textangular,angular-socket-io,angular-file-upload,angularjs-slider,angular-ui-notification,flag-icon-css,font-awesome}/**/*.{js,css,map,png,jpg,woff,woff2,ttf,less}'
                        ]
                    },
                    {
                        expand: true,
                        dest: 'dist/',
                        cwd: 'app/',
                        src: [
                            'assets/{helpers,metronic,socket\.io}/**/*.{js,css,map,png,jpg,woff,woff2,ttf}'
                        ]
                    },
                    {
                        expand: true,
                        dest: 'dist/',
                        cwd: 'app/',
                        src: [
                            '*.{ico,png,txt}',
                            '.htaccess',
                            '*.html',
                            '{src,views,shared}/**/*.html'
                        ]
                    },
                    {
                        expand: true,
                        dest: 'dist/',
                        cwd: '.',
                        dot: true,
                        src: [
                            'node_modules/flag-icon-css/flags/*/*.svg'
                        ]
                    },
                    {
                        expand: true,
                        dest: 'dist/',
                        cwd: 'app/',
                        dot: true,
                        src: [
                            'assets/jsgantt/**/*.{js,css}'
                        ]
                    },
                    {
                        expand: true,
                        dest: 'dist/',
                        cwd: 'app/',
                        dot: true,
                        src: [
                            'assets/dhtmlxgantt/**/*.{js,css}'
                        ]
                    }
                ]
            },
            dev: {
                files: [
                    {
                        expand: true,
                        dest: 'app',
                        cwd: '.',
                        src: [
                            'node_modules/{bootstrap-datepicker,angular-ui-notification,bootstrap-treeview,angular-bootstrap-colorpicker,jquery,bootstrap,lodash,angular,angular-ui-router,restangular,angular-local-storage,angular-bootstrap,angular-bootstrap,angular-bootstrap-colorpicker,angular-animate,angular-breadcrumb,angular-translate,angular-translate-loader-static-files,angular-cookies,angular-ui-sortable,textangular,angular-socket-io,angular-file-upload,angularjs-slider,angular-ui-notification,flag-icon-css,font-awesome}/**/*.{js,css,map,png,jpg,woff,woff2,ttf,less}'
                        ]
                    },
                    {
                        expand: true,
                        dest: 'dist/assets',
                        cwd: '.',
                        dot: true,
                        src: [
                            'node_modules/flag-icon-css/flags/*/*.svg'
                        ]
                    }
                    ]
            }
        },

        concat: {
            options: {
                separator: ';'
            },
            dist: {
                src: [
                    'app/*.js',
                    'app/routes/**/*.js',
                    'app/shared/**/*.js',
                    'app/assets/helpers/**/*.js',
                    'app/src/**/*.js',
                    'app/services/**/*.js'
                ],
                dest: '.tmp/scripts.js'
            }
        },
        babel: {
            options: {
                sourceMap: false,
                presets: ['@babel/preset-env'],
                minified: true,
                plugins: ["@babel/plugin-proposal-nullish-coalescing-operator"]
            },
            build: {
                files: {
                    '.tmp/scripts-b.js': ['.tmp/scripts.js'],

                }
            }
        },
        ngAnnotate: {
            dist: {
                files: {
                    '.tmp/scripts-b.js': ['.tmp/scripts-b.js']
                }
            }
        },

        uglify: {
            options: {},
            build: {
                files: {
                    'dist/scripts/scripts.min.js': ['.tmp/scripts-b.js']
                }
            }
        },

        processhtml: {
            options: {
                data: {
                    message: 'Hello world!'
                }
            },
            dist: {
                files: {
                    'dist/index.html': ['dist/index.html']
                }
            }
        },

        'string-replace': {
            dist: {
                files: {
                    'dist/index.html': ['app/index.html'],
                    'dist/scripts/scripts.min.js': ['dist/scripts/scripts.min.js']
                },
                options: {
                    replacements: [{
                        pattern: /\/assets/ig,
                        replacement: 'assets'
                    },
                        {
                            pattern: /\/digitalprint\.css/i,
                            replacement: 'digitalprint\.css'
                        },
                        {
                            pattern: /REPLACE_API_URL/i,
                            replacement: '<%= gruntConfigs.apiUrl %>'
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
                        }]
                }
            }
        }


    });

    grunt.registerTask('build', [
        'clean',
        'sails-linker',
        'copy:build',
        'less:prod',
        'concat',
        'babel:build',
        'ngAnnotate',
        'uglify:build',
        'string-replace',
        'processhtml'
    ]);

    grunt.registerTask('auto-build', [
        'clean',
        'sails-linker',
        'copy:build',
        'less:prod',
        'concat',
        'babel:build',
        'ngAnnotate',
        'uglify:build',
        'string-replace',
        'processhtml'
    ]);

    grunt.registerTask('serve', [
        'express:prod',
        'watch'
    ]);
    grunt.registerTask('serve-dev', [
        'copy:dev',
        'less:dev',
        'express:dev',
        'watch'
    ]);
    grunt.registerTask('minify', [
        'clean',
        'concat',
        'ngAnnotate',
        'uglify:build'
    ]);

    grunt.registerTask('default', ['serve'])

};
