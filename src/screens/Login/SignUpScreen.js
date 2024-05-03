import React from "react";
import { useNavigate } from "react-router-dom";
import { useState, useReducer, useEffect} from 'react';
// Components
import { IconArrowRight } from "./icons/IconArrowRight/IconArrowRight";
import { Button } from "./components/Button/Button";
import { TextInputDefault } from "./components/TextInputDefault/TextInputDefault";
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';

// Styles
import "./style.css";

export const ElementSignUpScreen = () => {
    let navigate = useNavigate(); 
    
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
  
    const handleSubmit = async() => {
      if (rememberId) {
        Cookies.set('rememberedId', email);
      } else {
        Cookies.remove('rememberedId');
      }
    
      const formData = new FormData();
        formData.append('email', email);
        formData.append('password', pwd);
        try {
          const response = await fetch('/api/auth/register', {
              method: 'POST',          
              body: formData,
          });
          if (response.ok) {
            let path = '/login'; 
            navigate(path);
          } else {
            if ('Notification' in window) {
              Notification.requestPermission().then((permission) => {
                if (permission === 'granted') {
                  new Notification('ERROR', {
                    body: 'Register failed',
                  });
                }
              });
            }
          }
        }catch (error) {
          console.error('Error sending data:', error);
        }
    }
    
    const handleGoogleLogin = async() => {
      let path = '/googlelogin';
      navigate(path);
    }
    const savedId = Cookies.get('rememberedId') || '';
  
    const [rememberId, setRememberId] = useState(savedId? true: false);

    const [email, setEmail] = useState('');
    const [pwd, setPwd] = useState('');
    
    const handleCheckboxChange = () => {
      setRememberId(prev => !prev);
    };
  
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

    };

    const onChangePwd = (pwd) => {
      const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
      const regexValid = passwordRegex.test(pwd);
      
      dispatch((!pwd)? "pwd_empty": regexValid? "pwd_valid": "pwd_error");

      dispatch((regexValid && state.emailValid)? "button_enabled": "button_disabled");

      setPwd(pwd);

    };
    

    return (
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
                        className="text-input-default-instance"
                        placeholderText=""
                        showLabel={true}
                        labelText="Email address"
                        errorText="Please provide a vaild email"
                        state={state.emailState}
                        onInputChange={onChangeEmail}
                    />
                    <TextInputDefault
                        className="text-input-default-instance"
                        placeholderText=""
                        showLabel={true}
                        labelText="Password"
                        errorText="Your password needs to be at least 8 characters including a lower-case letter, an upper case letter, a number and one special chatacter (!@#$%^&*)"
                        state={state.pwdState}
                        inputType="password"
                        onInputChange={onChangePwd}
                    />
                </div>
                <div className="frame-6" id="submitButton" onClick={handleSubmit}>
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

export default ElementSignUpScreen;
