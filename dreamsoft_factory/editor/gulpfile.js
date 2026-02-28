const {series} = require('gulp');
var webpack = require('webpack');
var path = require('path');
var fs = require('fs');
var Q = require('q');
var handlebars = require("handlebars");
const {argv: args} = require("yargs");


function build(done) {
    var args = require('yargs').argv;
    const dateFormat = (n) => `${n}`.length === 2 ? `${n}` : `0${n}`
    const d = new Date();
    const versionStamp = `${d.getFullYear()}${dateFormat(d.getMonth() + 1)}${dateFormat(d.getDate())}${dateFormat(d.getHours())}${dateFormat(d.getMinutes())}`;

    function makeVersion(companyID, domain, frameworkUrl, backendUrl, authUrl, staticUrl, frontendUrl, versionStamp, forUser) {

        var defer = Q.defer();
        var user = false;
        var indexFiles = true;

        var indexFile = fs.readFileSync('./app/index_template.html', 'utf8');
        var templateData = {
            "companyID": companyID,
            versionStamp: versionStamp,
            script: 'editor_' + (forUser ? 'user' : 'admin') + '_' + versionStamp + '.min.js',
            userType: forUser ? 'user' : 'admin'
        };
        var template = handlebars.compile(indexFile);
        var result = template(templateData);

        var dir = __dirname + '/dist/';
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir);
        }

        fs.writeFileSync('./dist/index' + (forUser ? 'u' : 'a') + '.html', result);

        var compiler = webpack({
            mode: "development",
            entry: './app/index.js',
            devtool: 'source-map',
            output: {
                filename: 'editor_' + (forUser ? 'user' : 'admin') + '.min.js',
                path: path.resolve(__dirname, 'dist/')
            },

            plugins: [
                new webpack.DefinePlugin({
                    'EDITOR_ENV': {
                        user: forUser,
                        admin: !forUser,
                        companyID: companyID,
                        domain: domain,
                        frameworkUrl: frameworkUrl,
                        backendUrl: backendUrl,
                        authUrl: authUrl,
                        staticUrl: staticUrl,
                        templatesDir: "''",
                        frontendUrl: domain
                    }
                }),
                new webpack.DefinePlugin({
                    'process.env': {
                        NODE_ENV: JSON.stringify('production')
                    }
                }),
                /*new webpack.optimize.UglifyJsPlugin(),*/
            ],

            module: {

                rules: [

                    {
                        test: /\.js$/,
                        loader: 'babel-loader'
                    }

                ]

            }

        });

        compiler.run((err, stats) => {
            if (err) {
                console.error(err);
                defer.reject(err);
            } else {
                defer.resolve();
            }
        });

        return defer.promise;

    }

    makeVersion(args.companyID,
        JSON.stringify(args.domain),
        JSON.stringify(args.frameworkUrl),
        JSON.stringify(args.backendUrl),
        JSON.stringify(args.authUrl),
        JSON.stringify(args.staticUrl),
        JSON.stringify(args.frontendUrl),
        versionStamp, false).then(
        makeVersion(args.companyID,
            JSON.stringify(args.domain),
            JSON.stringify(args.frameworkUrl),
            JSON.stringify(args.backendUrl),
            JSON.stringify(args.authUrl),
            JSON.stringify(args.staticUrl),
            JSON.stringify(args.frontendUrl),
            versionStamp, true).then(() => {
            ['editor_user', 'editor_admin'].forEach(file => {
                fs.copyFileSync('./dist/' + file + '.min.js', './app/' + file + '_' + versionStamp + '.min.js')
            });
            ['indexu.html', 'indexa.html'].forEach(file => {
                fs.copyFileSync('./dist/' + file, './app/' + file)
            })
            done()
        }),
        (err) => {
            console.error(err);

        }
    );
    done()
};


function clean(done) {
    fs.readdir('./app', (err, files) => {
        if (!err) {
            const patterns = ['editor_user_', 'editor_admin_', 'indexu.html', 'indexa.html']
            files.forEach(file => {
                patterns.forEach(pattern => {
                    if (file.indexOf(pattern) > -1) {
                        fs.unlinkSync('./app/' + file)
                        console.log('removed', file)
                    }
                })

            })
        }
        done()
    })

}

exports.clean = clean;
exports.build = build;
exports.default = series(clean, build)
