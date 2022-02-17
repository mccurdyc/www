const path = require('path');
const { IgnorePlugin } = require('webpack');

module.exports = {
  mode: 'production',
  entry: './index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'read-gcs.bundle.js',
  },
  plugins: [
    new IgnorePlugin({
      resourceRegExp: /worker_threads/,
    }),
  ],
  // resolve: {
  //   fallback: {
  //     "assert": require.resolve("assert/"),
  //     "buffer": require.resolve("buffer/"),
  //     "constants": require.resolve("constants-browserify"),
  //     "crypto": require.resolve("crypto-browserify"),
  //     "http": require.resolve("stream-http"),
  //     "https": require.resolve("https-browserify"),
  //     "os": require.resolve("os-browserify/browser"),
  //     "path": require.resolve("path-browserify"),
  //     "querystring": require.resolve("querystring-es3"),
  //     "stream": require.resolve("stream-browserify"),
  //     "url": require.resolve("url/"),
  //     "net": require.resolve("net"),
  //     "tls": require.resolve("tls"),
  //     "util": require.resolve("util/"),
  //     "zlib": require.resolve("browserify-zlib"),
  //   },
  // },
  // externals: {
  //   '@google-cloud/storage': 'commonjs @google-cloud/storage'
  // },
};
