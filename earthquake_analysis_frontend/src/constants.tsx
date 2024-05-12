export const BACKEND_API_URL = "http://localhost:8000/api/";

export const magnitudeColors = {
  minor: "cyan",
  light: "green",
  moderate: "#ff0000",
  strong: "#d60000",
  major: "#b00000",
  great: "#690000",
};
export const magnitudeColorsName = [
  "Minor < 3.9",
  "Light < 4.9",
  "Moderate < 5.9",
  "Strong < 6.9",
  "Major < 7.9",
  "Great 8.0+",
];
export const magnitudeColorsPicker = (magnitude: number) => {
  if (magnitude < 3.9) {
    return magnitudeColors.minor;
  } else if (magnitude < 4.9) {
    return magnitudeColors.light;
  } else if (magnitude < 5.9) {
    return magnitudeColors.moderate;
  } else if (magnitude < 6.9) {
    return magnitudeColors.strong;
  } else if (magnitude < 7.9) {
    return magnitudeColors.major;
  } else {
    return magnitudeColors.great;
  }
};
