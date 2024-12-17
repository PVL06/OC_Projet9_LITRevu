/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
    "./authentication/templates/**/*.html",
    "./review/templates/review/*.html",
    "./review/templates/review/partials/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
