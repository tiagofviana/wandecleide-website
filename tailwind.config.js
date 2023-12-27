/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin')

module.exports = {
  mode: 'jit',
  content: [
    '.\\src\\**\\*.{html,js}',
    '.\\src\\**\\forms.py'
  ],
  theme: {
    extend: {
      fontFamily: {
        'default': ['Nunito', 'sans-serif'],
        'handwrite': ['Lobster Two', 'sans-serif'],
      },

      brightness: {
        30: '.30',
      },

      maxWidth: {
        'screen-3xl': '2160px',
      },
      
      animation: {
        'fadeIn': 'fadeIn .8s ease-in',
        'fadeIn-right': 'fadeIn-right 1.2s ease-in',
        'fadeIn-bottom': 'fadeIn-bottom 1.2s ease-in',
      },
    }
  },
  
  plugins: [
    require('./plugins/animationDelay'),
    require('./plugins/textShadow'),
  ]
}