// Path: tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './core/templates/**/*.html'
  ],
  theme: {
    extend: {
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            // --- НАШИ ИЗМЕНЕНИЯ ---
            'p': { // Стили для параграфов
              fontSize: '1.125rem', // 18px
              lineHeight: '1.75rem',
            },
            'li': { // Стили для элементов списка
              fontSize: '1.125rem', // 18px
              lineHeight: '1.75rem',
            },
            // --------------------
            // Здесь можно переопределить и другие стили, например, цвет ссылок
            'a': {
              color: theme('colors.cyan.400'),
              '&:hover': {
                color: theme('colors.cyan.300'),
              },
            },
          },
        },
      }),
    },
  },
  plugins: [
      require('@tailwindcss/typography'),
  ],
}