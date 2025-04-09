import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import SurveyList from './components/SurveyList';
import SurveyDetail from './components/SurveyDetail';
import CategoryAnalysis from './components/CategoryAnalysis';

// Create a custom theme with racing club colors
const theme = createTheme({
  palette: {
    primary: {
      main: '#2e3f7f', // Deep blue
      light: '#5e6baf',
      dark: '#001952',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#e5b80b', // Gold
      light: '#ffe94d',
      dark: '#ae8900',
      contrastText: '#000000',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
    text: {
      primary: '#333333',
    },
  },
  typography: {
    fontFamily: [
      'Roboto',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 20px 0 rgba(0,0,0,0.05)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="/surveys" element={<SurveyList />} />
          <Route path="/surveys/:id" element={<SurveyDetail />} />
          <Route path="/categories" element={<CategoryAnalysis />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
}

export default App;