/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        bg: "#05070d",        // main background
        panel: "#0b1220",     // cards / panels
        accent: "#22c55e",    // speed line / highlights
        warning: "#ef4444",   // alerts
        muted: "#94a3b8",     // secondary text
      },
      boxShadow: {
        glow: "0 0 25px rgba(34,197,94,0.25)",
        panel: "0 10px 30px rgba(0,0,0,0.6)",
      },
      borderRadius: {
        xl: "14px",
      },
    },
  },
  plugins: [],
};
