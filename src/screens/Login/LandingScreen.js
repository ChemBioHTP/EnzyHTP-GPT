import React from "react";
import { useNavigate } from "react-router-dom";
import ElementLoginScreen from "./LoginScreen";
import { BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import ApiKeyScreen from "./ApiKeyScreen";
import ForgotpwdScreen from "./ForgotPwdScreen";
import ResetpwdScreen from "./ResetPwdScreen";
import ElementSignUpScreen from "./SignUpScreen"
// Images and icons
import ellipse2 from "../../assets/images/Login/ellipse-2.svg";
import ellipse1 from "../../assets/images/Login/ellipse-1.svg";
import union from "../../assets/images/Login/union.svg";
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';
import hexagonDottedConnectLineBackground1 from "../../assets/images/Login/hexagon-dotted-connect-line-background-1.png";
// Styles
import "./style.css";

export const ElementLandingScreen = () => {
    
    const PrivateRoute = ({ element }) => {
      const isLoggedIn = Cookies.get('userToken');
  
      return isLoggedIn ? (
        element
      ) : (
        <Navigate to="/" replace={true} state={{ from: window.location.pathname }} />
      );
    };

    return (
        <div className="element-landing-screen">
            <div className="overlap-group-wrapper">
                <div className="overlap-group">
                    <img className="ellipse" alt="Ellipse" src={ellipse2} />
                    <img className="hexagon-dotted" alt="Hexagon dotted" src={hexagonDottedConnectLineBackground1} />
                    <img className="img" alt="Ellipse" src={ellipse1} />
                    <div className="frame">
                        <img className="union" alt="Union" src={union} />
                        <div className="div">EnzyHTP-GPT</div>
                    </div>
                    <p className="p">Developed by Yang Lab at Vanderbilt University</p>
                    <p className="text-wrapper-2">
                      Access to molecular-level insights of your experiment with ease
                      by your AI-based virtual assistant
                      for Molecular Dynamics and more
                    </p>
                    <Routes>
                      <Route path="/" element={<ElementSignUpScreen />} />
                      <Route path="/login" element={<ElementLoginScreen />} />
                      <Route path="/key" element={<PrivateRoute element={<ApiKeyScreen />}/>} />
                      <Route path="/forgotpwd" element={<ForgotpwdScreen />} />
                      <Route path="/resetpwd" element={<ResetpwdScreen />} />
                      <Route path="/googlelogin" element={<GoogleLogin />} />
                    </Routes>
                </div>
            </div>
        </div>
          
  );
};


function GoogleLogin() {

  window.location.replace('/api/auth/oauth/google/login');
  return null;
}

export default ElementLandingScreen;
