import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Detection from "../pages/Detection";

const AppRouter: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/detection" element={<Detection />} />
    </Routes>
  );
};

export default AppRouter;
