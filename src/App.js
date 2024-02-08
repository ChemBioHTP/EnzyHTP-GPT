import React, { useState, useEffect } from "react";
import "./App.css";
import ElementLandingScreen from "./screens/Login/landingscreen";
import ElementLoginScreen from "./screens/Login/loginscreen";
import { BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import ApiKeyScreen from "./screens/Login/apikeyscreen";
import ForgotpwdScreen from "./screens/Login/forgotpwdscreen";
import Cookies from 'js-cookie';
import ResetpwdScreen from "./screens/Login/resetpwdscreen";

function App() {
  const [data, setData] = useState([{}]);

  const PrivateRoute = ({ element }) => {
    const isLoggedIn = Cookies.get('userToken');

    return isLoggedIn ? (
      element
    ) : (
      <Navigate to="/" replace={true} state={{ from: window.location.pathname }} />
    );
  };

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<ElementLandingScreen />} />
        <Route path="/login" element={<ElementLoginScreen />} />
        <Route path="/key" element={<PrivateRoute element={<ApiKeyScreen />}/>} />
        <Route path="/forgotpwd" element={<ForgotpwdScreen />} />
        <Route path="/resetpwd" element={<ResetpwdScreen />} />
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
