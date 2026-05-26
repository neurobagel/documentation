/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './docs/overrides/**/*.html',
    './docs/**/*.md'
  ],
  theme: {
    extend: {
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'fade-in-up': 'fadeInUp 0.8s ease-out forwards',
        'fade-in': 'fadeIn 1s ease-out forwards',
        'spin-slow': 'spin 20s linear infinite',
        'aurora': 'aurora 4s ease-in-out infinite',
        'marquee': 'marquee 50s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        aurora: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        marquee: {
          from: { transform: 'translateX(0)' },
          to: { transform: 'translateX(calc(-100% - 2.5rem))' }, // Shifts left by full width (-100%) plus the gap (-2.5rem) for a seamless loop
        }
      }
    },
  },
  plugins: [],
}
