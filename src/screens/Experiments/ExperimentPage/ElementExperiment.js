import React from "react";
import { useState, useReducer, useEffect} from 'react';
import { NavigationHeader } from "../components/NavigationHeader";
import { NavigationSideNav } from "../components/NavigationSideNav";
import { BrowserRouter as Router, Route, Routes, Navigate, useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import "./style.css";
import { NavigationSideBar } from "../components/NavigationSideBar/NavigationSideBar";
import ElementCreateWorkFlow from "../CreateWorkFLow/ElementCreateWorkFlow";
import ElementCreateTarget from "../CreateTarget/ElementCreateTarget";
import ElementExperimentsList from "../ExperimentsList/ElementExperimentsList";
import { Button } from "../components/Button";

export const ElementExperiment = () => {
  const [isVisible, setIsVisible] = useState(true);
  let navigate = useNavigate();
  const [sideLabel, setSideLabel] = useState([]);

  const [titleText, setTitleText] = useState("Example experiment 01");
  const handleButtonClick = (buttonId) => {
    if (buttonId === 0) {
      setIsVisible(!isVisible);
    }
    if (buttonId > 5) {
      setTitleText(sideLabel[buttonId - 6]);
      let path = '/exp/create'; 
      navigate(path);
    } else {
      let path = '/exp/'; 
      navigate(path);
    }
  };

  const example_get_experiments = {
    "user_id": "78a5f120-63ac-4ce1-aa84-8cce1826a415",
    "email": "san.zhang@example.com",
    "username": "san.zhang",
    "timestamp": "2024-02-21 20:45:06.460931",
    "experiments": [
        {
            "type": 0,
            "status": 0,
            "description": "Let's start a test.",
            "updated_time": "2024-02-21 04:53:43.210652",
            "id": "ae394fd8-4a59-4d0b-a1a2-eaaa04ba6768",
            "name": "exp-test-01",
            "metrics": "[]",
            "created_time": "2024-02-21 04:53:43.210650"
        },
        {
            "type": 0,
            "status": 0,
            "description": "Let's start a test.",
            "updated_time": "2024-02-21 04:53:43.210687",
            "id": "1bcb7760-c94e-4bcb-85f5-221169df8089",
            "name": "exp-test-02",
            "metrics": "[]",
            "created_time": "2024-02-21 04:53:43.210686"
        }
    ]
  }

  const example_get_experiments_detail = {
      "type": 0,
      "id": "1bcb7760-c94e-4bcb-85f5-221169df8089",
      "status": 0,
      "description": "Let's start a test.",
      "updated_time": "2024-02-21 04:53:43.210687",
      "name": "exp-test-02",
      "metrics": "[]",
      "created_time": "2024-02-21 04:53:43.210686",
      "user_id": "78a5f120-63ac-4ce1-aa84-8cce1826a415"
  }
  const [experiments, setExperiments] = useState([]);

  useEffect(() => {
    // Fetch experiments from the server
    const fetchData = async () => {
      try {
        // const response = await fetch(`http://localhost:5000/experiments/${user_id}`);
        // const data = await response.json();
        const data = example_get_experiments;
        setExperiments(data.experiments);
        let names = [];

        for (let i = 0; i < data.experiments.length; i++){
          names.push(data.experiments[i].name);
        }
        setSideLabel(names);
        
      } catch (error) {
        console.error('Error fetching experiments:', error);
      }
    };

    fetchData();
    
  }, []);

  const [logoutButton, setLogoutButton] = useState(false);

  const handleSideBarClick = (buttonId) => {
    if (buttonId === 0) {
      setIsVisible(!isVisible);
    }
  };

  const handleWrapperClick = (id) => {
    if (id === 0) {
      let path = '/exp/create'; 
      navigate(path);
    } else {
      let path = '/exp/flow'; 
      navigate(path);
    }
  };

  const handleHeaderClick = (id) => {
    if (id === 0) {
      // bell
    } else {
      // user profile
      setLogoutButton(prev => !prev);
    }
  };

  const handleSignout = async () => {   
    try {
      Cookies.remove('userToken');
      const response = await fetch('/api/auth/logout',{
        method: 'GET',
      });
      if (response.ok) {
        let path = '/login'; 
        navigate(path);
      }
    }catch (error) {
      console.error('Error sending data:', error);
    }
  };

  return (
    <div className="element-experiment" data-theme-mode="white-theme">
      <div className="div-2" data-breakpoints-mode="max-max-plus-1584px-1784px">
        <Routes>
          <Route path="/" element={<ElementExperimentsList sideVisible={isVisible} experiments={experiments} />} />
          <Route path="/flow" element={<ElementCreateWorkFlow sideVisible={isVisible} titleText={titleText} onClickWrapper={handleWrapperClick}/>} />
          <Route path="/create" element={<ElementCreateTarget sideVisible={isVisible} titleText={titleText} onClickWrapper={handleWrapperClick} />} />
        </Routes>
        <NavigationHeader className="navigation-header-instance" onClick={handleHeaderClick}/>
        {logoutButton &&(<div className="div-profile" onClick={handleSignout}>
          <Button
            buttonText="Log out"
            className="button-logout"
            iconClassName="button-2"
            override={<></>}
            icon1={<></>}
            size="large"
            stateProp="enabled"
            format="danger-tertiary"
            type="text-icon"
          />
        </div>)
        }
        <NavigationSideBar className="navigation-side-nav-instance" onButtonClick={handleSideBarClick} />
        
        {isVisible && <NavigationSideNav
          UIShellLeftPanelLinkText={sideLabel}
          UIShellLeftPanelSelected={[true, false, false, false, false]}
          UIShellLeftPanelStateProp={["selected", "enabled", "enabled", "enabled", "enabled"]}
          UIShellLeftPanelSelected1={Array(sideLabel.length).fill(false)}
          UIShellLeftPanelStateProp1={Array(sideLabel.length).fill("enabled")}
          className="navigation-side-nav-2"
          version="version-5"
          onButtonClick={handleButtonClick}
        />}
        
      </div>
    </div>
  );
};

export default ElementExperiment;