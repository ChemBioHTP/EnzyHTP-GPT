import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ElementLandingScreen from "./screens/Login/landingscreen";
import { ElementCreateTarget } from "./screens/CreateMutants/createmutants";
import { RunSimulation } from "./screens/RunSimulation/runsimulations";
import { ElementExperiments } from "./screens/UploadFile/uploadfile";

const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<ElementLandingScreen />} />
        <Route path="/upload_file" element={<ElementExperiments />} />
        <Route path="/create_mutants" element={<ElementCreateTarget />} />
        <Route path="/run_simulation" element={<RunSimulation />} />
      </Routes>
    </Router>
  );
};

export default AppRouter;
