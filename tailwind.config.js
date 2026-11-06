/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          navy: '#101D35',
          'navy-dark': '#0A1324',
          'navy-light': '#1A2C4E',
          blue: '#3478F6',
          'blue-dark': '#2563EB',
          'blue-light': '#60A5FA',
          teal: '#14B8A6',
          'teal-dark': '#0D9488',
          'teal-light': '#CCFBF1',
          cyan: '#0EA5E9',
          danger: '#EF4444',
          'danger-dark': '#DC2626',
          'danger-light': '#FEE2E2',
          warning: '#F59E0B',
          'warning-light': '#FEF3C7',
          success: '#10B981',
          'success-light': '#D1FAE5',
          bg: '#F8FAFC',
          card: '#FFFFFF',
          border: '#E2E8F0',
          muted: '#64748B'
        }
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace']
      },
      boxShadow: {
        'subtle': '0 1px 3px 0 rgba(16, 29, 53, 0.05), 0 1px 2px 0 rgba(16, 29, 53, 0.03)',
        'card': '0 4px 20px -2px rgba(16, 29, 53, 0.06), 0 2px 6px -1px rgba(16, 29, 53, 0.04)',
        'card-hover': '0 16px 32px -4px rgba(16, 29, 53, 0.12), 0 6px 12px -2px rgba(16, 29, 53, 0.06)',
        'modal': '0 25px 50px -12px rgba(16, 29, 53, 0.25)',
        'glow-blue': '0 0 20px -3px rgba(52, 120, 246, 0.35)',
        'glow-teal': '0 0 20px -3px rgba(20, 184, 166, 0.35)'
      }
    },
  },
  plugins: [],
}
