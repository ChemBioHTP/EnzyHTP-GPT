import React from "react";
import { useNavigate } from "react-router-dom";
// Components
import { IconArrowRight } from "./icons/IconArrowRight/IconArrowRight";
import { Button } from "./components/Button/Button";
import { TextInputDefault } from "./components/TextInputDefault/TextInputDefault";
// Images and icons
import ellipse2 from "../../assets/images/Login/ellipse-2.svg";
import ellipse1 from "../../assets/images/Login/ellipse-1.svg";
import union from "../../assets/images/Login/union.svg";
import hexagonDottedConnectLineBackground1 from "../../assets/images/Login/hexagon-dotted-connect-line-background-1.png";
// Styles
import "./style.css";

export const ElementLandingScreen = () => {
    let navigate = useNavigate(); 
    const routeChange = () =>{ 
      let path = '/key'; 
      navigate(path);
    }

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
                                <div className="text-wrapper-5">Log in</div>
                            </div>
                        </div>
                        <div className="frame-5">
                            <div className="frame-6">
                                <TextInputDefault
                                    backgroundClassName="text-input-default-2"
                                    className="text-input-default-instance"
                                    placeholderText="Email address"
                                    showHelper={false}
                                    showLabel={false}
                                    size="large"
                                    spacerClassName="design-component-instance-node"
                                    state="enabled"
                                    textFilled={false}
                                />
                                <TextInputDefault
                                    backgroundClassName="text-input-default-2"
                                    className="text-input-default-instance"
                                    placeholderText="Password"
                                    showHelper={false}
                                    showLabel={false}
                                    size="large"
                                    spacerClassName="design-component-instance-node"
                                    state="enabled"
                                    textFilled={false}
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

export default ElementLandingScreen;