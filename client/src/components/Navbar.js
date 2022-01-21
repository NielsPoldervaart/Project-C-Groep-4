import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import '../style/Navbar.css';
import Login from '../pages/Login';
import Template from '../pages/Template';
import Templates from '../pages/Templates';
import Logout from '../pages/Logout';
import Product from '../pages/Product';
import Products from '../pages/Products';
import Register from '../pages/Register';
import Password from '../pages/Password';
import Home from '../pages/Home';
import Images from '../pages/Images';
import Accounts from '../pages/Accounts';
import Help from '../pages/Help';
import Manual from '../pages/Manual';
import Profile from '../pages/Profile';

const Navbar = () => {
    return (
        <Router>
            <header className="Navbar">
                <h1 className="NavLogo"><Link className="Link" to="/1">
                    <img src="https://excelsiorrotterdam.nl/wp-content/uploads/2018/01/kynda_web.png" alt="KyndaLogo" width="150px"/>
                    </Link></h1>
                <nav>
                    <ul className="NavLinks">
                        <li><Link className="Link" to="/templates/1">Templates</Link></li>
                        <li><Link className="Link" to="/products/1">Products</Link></li>
                        <li><Link className="Link" to="/gallery/1/1">Beeldbank</Link></li>
                        <li><Link className="Link" to="/1/accounts">Accounts</Link></li>
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
                <Route path="/templates/:company_id" element={<Templates />}/>
                <Route path="/products/:company_id" element={<Products />}/>
                <Route path="/product/:company_id/:product_id" element={<Product />}/>
                <Route path="/template/:company_id/:template_id" element={<Template />}/>
                <Route path="/login" element={<Login />}/>
                <Route path="/register" element={<Register />}/>
                <Route path="/forgotpassword" element={<Password />}/>
                <Route path="/logout" element={<Logout />}/>
                <Route path="/welcome" element={<Home />}/>
                <Route path="/gallery/:company_id/:gallery_id" element={<Images />}/>
                <Route path="/:company_id/accounts" element={<Accounts />}/>
                <Route path="/help" element={<Help />}/>
                <Route path="/manual" element={<Manual />}/>
                <Route path="/profile" element={<Profile />}/>
            </Routes>
        </Router>
        
    )
}

export default Navbar
