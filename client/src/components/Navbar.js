import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import '../style/Navbar.css';
import Login from '../pages/Login';
import Template from '../pages/Template';
import Templates from '../pages/Templates';
import Register from '../pages/Register';
import Password from '../pages/Password';
import Home from '../pages/Home';
import Images from '../pages/Images';
import Accounts from '../pages/Accounts';
import Profile from '../pages/Profile';
import Manual from '../pages/Manual';
import Help from '../pages/Help';

const Navbar = () => {
    return (
        <Router>
            <header className="Navbar">
                <h1 className="NavLogo"><Link className="Link" to="/1">
                    <img src="https://excelsiorrotterdam.nl/wp-content/uploads/2018/01/kynda_web.png" alt="KyndaLogo" width="150px"/>
                    </Link></h1>
                <nav>
                    <ul className="NavLinks">
                        <li><Link className="Link" to="/1">Tamplates</Link></li>
                        <li><Link className="Link" to="/images">Beeldbank</Link></li>
                        <li><Link className="Link" to="/accounts">Accounts</Link></li>
                    </ul>
                    <ul className="profilePic">
                        <img src="https://image.flaticon.com/icons/png/512/50/50050.png" alt="pfpIcon" width="50px"/>
                        <div className="profileMenu">
                            <li><Link className="Link" to="/profile">Profiel</Link></li>
                            <li><Link className="Link" to="/manual">Handboek</Link></li>
                            <li><Link className="Link" to="/help">Help</Link></li>
                            <li><Link className="Link" to="/logout">Uitloggen</Link></li>
                        </div>
                    </ul>
                </nav>
            </header>
            <Routes>
                <Route path="/:company_id" element={<Templates />}/>
                <Route path="/:company_id/:template_id" element={<Template />}/>
                <Route path="/login" element={<Login />}/>
                <Route path="/register" element={<Register />}/>
                <Route path="/forgotpassword" element={<Password />}/>
                <Route path="/logout" element={<Login />}/>
                <Route path="/welcome" element={<Home />}/>
                <Route path="/images" element={<Images />}/>
                <Route path="/accounts" element={<Accounts />}/>
                <Route path="/profile" element={<Profile />}/>
                <Route path="/manual" element={<Manual />}/>
                <Route path="/help" element={<Help />}/>
            </Routes>
        </Router>
        
    )
}

export default Navbar
