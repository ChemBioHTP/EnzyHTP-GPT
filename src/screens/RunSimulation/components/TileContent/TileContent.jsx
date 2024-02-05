import React from 'react'

export const TileContent = ({header, description}) => {
  return (
    <>
    <div style={{color: "var(--text-text-primary, var(--Text-text-primary, #161616))",
      fontFamily: "IBM Plex Sans",
      fontSize: "16px",
      fontStyle: "normal",
      fontWeight: "400",
      lineHeight: "24px"}}>{header}</div>
      <div style={{color: "var(--text-text-secondary, var(--Text-text-secondary, #525252))",
      fontFamily: "IBM Plex Sans",
      fontSize: "12px",
      fontStyle: "normal",
      fontWeight: "400",
      lineHeight: "20px",
      letterSpacing: "0.16px", alignSelf: "stretch"
      }}>{description}</div>
      </>
  )
}

export default TileContent