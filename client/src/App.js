import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './pages/Login';
import Template from './pages/Template';
import Templates from './pages/Templates';

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">Tamplates</Link>
        <Link to="/">Tamplate</Link>
        <Link to="/login">Login</Link>
      </nav>
      <Routes>
        <Route path="/:company_id" element={<Templates />}/>
        <Route path="/:company_id/:template_id" element={<Template />}/>
        <Route path="/login" element={<Login />}/>
      </Routes>
    </Router>
  );
}

export default App;
