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
                window.location.href = "/login";
            }
        }
    ).catch(error => console.error(`Logout failed : ${error.message}`));
  }, [navigate])

    return (
        <div>
            <h1>Logout</h1>
        </div>
    );
};
  
export default Logout;