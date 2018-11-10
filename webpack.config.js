const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = (env, argv) => {
  const devMode = argv.mode !== "production";
  return {
    plugins: [
      new MiniCssExtractPlugin({
        filename: "style.css"
      })
    ],
    entry: {
      vendor: ['react', 'react-dom', 'prop-types', 'react-contextmenu'],
      app: ["./src/components/index.js"]
    },
    output: {
      path: path.resolve(__dirname, "./pytatki/static"),
      filename: "[name].bundle.js"
    },
    optimization: {
      splitChunks: {
        chunks: 'async'
      }
    },
    devtool: "source-map",
    module: {
      rules: [{
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          loader: "babel-loader",
          options: {
            cwd: "./"
          }
        },
        {
          test: /\.s?css$/,
          exclude: [/node_modules/, /global.scss/],
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
    }
  };
};