const plugin = require('tailwindcss/plugin')

module.exports = plugin(function({ matchUtilities, theme }){
    matchUtilities({
        'text-shadow': (value) => {
            return {textShadow: value}
        }
    }, {
        values: theme('textShadow')
    })
}, {
    theme: {
        textShadow: {
            DEFAULT: '2px 1px rgba(0,0,0,.7)',
        }
    }
})