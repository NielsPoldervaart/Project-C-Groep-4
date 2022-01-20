import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react'
import '../style/Accounts.css'
import Loader from '../components/Loader';

const Accounts = () => {
    let navigate = useNavigate();

    const [loading, setLoading] = useState(true);

    useEffect(async () => {
        let userData = {};
  
        await fetch(`/login`).then(
          res => res.json()
        ).then(
          data => {
              if (data.Code === 500 || data.Code === 404) {
                window.location.href = "/login";
              } else {
                userData = data;
              }
          }
        )

        fetch(`/accounts/${userData.company_company_id}`).then(
            res => res.json()
        ).then(
            data => {
                console.log(data)
                setLoading(false);
            }
        )
    });

    const DisplayLoader = () => {
        return (
          <div className='loaderDiv'>
            <Loader />
          </div>
        )
    }

    const DisplayAccounts = () => {
        return (
            <div>
                <div className='accountsList'>
                    <div className='account'>
                    </div>
                </div>
            </div>
          )
    }

    return (
        <div className="Accounts">
            <div className="AccountsText">
                {loading ? DisplayLoader() : DisplayAccounts}
            </div>
        </div>
    )
};

export default Accounts;