module.exports = {
  extends: ['eslint:recommended', 'plugin:react/recommended'],
  plugins: ['prettier', 'react'],
  rules: {
    'prettier/prettier': 'off',
    'no-unused-vars': 'off',
    'no-undef': 'off',
    'react/react-in-jsx-scope': 'off',
    'react/no-unknown-property': 'off',
    // 'react/prop-types': 'off',
  },
  //支持es6
  parserOptions: {
    ecmaVersion: 6,
  },
  env: {
    node: true,
  },
};
