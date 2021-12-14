import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
  let navigate = useNavigate();

  useEffect(() => {
    fetch(`/logout`)
    .then(res => res.json())
    .then(
        data => {
            if (data.Code === 201) {
                navigate('/login')
                console.log("Logout succesful!")
            }
        }
    ).catch(error => console.log('Logout failed : ' + error.message));
  }, [])

    return (
        <div>
            <h1>Logout</h1>
        </div>
    );
};
  
export default Logout;