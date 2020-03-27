import Typography from "typography";

const typography = new Typography({
  baseFontSize: "18px",
  baseLineHeight: 1.45,
  headerFontFamily: ["Palanquin", "sans-serif"],
  bodyFontFamily: ["Palanquin", "sans-serif"],
});

// Insert styles directly into the <head>
typography.injectStyles();

export default typography;
