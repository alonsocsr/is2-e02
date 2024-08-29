/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/*.html',
    './templates/**/*.html',
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily:{
        'sans': ["Lora", "serif"],
      }
    },
  },
  plugins: [],
}

