// config-overrides.js
const path = require('path');

module.exports = function override(config, env) {
  // 修改输出目录
  config.output.path = path.resolve(__dirname, 'build-custom');
  // 添加一个自定义的loader规则
  config.module.rules.push({
    test: /\.custom\.css$/,
    use: ['style-loader', 'css-loader'],
  });

  // 启用Webpack缓存
  config.cache = true;

  return config;
};
