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
import ElementCreateResult from "../CreateResult/ElementCreateResult";
import ElementCompletedResult from "../CreateResult/ElementCompletedResult";

export const ElementExperiment = () => {
  let navigate = useNavigate();
  const [isVisible, setIsVisible] = useState(true);
  const [sideLabel, setSideLabel] = useState([]);
  const [sideLabelSelected, setSideLabelSelected] = useState([true, false, false, false, false]);
  const [sideLabelState, setSideLabelState] = useState(["selected", "enabled", "enabled", "enabled", "enabled"]);
  const [sideLabelSelected1, setSideLabelSelected1] = useState([]);
  const [sideLabelState1, setSideLabelState1] = useState([]);

  const [progress, setProgress] = useState("zero");

  const [titleText, setTitleText] = useState("Example experiment 01");

  const handleButtonClick = (buttonId) => {
    if (buttonId === 0) {
      setIsVisible(!isVisible);
    }
    if (buttonId > 5) {
      setTitleText(sideLabel[buttonId - 6]);
      if(buttonId == 6){
        setProgress("twenty-five");
        let path = '/exp/result'; 
        navigate(path);
      }else if(buttonId == 7){
        let path = '/exp/completed'; 
        navigate(path);
      }else{
        let path = '/exp/create'; 
        navigate(path);
      }
      
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
            "type": "on our server",
            "status": "In Progress",
            "description": "this is a test",
            "updated_time": "2024-04-14 04:53:43",
            "id": "ae394fd8-4a59-4d0b-a1a2-eaaa04ba6768",
            "name": "test-exp-01",
            "metrics": "SPI,Stability",
            "created_time": "2024-04-14 01:53:43"
        },
        {
            "type": "on your own",
            "status": "Done",
            "description": "this is a test",
            "updated_time": "2024-02-24 04:22:22",
            "id": "1bcb7760-c94e-4bcb-85f5-221169df8089",
            "name": "test-exp-02",
            "metrics": "EF,SPI,Stability",
            "created_time": "2024-02-22 02:51:00"
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
        // const formData = new FormData();
        // formData.append('email', 'san.zhang@example.com');
        // formData.append('password', '123456');
        // await fetch('https://localhost:5000/api/auth/login', {
        //   method: 'POST',
        //   body: formData,   
        // })
        // .then(response => {
        //   if (!response.ok) {
        //     if (response.status === 401) {
        //       console.log("Invalid credentials");
        //     } else if (response.status === 404) {
        //       console.log("User not found");
        //     }
        //   }
        //   return response.json();
        // })

        // const response = await fetch('https://localhost:5000/api/experiment/',
        //   {
        //     method: 'GET',
        //     headers: {
        //       'Content-Type': 'application/json',
        //       'Connection': 'keep-alive',
        //     }
        //   }
        // ).then((response) => console.log(response));
        
        // const data = await response.json();
        let names = [];

        for (let i = 0; i < data.experiments.length; i++){
          names.push(data.experiments[i].name);
        }
        setSideLabel(names);
        
      } catch (error) {
        console.error('Error fetching experiments:', error);
      }
    };
    const data = example_get_experiments;
    setExperiments(data.experiments);
    fetchData();
    setSideLabelState1(Array(sideLabel.length).fill("enabled"));

    setSideLabelSelected1(Array(sideLabel.length).fill(false));
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

  const createNewExperiment=()=>{
    
    // setSideLabelSelected1([...sideLabelSelected1, true]);
    // setSideLabelState1([...sideLabelState1, "selected"]);
    // setSideLabelSelected(Array(5).fill(false));
    // setSideLabelState(Array(5).fill("enabled"));
    setSideLabel([...sideLabel, "exp-test-03"]);
    setProgress("zero");
    navigate("/exp/create");
  }
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
          <Route path="/" element={<ElementExperimentsList sideVisible={isVisible} experiments={experiments} createNewExp={createNewExperiment}/>} />
          <Route path="/flow" element={<ElementCreateWorkFlow sideVisible={isVisible} titleText={titleText} onClickWrapper={handleWrapperClick}/>} />
          <Route path="/create" element={<ElementCreateTarget sideVisible={isVisible} titleText={titleText} onClickWrapper={handleWrapperClick} />} />
          <Route path="/result" element={<ElementCreateResult sideVisible={isVisible} titleText={titleText} progerss={progress} />} />
          <Route path="/completed" element={<ElementCompletedResult sideVisible={isVisible} titleText={titleText} onClickWrapper={handleWrapperClick} />} />
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
          UIShellLeftPanelSelected={sideLabelSelected}
          UIShellLeftPanelStateProp={sideLabelState}
          UIShellLeftPanelSelected1={sideLabelSelected1}
          UIShellLeftPanelStateProp1={sideLabelState1}
          className="navigation-side-nav-2"
          version="version-5"
          onButtonClick={handleButtonClick}
        />}
        
      </div>
    </div>
  );
};

export default ElementExperiment;