import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: { main: "#1976d2" },
    secondary: { main: "#f50057" },
    background: { default: "#f4f4f4" },
  },
  typography: {
    fontFamily: "Arial, sans-serif",
  },
});

export default theme;
