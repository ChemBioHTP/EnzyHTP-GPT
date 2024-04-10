import React, { useEffect } from "react";
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
import Cookies from 'js-cookie';
import hexagonDottedConnectLineBackground1 from "../../assets/images/Login/hexagon-dotted-connect-line-background-1.png";
// Styles
import "./style.css";

export const ElementLoginScreen = () => {
    let navigate = useNavigate(); 
    const handleSubmit = async() => {
      if (rememberId) {
        Cookies.set('rememberedId', email);
      } else {
        Cookies.remove('rememberedId');
      }

      const formData = new FormData();
      formData.append('email', email);
      formData.append('password', pwd);
      await fetch('/api/auth/login', {
        method: 'POST',
        body: formData,   
      })
      .then(response => {
        if (!response.ok) {
          if (response.status === 401) {
            throw dispatch("pwd_error");
          } else if (response.status === 404) {
            throw dispatch("email_notfound");
          }
        }
    
        return response.json();
      })
      .then(data => {
        let userToken = data.id;
        const currentTime = new Date();
        const expirationTime = new Date(currentTime.getTime() + 60 * 60 * 1000);        
        Cookies.set('userToken', userToken, { expires: expirationTime }); 
        
        let path = '/key';
        navigate(path);
      })
      .catch(error => {
          console.error('Error sending data:', error);
      });
    }
  
    const handleGoogleLogin = async() => {
      let path = '/api/auth/oauth/google/login';
      navigate(path);
    }
  
  /* hanlde enter press */
  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      document.getElementById("submitButton").click();
    }
  }
  useEffect(() => {
    document.addEventListener("keydown", handleKeyPress);
    return () => document.removeEventListener("keydown", handleKeyPress);
  }, []);
  
  /* end with key press*/
  
    const savedId = Cookies.get('rememberedId') || '';
  
    const [rememberId, setRememberId] = useState(savedId? true: false);
    
    const [email, setEmail] = useState(savedId);
    const [pwd, setPwd] = useState('');

    const handleCheckboxChange = () => {
      setRememberId(prev => !prev);
    };
  
    const initState = {
        emailState:"enabled",
        pwdState:"enabled",
        emailValid: savedId? true: false,
        errorText: "Error Text",
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

    };

    const onChangePwd = (pwd) => {
      
      dispatch(pwd? "pwd_valid": "pwd_empty");

      dispatch((pwd && state.emailValid)? "button_enabled": "button_disabled");

      setPwd(pwd);

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
                            <div className="text-wrapper-3">Log in</div>
                            <div className="frame-4">
                                <div className="text-wrapper-4">New to EnzyHTP?</div>
                                <div className="text-wrapper-5"><Link to="/">Sign up</Link></div>
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
                                    inputDefault={savedId}
                                    errorText={state.errorText}
                                    size="large"
                                    spacerClassName="design-component-instance-node"
                                    state={state.emailState}
                                    textFilled={false}
                                    textDefault={true}
                                    onInputChange={onChangeEmail}
                                />
                                <TextInputDefault
                                    backgroundClassName="text-input-default-2"
                                    className="text-input-default-instance"
                                    placeholderText=""
                                    showHelper={false}
                                    showLabel={true}
                                    showLink={true}
                                    linkText="Forgot password?"
                                    linkHerf="/forgotpwd"
                                    labelText="Password"
                                    errorText="Your password was incorrect. Please try again or tap Forgot password to reset it."
                                    size="large"
                                    spacerClassName="design-component-instance-node"
                                    state={state.pwdState}
                                    textFilled={false}
                                    inputType="password"
                                    onInputChange={onChangePwd}
                                />
                            </div>
                            <div className="frame-6" id="submitButton" onClick={handleSubmit} >
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
                            <div className="frame-6" >
                              <div className="text-wrapper-4">
                                <input
                                  type="checkbox"
                                  className="custom-checkbox"
                                  checked={rememberId}
                                  onChange={handleCheckboxChange}
                                />
                                Remember id
                              </div>
                            </div>
                        </div>
                        <div className="frame-6" onClick={handleGoogleLogin}>
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
          errorText: "Please provide a vaild email",
        };
      case "email_notfound":
        return {
          ...state,
          emailState: "error",
          emailValid: false,
          errorText: "The email does not exist. Please sign up for a new account.",
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

export default ElementLoginScreen;