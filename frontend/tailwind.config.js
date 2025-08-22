/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'reach-blue': '#2563eb',
        'reach-orange': '#f97316',
        'reach-pink': '#ec4899',
        'reach-purple': '#8b5cf6',
        'warm-gray': {
          50: '#fafaf9',
          100: '#f5f5f4',
          200: '#e7e5e4',
          300: '#d6d3d1',
        }
      },
      fontFamily: {
        'child-friendly': ['Comic Neue', 'Quicksand', 'Nunito', 'sans-serif'],
      }
    },
  },
  plugins: [],
}