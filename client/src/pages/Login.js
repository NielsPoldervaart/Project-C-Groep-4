import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react'
import '../style/Login.css';

const Login = () => {
    let navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: "",
        password: "",
    });

    let header = new Headers();

    header.append('Content-Type', 'application/json');
    header.append('Accept', 'application/json');
    header.append('Access-Control-Allow-Origin', '*');
    header.append('Access-Control-Allow-Credentials', 'true');

    const HandleUsernameChange = (e) => {
        setFormData({...formData, name: e.target.value})
    }

    const HandlePasswordChange = (e) => {
        setFormData({...formData, password: e.target.value})
    }

    const verifyUser = (e) => {
        e.preventDefault()

        fetch('/login', {
            method: 'POST',
            body: JSON.stringify(formData),
            headers: header,
        })
        .then(res =>  res.json())
        .then(data => {
            if (data.Code === 200) {

                fetch(`/login`).then(
                    res => res.json()
                ).then(
                    data => {
                        if (data.Code === 500 || data.Code === 404) {
                            window.location.href = "/login";
                        } else {
                            navigate(`/${data.company_company_id}`)
                        }
                    }
                )
            }
            else {
                alert("Error, Wrong credentials!")
            }
        })
        .catch(error => console.log('Authorization failed : ' + error.message));
    }

    return (
        <div className="login">
            <div className="loginBox">
                <div className="logoBox">
                    <img src="https://excelsiorrotterdam.nl/wp-content/uploads/2018/01/kynda_web.png" alt="kyndaLogo" width="250" />
                </div>
                <form className="loginForm" method="post" id="form" onSubmit={(e) => verifyUser(e)}>
                    <div className="loginInput">
                        <div className="email">
                            <label className="inputLabel" htmlFor="email">
                            Gebruikersnaam
                            </label>
                            <input className="inputInput" type="text" name="username" id="username" required="required" maxLength="100" tabIndex="1" autoFocus="autofocus" value={formData.name} onChange={HandleUsernameChange} />
                        </div>
                        <div className="password">
                            <label className="inputLabel" htmlFor="password">
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