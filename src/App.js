import React, { useState, useEffect } from "react";
import "./App.css";
import ElementLandingScreen from "./screens/Login/LandingScreen";
import ElementLoginScreen from "./screens/Login/LoginScreen";
import { BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';

import ElementExperiment from "./screens/Experiments/ExperimentPage/ElementExperiment";

function App() {

  return (
    <div className="App">
      <Routes>
        <Route path="/*" element={<ElementLandingScreen />} />
        
        <Route path="/exp/*" element={<ElementExperiment />} />
      </Routes>
    </div>    
  );
}

export default App;
