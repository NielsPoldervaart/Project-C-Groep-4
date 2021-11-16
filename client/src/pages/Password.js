import './Password.css';

const Password = () => {
    return (
        <div className="Password">
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
                <h1>FORGOT PASSWORD</h1>
            </nav>
        </div>
    );
};
  
export default Password;