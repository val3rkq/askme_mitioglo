const plugin = require('tailwindcss/plugin');

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './**/*.html',
    ],
    theme: {
        extend: {
            backgroundImage: {
                'image': "bg-[url('./../static/img/background.png')]",
            },
            colors: {
                'primary': 'black',
                // 'primary': '#14532d',
                'secondary': '#9ca3af',
                'selected': 'white',
                'text': 'black',
                'tag': '#374151',
                'error': '#ef4444'
            },
            fontSize: {
                '2.5xl': '1.875rem',
            },
            fontFamily: {
                ubuntu: ['Ubuntu', 'sans-serif'],
            },
            boxShadow: {
                'custom': '0 6px 10px rgba(0, 0, 0, 0.2)',
                'custom-footer': '0 -6px 10px rgba(0, 0, 0, 0.2)',
            },
        },
    },
    plugins: [
        plugin(function ({ addUtilities }) {
            addUtilities({
                '.transition-custom': {
                    transitionProperty: 'all',
                    transitionDuration: '250ms',
                    transitionTimingFunction: 'ease-in-out',
                },
            });
        }),
    ],
}  