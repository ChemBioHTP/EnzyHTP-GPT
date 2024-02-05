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
import Cookies from 'js-cookie';
import hexagonDottedConnectLineBackground1 from "../../assets/images/Login/hexagon-dotted-connect-line-background-1.png";
// Styles
import "./style.css";

export const ApiKeyScreen = () => {
    let navigate = useNavigate(); 
    const routeChange = () =>{ 
      let path = '/key'; 
      navigate(path);
    }
    
    const [key, setKey] = useState('');

    const initState = {
        bottonDisabled: true,
        bottonState: "disabled",
    }

    const [state, dispatch] = useReducer(reducer, initState);

    const onChangeKey = (key) => {

      dispatch(key? "button_enabled": "button_disabled");

      setKey(key);

    };

    const handleSignout = async () => {   
      try {
        Cookies.remove('userToken');
        const response = await fetch('https://192.168.1.252:5000/api/auth/logout');
        if (response.ok) {
          
          let path = '/login'; 
          navigate(path);
        }
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
                            <div className="text-wrapper-3">Provide Secret API Key</div>
                            <div className="frame-4">
                            <div className="text-wrapper-4">Copy and paste your API key from OpenAI.</div>                               
                                <div className="text-wrapper-5"><Link to="https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key" target="_blank">learn more</Link></div>
                            </div>
                            <div className="text-wrapper-4" style={{ textAlign: 'left' }}>We need it for running the embedded ChatGPT
                            <br />Agent for your workflow. Estimated cost: $5000/run</div>
                        </div>
                        <div className="frame-5">
                            <div className="frame-6">
                            <TextInputDefault
                                    backgroundClassName="text-input-default-2"
                                    className="text-input-default-instance"
                                    placeholderText=""
                                    showHelper={false}
                                    showLabel={false}
                                    errorText="Please provide a vaild email"
                                    size="large"
                                    spacerClassName="design-component-instance-node"
                                    state="enabled"
                                    textFilled={false}
                                    onInputChange={onChangeKey}
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
                            <div className="frame-6" onClick={handleSignout}>
                                <Button
                                    buttonText="Sign out"
                                    className="button-instance"
                                    iconClassName="button-2"
                                    size="large"
                                    stateProp="enabled"
                                    format="secondary"
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

export default ApiKeyScreen;