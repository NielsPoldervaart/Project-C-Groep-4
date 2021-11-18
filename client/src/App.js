import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Template from './pages/Template';
import Templates from './pages/Templates';
import Register from './pages/Register';
import Password from './pages/Password';

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
      <Routes>
        <Route path="/" element={<Templates />}/>
        <Route path="/template" element={<Template />}/>
        <Route path="/login" element={<Login />}/>
        <Route path="/register" element={<Register />}/>
        <Route path="/forgotpassword" element={<Password />}/>
      </Routes>
    </Router>
  );
}

export default App;
