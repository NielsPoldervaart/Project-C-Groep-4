import React, { useEffect } from 'react'

const Logout = () => {

    useEffect(() => {
        fetch(`/logout`).then(
            res => res.json()
          ).then(
            data => {
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