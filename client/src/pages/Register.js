import './Register.css';

const Register = () => {
    return (
        <div className="Register">
            <div className="kyndaBackground">
                <div className="gradientWrapper">
                    <div className="linear-gradient"></div>
                    <div className="radial-gradient"></div>
                </div>
            </div>

            <nav className="header">
                <a className="headerLink" href="/">
                    <img src="https://assets.website-files.com/5f5210d08f59cd33456fb659/5f5210d08f59cd67186fb79a_kyndalogo.svg" alt="kyndaLogo" />
                    <div className="logoBlockStripe"></div>
                </a>
            </nav>

            <div className="registerBox">
                <div className="headerBox">
                    Account aanvragen
                </div>
                <form className="registerForm" method="post" action id="form">
                    <div className="registerInput">
                        <div className="registerName">
                            <label className="inputLabel" for="name"> Naam </label>
                            <input className="inputInput" type="text" name="name" id="name" required="required" maxLength="100" tabIndex="1" />
                        </div>
                        <div className="registerEmail">
                            <label className="inputLabel" for="email"> E-mail </label>
                            <input className="inputInput" type="text" name="email" id="email" required="required" maxLength="100" tabIndex="2" />
                        </div>
                        <div className="registerPassword">
                            <label className="inputLabel" for="password"> Wachtwoord </label>
                            <input className="inputInput" type="password" name="password" id="password" required="required" maxLength="100" tabIndex="3" autoComplete="off" />
                        </div>
                    </div>
                    <div className="registerButton">
                        <button className="buttonR" type="submit" id="button">
                            <span className="buttonLabel">Account aanvragen</span>
                        </button>
                    </div>
                </form>
            </div>

        </div>
    );
};
  
export default Register;