import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import '../style/Navbar.css';
import Login from '../pages/Login';
import Template from '../pages/Template';
import Templates from '../pages/Templates';

const Navbar = () => {
    return (
        <Router>
            <header className="Navbar">
                <h1 className="NavLogo"><Link className="Link" to="/">Kynda</Link></h1>
                <nav>
                    <ul className="NavLinks">
                        <li><Link className="Link" to="/">Tamplates</Link></li>
                        <li><Link className="Link" to="/">Template</Link></li>
                        <li><Link className="Link" to="/">Login</Link></li>
                    </ul>
                </nav>
            </header>
            <Routes>
                <Route path="/:company_id" element={<Templates />}/>
                <Route path="/:company_id/:template_id" element={<Template />}/>
                <Route path="/login" element={<Login />}/>
            </Routes>
        </Router>
        
    )
}

export default Navbar
