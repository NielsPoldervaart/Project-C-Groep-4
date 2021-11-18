import '../style/Login.css';

const Login = () => {
    return (
        <div className="login">
            <div className="loginBox">
                <div className="logoBox">
                    <img src="https://excelsiorrotterdam.nl/wp-content/uploads/2018/01/kynda_web.png" alt="kyndaLogo" width="250" />    
                </div>
                <form className="loginForm" method="post" action id="form">
                    <div className="loginInput">
                        <div className="email">
                            <label className="inputLabel" for="email">
                            E-mail
                            </label>
                            <input className="inputInput" type="text" name="email" id="email" required="required" maxLength="100" tabIndex="1" autoFocus="autofocus" />
                        </div>
                        <div className="password">
                            <label className="inputLabel" for="password">
                            Wachtwoord
                            </label>
                            <input className="inputInput" type="password" name="password" id="password" required="required" maxLength="100" tabIndex="2" autoComplete="off" />
                        </div>
                    </div>
                    <div className="loginButton">
                        <button className="button" type="submit" id="button">
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