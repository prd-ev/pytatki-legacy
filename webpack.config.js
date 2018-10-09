const path = require('path');

module.exports = {
  entry: "./js",
  output: {
    path: path.resolve(__dirname, "./pytatki/static"),
    filename: "bundle.js"
  },
  module: {
    rules: [{
      test: /\.(js|jsx)$/,
      exclude: /node_modules/,
      loader: "babel-loader",
    }]
  }
};