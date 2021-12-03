import React, { useState, useEffect } from 'react'

const Logout = () => {
    const [logoutData, setLogoutData] = useState([])

    useEffect(() => {
        fetch(`/logout`).then(
            res => res.json()
          ).then(
            data => {
              setLogoutData(data)
              console.log(data)
            }
          )
    }, [])

    return (
        <div>
            <h1>Logout</h1>
        </div>
    );
};
  
export default Logout;