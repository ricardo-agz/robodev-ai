import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from './Home';
$$dynamic:0
$$AUTH:0
import './App.css';

function App() {
  $$AUTH:5
  return (
    $$AUTH:1
    <div className="App">
      $$AUTH:2
      <Routes>
        <Route path="/" element={<Home />} />
        $$AUTH:3
        $$dynamic:1
      </Routes>  
    </div>
    $$AUTH:4
  );
}

export default App;
