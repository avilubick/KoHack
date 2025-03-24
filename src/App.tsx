import ReactDOM from "react-dom/client";
import React, { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom';
import "./App.css";
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import Globe from './pages/Globe';
import AtALoss from './pages/AtALoss';


function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/globe" element={<Globe />} />
        <Route path="/ataloss" element={<AtALoss />} />
      </Routes>
    </>
  );
}
// Um why in the world is the router not working??? I'm at a I II II I_. Nvm it works now lol just delete the package lock json

export default App;
