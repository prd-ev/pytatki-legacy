module.exports = function(api) {
  api.cache(true);
  const presets = [
    [
      "@babel/env",
      {
        targets: {
          chrome: "68",
          firefox: "61",
          safari: "11.1",
          edge: "17",
          opera: "55",
          android: "4.4.4",
          ios: "11.2"
        },
        useBuiltIns: "usage"
      }
    ],
    "@babel/react"
  ];

  const plugins = ["@babel/plugin-proposal-class-properties"];

  return {
    presets,
    plugins
  };
};
