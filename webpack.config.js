var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: './assets/js/index',

    output: {
        path: path.resolve('./assets/bundles'),
        filename: '[name]-[hash].js'
    },

    plugins: [
        new BundleTracker({
            filename: './webpack-stats.json'
        })
    ],

    module: {
        rules: [
            {
                test: /\.tsx?$/,

                exclude: /node_modules/,
                loader: 'awesome-typescript-loader',
            }
        ]
    },

    resolve: {
        modules: ['node_modules'],

        extensions: ['.js', '.jsx', '.ts', '.tsx']
    },

    devtool: 'source-map'
};

