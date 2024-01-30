import React from "react";
import { useNavigate } from "react-router-dom";
import { useState } from 'react';
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

export const ElementLoginScreen = () => {
    let navigate = useNavigate(); 
    const routeChange = () =>{ 
      let path = '/key'; 
      navigate(path);
    }

    const [email, setEmail] = React.useState('');
    const [pwd, setPwd] = React.useState('');

    const [emailState, setEmailState] = React.useState('enabled');
    const [pwdState, setPwdState] = React.useState('enabled');

    const onChangeEmail = (useremail) => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const isValid = (!useremail) || emailRegex.test(useremail);
      if (!isValid) {
        setEmailState("error");
      } else {
        setEmailState("enabled");
      }
      setEmail(useremail);
    };

    const onChangePwd = (pwd) => {
      const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
      const isValid = (!pwd) || passwordRegex.test(pwd);
      if (!isValid) {
        setPwdState("error");
      } else {
        setPwdState("enabled");
      }
      setPwd(pwd);
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
                                    errorText="Please provide a vaild email"
                                    size="large"
                                    spacerClassName="design-component-instance-node"
                                    state={emailState}
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
                                    state={pwdState}
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
                                    stateProp="enabled"
                                    format="primary"
                                    type="text-icon"
                                    onClick={handleSubmit}
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

export default ElementLoginScreen;