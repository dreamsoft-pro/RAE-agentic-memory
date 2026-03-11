javascript
// Karma configuration file, see link for more information
// https://karma-runner.github.io/1.0/config/configuration-file.html

module.exports = function(config) {
  config.set({
    frameworks: ['jasmine'],
    files: [
      { pattern: 'src/**/*.ts', watched: true, included: false, served: true },
      { pattern: 'src/**/*.js', watched: true, included: false, served: true },
      { pattern: 'test/**/*.spec.ts', watched: true, included: true, served: true }
    ],
    exclude: [],
    preprocessors: {
      'src/**/*.ts': ['typescript'],
      'test/**/*.spec.ts': ['typescript']
    },
    typescriptPreprocessor: {
      options: {
        compilerOptions: {
          module: 'commonjs',
          target: 'es6'
        }
      },
      transformPath: function(path) {
        return path.replace(/\.ts$/, '.js');
      }
    },
    reporters: ['progress'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    browsers: ['Chrome'],
    singleRun: false
  });
};
