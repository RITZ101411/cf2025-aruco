import React from "react";
import marker from "../assets/images/aruco_0.png"

const Home: React.FC = () => {
  return (
    <div>
      <h1>Home Page</h1>
      <p>P</p>
      <img src="/images/aruco_0.png" alt="ArUco Marker" width={200} />
      <img src={marker}></img>
    </div>
  );
};

export default Home;
