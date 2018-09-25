var webpack = require("webpack");
module.exports = {
  entry: ["./js/index.js"],
  output: {
    path: __dirname + "/static",
    filename: "bundle.js"
  },
  module: {
    loaders: [
      {
        test: /\.(js|jsx)$/,
        loader: "babel-loader",
        query: {
          presets: ["es2015", "react", "stage-2"],
          plugins: ["transform-class-properties"]
        }
      }
    ]
  },
  plugins: [],
};
