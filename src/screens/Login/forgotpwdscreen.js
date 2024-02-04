import React from "react";
import { useNavigate } from "react-router-dom";
import { useState, useReducer, useEffect} from 'react';
// Components
import { IconArrowRight } from "./icons/IconArrowRight/IconArrowRight";
import { Button } from "./components/Button/Button";
import { TextInputDefault } from "./components/TextInputDefault/TextInputDefault";
// Images and icons
import ellipse2 from "../../assets/images/Login/ellipse-2.svg";
import ellipse1 from "../../assets/images/Login/ellipse-1.svg";
import union from "../../assets/images/Login/union.svg";
import { Link } from 'react-router-dom';
import hexagonDottedConnectLineBackground1 from "../../assets/images/Login/hexagon-dotted-connect-line-background-1.png";
// Styles
import "./style.css";

export const ForgotpwdScreen = () => {
    let navigate = useNavigate(); 
    const handleSubmit = async() => {
      
    }

    const [email, setEmail] = useState('');
 
  
    const initState = {
        emailState:"enabled",
        emailValid: false,
        bottonDisabled: true,
        bottonState: "disabled",
    }

    const [state, dispatch] = useReducer(reducer, initState);

    const onChangeEmail = (useremail) => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const regexValid = emailRegex.test(useremail);
      
      dispatch((!useremail)? "email_empty": regexValid? "email_valid": "email_error");

      dispatch(regexValid? "button_enabled": "button_disabled");
           
      setEmail(useremail);

    };
    

    return (
        <div className="element-landing-screen">
            <div className="overlap-group-wrapper">
                <div className="overlap-group">
                    <div className="rectangle" />
                    <img className="ellipse" alt="Ellipse" src={ellipse2} />
                    <img className="hexagon-dotted" alt="Hexagon dotted" src={hexagonDottedConnectLineBackground1} />
                    <img className="img" alt="Ellipse" src={ellipse1} />
                    <div className="frame">
                        <img className="union" alt="Union" src={union} />
                        <div className="div">EnzyHTP</div>
                    </div>
                    <p className="p">Developed by Yang Lab at Vanderbilt University</p>
                    <p className="text-wrapper-2">
                        Revolutionizing computational chemistry by seamlessly streamlining preparation, mutation, and analysis.
                    </p>
                    <div className="frame-2">
                        <div className="frame-3">
                            <div className="text-wrapper-3">Forgot password</div>
                            <div className="frame-4">
                                <div className="text-wrapper-4" style={{ textAlign: 'left' }}>Please verify your email for us. Once you do, we'll
                                <br />send instructions to reset your password.</div>
                            </div>
                        </div>
                        <div className="frame-5">
                            <div className="frame-6">
                                <TextInputDefault
                                    backgroundClassName="text-input-default-2"
                                    className="text-input-default-instance"
                                    placeholderText=""
                                    showHelper={false}
                                    showLabel={true}
                                    labelText="Email address"
                                    errorText="Please provide a vaild email"
                                    size="large"
                                    spacerClassName="design-component-instance-node"
                                    state={state.emailState}
                                    textFilled={false}
                                    onInputChange={onChangeEmail}
                                />                                
                            </div>
                            <div className="frame-6" onClick={handleSubmit}>
                                <Button
                                    buttonText="Reset my password"
                                    className="button-instance"
                                    iconClassName="button-2"
                                    override={<IconArrowRight className="icon-arrow-right" />}
                                    size="large"
                                    stateProp={state.bottonState}
                                    disabled={state.bottonDisabled}
                                    format="primary"
                                    type="text-icon"
                                />
                            </div>                           
                        </div>                        
                    </div>
                </div>
            </div>
        </div>
    );
};

function reducer(state, action) {
    switch (action) {
      case "email_error":
        return {
          ...state,
          emailState: "error",
          emailValid: false,
        };
      case "email_empty":
        return {
          ...state,
          emailState: "enabled",
          emailValid: false,
        };
      case "email_valid":
        return {
          ...state,
          emailState: "enabled",
          emailValid: true,
        };
      case "button_disabled":
        return {
          ...state,
          bottonState: "disabled",
          bottonDisabled: true,
        };
      case "button_enabled":
        return {
          ...state,
          bottonState: "enabled",
          bottonDisabled: false,
        };
    }
  
    return state;
}

export default ForgotpwdScreen;