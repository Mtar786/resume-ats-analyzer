import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Create React root and render the main component
const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);