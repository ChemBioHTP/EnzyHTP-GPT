import React from 'react'
import Workflow from '../Workflow/Workflow'
import "./style.css"
import { ReactComponent as Edit } from '../../../../assets/images/RunSimulation/edit.svg';

export const WorkflowDisplay = () => {
  return (
    <>
    <div style={{display: "flex", flexDirection: "row", justifyContent: "space-between"}}>
      <p style={{color: "#000",
      fontFamily: "IBM Plex Sans",
      fontSize: "14px",
      fontStyle: "normal",
      fontWeight: "600",
      lineHeight: "18px",
      letterSpacing: "0.16px", marginLeft: "10px", marginTop: "5px"}}>Workflow</p>
      <Edit style={{ marginLeft: 885, marginTop: 16}}/>
    </div>
    <div className='Workflow'>
        <Workflow/>
    </div>
    </>
  )
}

export default WorkflowDisplay