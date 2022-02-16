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
  // externals: {
  //   '@google-cloud/storage': 'commonjs @google-cloud/storage'
  // },
};
