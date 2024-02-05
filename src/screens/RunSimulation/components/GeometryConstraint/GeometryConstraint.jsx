import React from 'react'
import { ReactComponent as Edit } from '../../../../assets/images/RunSimulation/edit.svg';

const GeometryConstraint = () => {
  return (
    <>
    <p style={{ color: "#000",
                fontFamily: "IBM Plex Sans",
                fontSize: "14px",
                fontStyle: "normal",
                fontWeight: "600",
                lineHeight: "18px", /* 128.571% */
                letterSpacing: "0.16px"}}>
    Geometry constraint 
    </p>
    <p style={{ color: "#525252",
                fontFamily: "IBM Plex Sans",
                fontSize: "12px",
                fontStyle: "normal",
                fontWeight: "400",
                lineHeight: "18px", /* 128.571% */
                letterSpacing: "0.16px", marginLeft: "20px"}}>Whole enzyme</p>
    <Edit style={{ marginLeft: "auto", marginRight: 0}}/>
    </>
  )
}

export default GeometryConstraint