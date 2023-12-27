const plugin = require('tailwindcss/plugin')

module.exports = plugin(function({ matchUtilities, theme }){
    matchUtilities({
        'animation-delay': (value) => {
            return {animationDelay: value}
        }
    }, {
        values: theme('animationDelay')
    })
}, {
    theme: {
        animationDelay: {
            100: '100ms',
            200: '200ms',
            300: '300ms',
            400: '400ms',
            500: '500ms',
            600: '600ms',
            700: '700ms',
            800: '800ms',
            900: '900ms',
            1000: '1000ms',
            1100: '1100ms',
            1200: '1200ms',
        }
    }
})