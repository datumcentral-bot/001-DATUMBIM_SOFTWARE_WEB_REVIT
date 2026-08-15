/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        datumbim: {
          bg: '#1e1e1e',
          surface: '#252526',
          border: '#3e3e42',
          accent: '#0078d4',
          text: '#cccccc',
          textSecondary: '#969696',
          ribbon: '#2d2d30',
        }
      }
    },
  },
  plugins: [],
}
