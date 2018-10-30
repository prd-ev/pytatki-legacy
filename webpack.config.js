const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = (env, argv) => {
  const devMode = argv.mode !== 'production';
  return {
    plugins: [
      new MiniCssExtractPlugin({
        filename: "style.css"
      })
    ],
    entry: ["@babel/polyfill","./src/js/index.js"],
    output: {
      path: path.resolve(__dirname, "./pytatki/static"),
      filename: "bundle.js"
    },
    devtool: "source-map",
    module: {
      rules: [{
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          loader: "babel-loader",
        },
        {
          test: /\.s?css$/,
          exclude: [/node_modules/,/global.scss/],
          use: [
            devMode ? "style-loader" : MiniCssExtractPlugin.loader,
            "css-loader?modules&localIdentName=[local]---[hash:base64:5]",
            "sass-loader",
            "postcss-loader"
          ]
        },
        {
          test: /global.scss/,
          use: [
            devMode ? "style-loader" : MiniCssExtractPlugin.loader,
            "css-loader",
            "sass-loader",
            "postcss-loader"
          ]
        }
      ]
    },
  };
};