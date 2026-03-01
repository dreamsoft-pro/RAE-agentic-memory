module.exports = function (grunt) {

    var path = require('path');

    var config = require('./configs/prod.config')({});
    var appOptions = config.get();

    var gruntConfigs = {
        'apiUrl': appOptions.apiUrl,
        'authUrl': appOptions.authUrl,
        'staticUrl': appOptions.staticUrl,
        'socketUrl': appOptions.socketUrl
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
                    port: 9000,
                    server: path.resolve('./index')
                }
            },
            prod: {
                options: {
                    bases: 'dist',
                    port: 9010,
                    server: path.resolve('./index')
                }
            }
        },

        'bower-install-simple': {
            'prod': {
                options: {
                    production: true,
                    directory: "./app/assets/bower_components/"
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
                        cwd: 'app/',
                        src: [
                            'assets/{bower_components,helpers,metronic,socket\.io}/**/*.{js,css,map,png,jpg,woff,woff2,ttf}'
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
                        cwd: 'app/',
                        dot: true,
                        src: [
                            'assets/bower_components/flag-icon-css/flags/*/*.svg'
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

        ngAnnotate: {
            dist: {
                files: {
                    '.tmp/scripts.js': ['.tmp/scripts.js']
                }
            }
        },

        uglify: {
            options: {},
            build: {
                files: {
                    'dist/scripts/scripts.min.js': ['.tmp/scripts.js']
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

        prompt: {
            target: {
                options: {
                    questions: [
                        {
                            config: 'replaceApiUrl', // arbitrary name or config for any other grunt task
                            type: 'list', // list, checkbox, confirm, input, password
                            message: 'Select api URL for this build:', // Question to ask the user, function needs to return a string,
                            default: 'https://api.digitalprint.pro/', // default value if nothing is entered
                            choices: [
                                {name: 'https://api.dreamsoft.pro/', checked: true},
                                {name: 'https://dev2.dreamsoft.pro/'},
                                {name: 'https://acc.dreamsoft.pro/'}
                            ]
                        }
                    ],
                    then: function (results) {
                        gruntConfigs.apiUrl = results['replaceApiUrl'];
                    }
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
                        }]
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
        'ngAnnotate',
        'uglify:build',
        'prompt',
        'string-replace',
        'processhtml'
    ]);

    grunt.registerTask('auto-build', [
        'clean',
        'sails-linker',
        'less:prod',
        'copy:build',
        'concat',
        'ngAnnotate',
        'uglify:build',
        'string-replace',
        'processhtml'
    ]);

    grunt.registerTask('serve', [
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
