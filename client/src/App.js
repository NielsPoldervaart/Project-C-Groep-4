import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './pages/Login';
import Template from './pages/Template';
import Templates from './pages/Templates';

function App() {

  // const [data, setData] = useState([{}])

  // useEffect(() => {
  //   fetch("/members").then(
  //     res => res.json()
  //   ).then(
  //     data => {
  //       setData(data)
  //       console.log(data)
  //     }
  //   )
  // }, [])

  return (
    <Router>
      <nav>
        <Link to="/">Templates</Link>
        <Link to="/template">Tamplate :)</Link>
        <Link to="/login">Login</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Templates />}/>
        <Route path="/template" element={<Template />}/>
        <Route path="/login" element={<Login />}/>
      </Routes>
    </Router>
  );
}

export default App;
