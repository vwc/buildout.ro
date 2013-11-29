/* jshint node: true */
'use strict';

module.exports = function (grunt) {

    // load all grunt tasks
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

    // Project configuration.
    grunt.initConfig({

        // Metadata.
        pkg: grunt.file.readJSON('package.json'),
        banner: '/*!\n' +
                  '* RoConsulting v<%= pkg.version %> by Ade25\n' +
                  '* Copyright <%= pkg.author %>\n' +
                  '* Licensed under <%= pkg.licenses %>.\n' +
                  '*\n' +
                  '* Designed and built by ade25\n' +
                  '*/\n',
        jqueryCheck: 'if (!jQuery) { throw new Error(\"Bootstrap requires jQuery\") }\n\n',

        // Task configuration.
        clean: {
            dist: ['dist']
        },

        jshint: {
            options: {
                jshintrc: 'js/.jshintrc'
            },
            gruntfile: {
                src: 'Gruntfile.js'
            },
            src: {
                src: ['js/*.js']
            },
            test: {
                src: ['js/tests/unit/*.js']
            }
        },

        concat: {
            options: {
                banner: '<%= banner %><%= jqueryCheck %>',
                stripBanners: false
            },
            dist: {
                src: [
                    'bower_components/jquery/jquery.js',
                    'bower_components/modernizr/modernizr.js',
                    'bower_components/bootstrap/dist/js/bootstrap.js',
                    'js/main.js'
                ],
                dest: 'dist/js/<%= pkg.name %>.js'
            },
            theme: {
                src: [
                    'bower_components/bootstrap/dist/js/bootstrap.js',
                    'js/main.js'
                ],
                dest: 'dist/js/main.js'
            }
        },

        uglify: {
            options: {
                banner: '<%= banner %>'
            },
            dist: {
                src: ['<%= concat.dist.dest %>'],
                dest: 'dist/js/<%= pkg.name %>.min.js'
            }
        },

        recess: {
            options: {
                compile: true
            },
            theme: {
                src: ['less/styles.less'],
                dest: 'dist/css/styles.css'
            },
            min: {
                options: {
                    compress: true
                },
                src: ['less/styles.less'],
                dest: 'dist/css/styles.min.css'
            }
        },

        copy: {
            fonts: {
                expand: true,
                flatten: true,
                cwd: 'bower_components/',
                src: ['font-awesome/font/*'],
                dest: 'assets/fonts/'
            },
            templates: {
                expand: true,
                flatten: true,
                src: ['_site/*.html'],
                dest: 'dist/'
            }
        },
        imagemin: {
            theme: {
                files: [{
                    expand: true,
                    cwd: 'assets/img/',
                    src: ['*.{png,jpg,gif}'],
                    dest: 'dist/img'
                }]
            }
        },
        rev: {
            options:  {
                algorithm: 'sha256',
                length: 8
            },
            files: {
                src: ['dist/**/*.{js,css,png,jpg}']
            }
        },
        qunit: {
            options: {
                inject: 'js/tests/unit/phantom.js'
            },
            files: ['js/tests/*.html']
        },

        connect: {
            server: {
                options: {
                    port: 3000,
                    base: '.'
                }
            }
        },
        jekyll: {
            theme: {}
        },

        sed: {
            'compile-template-index': {
                path: 'dist/index.html',
                pattern: '../assets/',
                replacement: '/++theme++ro.sitetheme/assets/'
            },
            'compile-template-signin': {
                path: 'dist/signin.html',
                pattern: '../../assets/',
                replacement: '/++theme++ro.sitetheme/assets/'
            },
            'compile-template-theme': {
                path: 'dist/theme.html',
                pattern: '../../assets/',
                replacement: '/++theme++ro.sitetheme/assets/'
            },
            'compile-template-frontpage': {
                path: 'dist/frontpage.html',
                pattern: '../../assets/',
                replacement: '/++theme++ro.sitetheme/assets/'
            },
            'compile-template-work-fm': {
                path: 'dist/work-fm.html',
                pattern: '../../assets/',
                replacement: '/++theme++ro.sitetheme/assets/'
            },
            'compile-template-consultingm': {
                path: 'dist/consulting.html',
                pattern: '../../assets/',
                replacement: '/++theme++ro.sitetheme/assets/'
            }
        },

        validation: {
            options: {
                reset: true
            },
            files: {
                src: ['_gh_pages/**/*.html']
            }
        },

        watch: {
            src: {
                files: '<%= jshint.src.src %>',
                tasks: ['jshint:src', 'qunit']
            },
            test: {
                files: '<%= jshint.test.src %>',
                tasks: ['jshint:test', 'qunit']
            },
            recess: {
                files: 'less/*.less',
                tasks: ['recess']
            },
            templates: {
                files: '*.html',
                tasks: ['jekyll:theme']
            }
        }
    });


    // These plugins provide necessary tasks.
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-connect');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-qunit');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-html-validation');
    grunt.loadNpmTasks('grunt-jekyll');
    grunt.loadNpmTasks('grunt-recess');
    grunt.loadNpmTasks('grunt-rev');
    grunt.loadNpmTasks('grunt-sed');
    grunt.loadNpmTasks('browserstack-runner');

    // Copy jekyll generated templates and rename for diazo
    grunt.registerTask('copy-templates', '', function () {
        grunt.file.copy('_site/index.html', 'dist/index.html');
        grunt.file.copy('_site/signin/index.html', 'dist/signin.html');
        grunt.file.copy('_site/theme/index.html', 'dist/theme.html');
        grunt.file.copy('_site/frontpage/index.html', 'dist/frontpage.html');
        grunt.file.copy('_site/consulting/index.html', 'dist/consulting.html');
        grunt.file.copy('_site/work-fm/index.html', 'dist/work-fm.html');
    });

    // Docs HTML validation task
    grunt.registerTask('validate-html', ['jekyll', 'validation']);

    // Test task.
    var testSubtasks = ['dist-css', 'jshint', 'qunit', 'validate-html'];

    grunt.registerTask('test', testSubtasks);

    // JS distribution task.
    grunt.registerTask('dist-js', ['concat', 'uglify']);

    // CSS distribution task.
    grunt.registerTask('dist-css', ['recess']);

    // Assets distribution task.
    grunt.registerTask('dist-assets', ['copy']);

    // Cache buster distribution task.
    grunt.registerTask('dist-cb', ['rev']);

    // Template distribution task.
    grunt.registerTask('dist-templates', ['jekyll:theme', 'copy-templates']);

    // Full distribution task.
    grunt.registerTask('dist', ['clean', 'dist-css', 'dist-js', 'dist-templates', 'sed']);

    // Default task.
    grunt.registerTask('default', ['test', 'dist']);
};