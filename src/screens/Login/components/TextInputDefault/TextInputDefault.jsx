/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { useState, useRef, useEffect } from 'react';
import { WarningFilled } from "../../icons/WarningFilled";
import "./style.css";
import { Link } from "react-router-dom";

export const TextInputDefault = ({
  labelText = "Label",
  linkText = "Link",
  linkHerf = "/",
  showLabel = true,
  showLink = false,
  inputDefault = "Default text",
  placeholderText = "Placeholder text (optional)",
  errorText = "Error message goes here",
  state,
  textDefault = false,
  className,
  inputType = "text",
  onInputChange,
}) => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    const value = event.target.value;
    setInputValue(value);
    onInputChange(value);
  };
  
  useEffect(() => {
    if(textDefault){
      setInputValue(inputDefault);
    }
  }, []);

  return (
    <div className={`text-input-default ${state} ${className}`}>
      <div className="label-character">
        {showLabel && (
          <div className="label-margin">{showLabel && <div className="label-text">{labelText}</div>}</div>
        )}
        {showLink && (
          <div className="link-margin">{showLink && <Link className="link-text" to={linkHerf}>{linkText}</Link>}</div>
        )}

      </div>
      <div className={`text-input  ${state}`}>  
        <input
          className={`input`}
          placeholder={state === "enabled" ? placeholderText : undefined}
          type={inputType}
          value={inputValue}
          onChange={handleInputChange}
        />     
        
        <div className="overlap-error">
          {state === "error" && <WarningFilled className="instance-node" />}
        </div>
      </div>
      {(state === "error") && (
        <div className="helper-text">    
          {errorText}
        </div>
      )}
    </div>
  );
};

TextInputDefault.propTypes = {
  countText: PropTypes.string,
  labelText: PropTypes.string,
  showLabel: PropTypes.bool,
  inputText: PropTypes.string,
  inputDefault: PropTypes.string,
  placeholderText: PropTypes.string,
  errorText: PropTypes.string,
  state: PropTypes.oneOf(["enabled", "error"]),
  textFilled: PropTypes.bool,
  textDefault: PropTypes.bool,
  textHidden: PropTypes.bool,
  inputType: PropTypes.string,
};
