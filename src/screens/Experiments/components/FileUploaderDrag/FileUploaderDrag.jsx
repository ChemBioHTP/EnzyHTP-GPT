/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

// import PropTypes from "prop-types";
// import React from "react";
// import "./style.css";

// export const FileUploaderDrag = ({ helperText = "Drag and drop files here or click to upload", state, className }) => {
//   return (
//     <div className={`file-uploader-drag state-${state} ${className}`}>
//       <div className="description-wrapper">
//         <p className="description">{helperText}</p>
//       </div>
//     </div>
//   );
// };

// FileUploaderDrag.propTypes = {
//   helperText: PropTypes.string,
//   state: PropTypes.oneOf(["disabled", "drag-hover", "focus", "enabled"]),
// };

/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import React from "react";
import { PropTypes } from "prop-types";
import "./style.css";
import { useState, useRef } from "react";
import { Button } from "../../../CreateMutants/components/Button";
import { IconArrowRight1 } from "../../../CreateMutants/icons/IconArrowRight1";
import { useNavigate } from "react-router-dom";

import "./style.css";


export const FileUploaderDrag = ({ helperText = "Drag and drop files here or click to upload", state, className }) => {
  const [file, setFile] = useState(null);
  const fileInputRef = useRef(null);
  const [valid, setValid] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  let navigate = useNavigate();

  const routeChange = () => {
    try {
      navigate("/create_mutants");
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles.length > 0) {
      const selectedFile = droppedFiles[0];
  
      // Check if the file has the correct extension
      if (selectedFile.name.endsWith('.pdb')) {
        handleFiles(droppedFiles);
      } else {
        alert('Please drop a file with a ".pdb" extension.');
      }
    }
  };

  const handleFiles = (files) => {
    if (files.length > 0) {
      const selectedFile = files[0];
      setFile(selectedFile);
      uploadFile(selectedFile);
    }
  };

  const handleFileInputChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    uploadFile(selectedFile);
  };

  const uploadFile = async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      // Adjust the URL based on your backend setup
      const response = await fetch('http://127.0.0.1:5000/api/validate_file', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`File upload failed with status ${response.status}`);
      }
      const data = await response.json();
      setValid(data.validity)
      setErrorMessage(data.message)
  
    } catch (error) {
      console.error('Error uploading file', error.message);
      alert('An error occurred while uploading the file. Please try again.');
    }
  };

  return (
    <>
    <div className={`file-uploader-drag state-${state} ${className}`} onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()} onClick={() => fileInputRef.current.click()}
    >
      <div className="description-wrapper">
        <p className="description">{helperText}</p>
        <input
          type="file"
          onChange={handleFileInputChange}
          style={{ display: 'none' }}
          ref={fileInputRef}
          accept=".pdb" />
      </div>
      {file && (
        <div className="selected-file-info">
          <p>Selected File: {file.name}</p>
          <p>File Size: {(file.size / 1000000).toFixed(2)} MB</p>
        </div>
      )}
    </div>
    <div style={{marginRight: 10, marginLeft: "auto"}}>
        {valid === null && <p></p>}
        {valid &&         
        <div onClick={routeChange}>
          <Button
            buttonText="Next"
            className="button-3"
            icon1={<IconArrowRight1 className="icon-instance-node-3" />}
            iconClassName="button-2"
            size="large"
            stateProp="enabled"
            type="text-icon"
          />
        </div>}
        {valid === false && (
          <div>
            <p style={{maxWidth:"200ch", whiteSpace:"pre-line"}}>{errorMessage}</p>
          </div>
        )}
    </div>
    </>
  );
};

FileUploaderDrag.propTypes = {
  helperText: PropTypes.string,
  state: PropTypes.oneOf(["disabled", "drag-hover", "focus", "enabled"]),
};
