import React, { useState, useEffect } from "react";
import "./App.css";
import ElementLandingScreen from "./screens/Login/landingscreen";
import ElementLoginScreen from "./screens/Login/loginscreen";
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import ApiKeyScreen from "./screens/Login/apikeyscreen";

function App() {
  const [data, setData] = useState([{}]);

  // useEffect(() => {
  //   fetch("/members")
  //     .then((res) => res.json())
  //     .then((data) => setData(data));
  // });

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<ElementLandingScreen />} />
        <Route path="/login" element={<ElementLoginScreen />} />
        <Route path="/key" element={<ApiKeyScreen />} />
      </Routes>
    </div>    
    
      // {/* {typeof data.members === "undefined" ? (
      //   <p>Loading...</p>
      // ) : (
      //   data.members.map((member, i) => <p key={i}>{member}</p>)
      // )} */}
  );
}

export default App;
