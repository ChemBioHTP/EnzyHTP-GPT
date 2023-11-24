import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ElementLandingScreen from "./screens/Login/landingscreen";
import { ElementCreateTarget } from "./screens/CreateMutants/createmutants";

const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<ElementLandingScreen />} />
        <Route path="/create_mutants" element={<ElementCreateTarget />} />
        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
};

export default AppRouter;
