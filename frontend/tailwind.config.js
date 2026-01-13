/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: '#050510',
          panel: '#0a0a1a',
          primary: '#00f3ff',
          secondary: '#7000ff',
          alert: '#ff003c',
          success: '#00ff9d',
          text: '#e0e0e0',
          dim: '#606080'
        }
      },
      fontFamily: {
        mono: ['"Fira Code"', 'monospace'],
        sans: ['"Inter"', 'sans-serif']
      }
    },
  },
  plugins: [],
}
