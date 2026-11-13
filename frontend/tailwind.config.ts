import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./features/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        space: {
          950: "#05070e",
          900: "#0a0f1d",
          800: "#11192e",
        },
        mars: {
          500: "#e05a33",
          600: "#c8431c",
          400: "#f27a54",
        },
      },
    },
  },
  plugins: [],
};
export default config;
