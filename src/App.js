import React, { useState, useEffect } from "react";
import "./App.css";
import ElementLandingScreen from "./screens/Login/landingscreen";

function App() {
  const [data, setData] = useState([{}]);

  // useEffect(() => {
  //   fetch("/members")
  //     .then((res) => res.json())
  //     .then((data) => setData(data));
  // });

  return (
    <div className="App">
      <ElementLandingScreen />
    </div>
    // {/* {typeof data.members === "undefined" ? (
    //   <p>Loading...</p>
    // ) : (
    //   data.members.map((member, i) => <p key={i}>{member}</p>)
    // )} */}
  );
}

export default App;
