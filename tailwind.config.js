/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/*.html',
    './templates/**/*.html',
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
    './node_modules/flowbite/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily:{
        'sans': ["Figtree", "serif"],
      },
      maxWidth: {
        '8xl': '96rem',
      }
    },
  },
  plugins: [
    require('flowbite/plugin')({
      charts: true,
    }),
  ],
}



