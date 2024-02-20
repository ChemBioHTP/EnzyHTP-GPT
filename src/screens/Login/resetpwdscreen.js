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
import Cookies from 'js-cookie';
import hexagonDottedConnectLineBackground1 from "../../assets/images/Login/hexagon-dotted-connect-line-background-1.png";
// Styles
import "./style.css";

export const ResetpwdScreen = () => {
    let navigate = useNavigate(); 
    const handleSubmit = async() => {
    
    }
  
    const [newPwd, setNewPwd] = useState('');
    const [conPwd, setConPwd] = useState('');
    
  
    const initState = {
        newPwdState:"enabled",
        conPwdState:"enabled",
        newPwdVaild: false,
        conPwdValid: false,
        bottonDisabled: true,
        bottonState: "disabled",
    }

    const [state, dispatch] = useReducer(reducer, initState);

    const onChangeNewPwd = (pwd) => {
      const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
      const regexValid = passwordRegex.test(pwd);
      const match = pwd===conPwd? true: false;
      if (!pwd) {
        dispatch("new_pwd_empty");
      } else if(regexValid){
        dispatch("new_pwd_valid");       
        dispatch((!conPwd)? "confirm_pwd_empty": match? "confirm_pwd_valid": "confirm_pwd_error");
      } else {
        dispatch("new_pwd_error");
      }
      
      
      dispatch((regexValid && match)? "button_enabled": "button_disabled");
  
      setNewPwd(pwd);

    };

    const onChangeConPwd = (pwd) => {
      const match = pwd===newPwd? true: false;
      
      dispatch((!pwd)? "confirm_pwd_empty": match? "confirm_pwd_valid": "confirm_pwd_error");

      dispatch((match && state.newPwdValid)? "button_enabled": "button_disabled");

      setConPwd(pwd);

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
                            <div className="text-wrapper-3">Reset Password</div>
                            <div className="frame-4">
                                <div className="text-wrapper-4">Please enter your new password</div>
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
                                    labelText="New password"
                                    errorText="Your password needs to be at least 8 characters including a lower-case letter, an upper case letter, a number and one special chatacter (!@#$%^&*)"
                                    size="large"
                                    spacerClassName="design-component-instance-node"
                                    state={state.newPwdState}
                                    textFilled={false}
                                    
                                    onInputChange={onChangeNewPwd}
                                />
                                <TextInputDefault
                                    backgroundClassName="text-input-default-2"
                                    className="text-input-default-instance"
                                    placeholderText=""
                                    showHelper={false}
                                    showLabel={true}
                                    labelText="Confirm password"
                                    errorText="Password do not match. Please re-enter."
                                    size="large"
                                    spacerClassName="design-component-instance-node"
                                    state={state.conPwdState}
                                    textFilled={false}
                                    
                                    onInputChange={onChangeConPwd}
                                />
                            </div>
                            <div className="frame-6" onClick={handleSubmit}>
                                <Button
                                    buttonText="Reset my password"
                                    className="button-instance"
                                    iconClassName="button-2"
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
      case "new_pwd_error":
        return {
          ...state,
          newPwdState: "error",
          newPwdValid: false,
        };
      case "new_pwd_empty":
        return {
          ...state,
          newPwdState: "enabled",
          newPwdValid: false,
        };
      case "new_pwd_valid":
        return {
          ...state,
          newPwdState: "enabled",
          newPwdValid: true,
        };
      case "confirm_pwd_error":
        return {
          ...state,
          conPwdState: "error",
          conPwdValid: false,
        };
      case "confirm_pwd_empty":
        return {
          ...state,
          conPwdState: "enabled",
          conPwdValid: false,
        };
      case "confirm_pwd_valid":
        return {
          ...state,
          conPwdState: "enabled",
          conPwdValid: true,
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

export default ResetpwdScreen;