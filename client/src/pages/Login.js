import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react'
import '../style/Login.css';

const Login = () => {
    let navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [loginResponse, setLoginResponse] = useState({});

    let header = new Headers();

    header.append('Content-Type', 'application/json');
    header.append('Accept', 'application/json');
    header.append('Access-Control-Allow-Origin', '*');
    header.append('Access-Control-Allow-Credentials', 'true');

    const HandleEmailChange = (e) => {
        setFormData({...formData, email: e.target.value})
    }

    const HandlePasswordChange = (e) => {
        setFormData({...formData, password: e.target.value})
    }

    const verifyUser = (e) => {
        e.preventDefault()

        console.log(JSON.stringify(formData))

        fetch('/login', {
            method: 'POST',
            body: JSON.stringify(formData),
            headers: header,
        })
        .then(response => response.json())
        .catch(error => console.log('Authorization failed : ' + error.message));
    }

    return (
        <div className="login">
            <div className="loginBox">
                <div className="logoBox">
                    <img src="https://excelsiorrotterdam.nl/wp-content/uploads/2018/01/kynda_web.png" alt="kyndaLogo" width="250" />    
                </div>
                {/* <form className="loginForm" method="post" action id="form" onSubmit={() => navigate(`/`)}> */}
                <form className="loginForm" method="post" action id="form" onSubmit={(e) => console.log(verifyUser(e))}>
                    <div className="loginInput">
                        <div className="email">
                            <label className="inputLabel" for="email">
                            E-mail
                            </label>
                            <input className="inputInput" type="text" name="email" id="email" required="required" maxLength="100" tabIndex="1" autoFocus="autofocus" value={formData.email} onChange={HandleEmailChange} />
                        </div>
                        <div className="password">
                            <label className="inputLabel" for="password">
                            Wachtwoord
                            </label>
                            <input className="inputInput" type="password" name="password" id="password" required="required" maxLength="100" tabIndex="2" autoComplete="off" value={formData.password} onChange={HandlePasswordChange} />
                        </div>
                    </div>
                    <div className="loginButton">
                        <button className="buttonL" type="submit" id="button" >
                            <span className="buttonLabel">Inloggen</span>
                        </button>
                    </div>
                    <div className="register">
                        <a className="registerLink" href="./register">Account aanvragen</a>
                    </div>
                    <div className="forgotPassword">
                        <a className="passwordLink" href="./forgotpassword">Wachtwoord vergeten?</a>
                    </div>
                </form>
            </div>
        </div>

    );
};
  
export default Login;