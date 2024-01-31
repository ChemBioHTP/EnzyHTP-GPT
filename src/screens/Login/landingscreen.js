import React from "react";
import { useNavigate } from "react-router-dom";
import { useState, useReducer} from 'react';
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

export const ElementLandingScreen = () => {
    let navigate = useNavigate(); 
    const routeChange = () =>{ 
      let path = '/key'; 
      navigate(path);
    }
    const [email, setEmail] = useState('');
    const [pwd, setPwd] = useState('');

    const initState = {
        emailState:"enabled",
        pwdState:"enabled",
        emailValid: false,
        pwdValid: false,
        bottonDisabled: true,
        bottonState: "disabled",
    }

    const [state, dispatch] = useReducer(reducer, initState);

    const onChangeEmail = (useremail) => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const regexValid = emailRegex.test(useremail);
      
      dispatch((!useremail)? "email_empty": regexValid? "email_valid": "email_error");

      dispatch((regexValid && state.pwdValid)? "button_enabled": "button_disabled");
           
      setEmail(useremail);
      console.log("In email change",state.bottonDisabled);
    };

    const onChangePwd = (pwd) => {
      const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
      const regexValid = passwordRegex.test(pwd);
      
      dispatch((!pwd)? "pwd_empty": regexValid? "pwd_valid": "pwd_error");

      dispatch((regexValid && state.emailValid)? "button_enabled": "button_disabled");

      setPwd(pwd);
      console.log("In pwd change",state.bottonDisabled);
    };

    const handleSubmit = async () => {
        const data = {
            email: email,
            password: pwd,
        };
      
        try {
            const response = await fetch('https://localhost:5000', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
        }catch (error) {
            console.error('Error sending data:', error);
        }
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
                            <div className="text-wrapper-3">Create an account</div>
                            <div className="frame-4">
                                <div className="text-wrapper-4">Have an account?</div>
                                <div className="text-wrapper-5"><Link to="/login">Log in</Link></div>
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
                                <TextInputDefault
                                    backgroundClassName="text-input-default-2"
                                    className="text-input-default-instance"
                                    placeholderText=""
                                    showHelper={false}
                                    showLabel={true}
                                    labelText="Password"
                                    errorText="Your password needs to be at least 8 characters including a lower-case letter, an upper case letter, a number and one special chatacter (!@#$%^&*)"
                                    size="large"
                                    spacerClassName="design-component-instance-node"
                                    state={state.pwdState}
                                    textFilled={false}
                                    onInputChange={onChangePwd}
                                />
                            </div>
                            <div className="frame-6" onClick={routeChange}>
                                <Button
                                    buttonText="Continue"
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
                        <div className="frame-6">
                            <Button
                                buttonText="Log in with Google"
                                className="button-instance"
                                iconClassName="button-2"
                                override={<IconArrowRight className="icon-arrow-right" />}
                                size="large"
                                stateProp="enabled"
                                format="tertiary"
                                type="text-icon"
                            />
                            <Button
                                buttonText="Log in with Facebook"
                                className="button-instance"
                                iconClassName="button-2"
                                override={<IconArrowRight className="icon-arrow-right" />}
                                size="large"
                                stateProp="enabled"
                                format="tertiary"
                                type="text-icon"
                            />
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
      case "pwd_error":
        return {
          ...state,
          pwdState: "error",
          pwdValid: false,
        };
      case "pwd_empty":
        return {
          ...state,
          pwdState: "enabled",
          pwdValid: false,
        };
      case "pwd_valid":
        return {
          ...state,
          pwdState: "enabled",
          pwdValid: true,
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

export default ElementLandingScreen;