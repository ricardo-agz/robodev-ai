import React from "react";
import './App.css';
import { Routes, Route } from "react-router-dom";
import Home from './Home';
$$DYNAMIC_IMPORTS$$
$$AUTH_IMPORTS$$


function App() {
  $$USE_FIND$$
  return (
    $$CONTEXT_PROVIDER$$
    <div className="App">
      $$NAV$$
      <Routes>
        <Route path="/" element={<Home />} />
        $$AUTH_ROUTES$$
        $$DYNAMIC_ROUTES$$
      </Routes>  
    </div>
    $$CLOSE_CONTEXT_PROVIDER$$
  );
}

export default App;
