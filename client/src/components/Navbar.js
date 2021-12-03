import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import '../style/Navbar.css';
import Login from '../pages/Login';
import Logout from '../pages/Logout';
import Template from '../pages/Template';
import Templates from '../pages/Templates';
import Register from '../pages/Register';
import Password from '../pages/Password';

const Navbar = () => {
    return (
        <Router>
            <header className="Navbar">
                <h1 className="NavLogo"><Link className="Link" to="/1">Kynda</Link></h1>
                <nav>
                    <ul className="NavLinks">
                        <li><Link className="Link" to="/1">Tamplates</Link></li>
                        <li><Link className="Link" to="/login">Login</Link></li>
                        <li><Link className="Link" to="/register">Register</Link></li>
                        <li><Link className="Link" to="/forgotpassword">Password</Link></li>
                        <li><Link className="Link" to="/logout">Logout</Link></li>
                    </ul>
                </nav>
            </header>
            <Routes>
                <Route path="/:company_id" element={<Templates />}/>
                <Route path="/:company_id/:template_id" element={<Template />}/>
                <Route path="/login" element={<Login />}/>
                <Route path="/register" element={<Register />}/>
                <Route path="/forgotpassword" element={<Password />}/>
                <Route path="/logout" element={<Logout />}/>
            </Routes>
        </Router>
        
    )
}

export default Navbar
