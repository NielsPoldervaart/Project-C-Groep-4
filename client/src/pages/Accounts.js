import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react'
import '../style/Accounts.css'
import Loader from '../components/Loader';

const Accounts = () => {
    let navigate = useNavigate();

    const [accountsData, setAccountsData] = useState("")
    const [loading, setLoading] = useState(true);

    const [values, setValues] = useState({
        accepted: false,
    });

    const HandleAccept = () => {
        setValues({...values, accepted: true})
    }

    const HandleDecline = () => {
        setValues({...values, accepted: false})
        YeetUser();
    }

    const YeetUser = () => {
        //keeg
    }

    const DisplayLoader = () => {
        return (
          <div className='loaderDiv'>
            <Loader />
          </div>
        )
    }

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
            }
        )
    });

    return (
        <div className="Accounts">
            <div className="AccountsText">
                {loading ? DisplayLoader() : <div className='loadedAccounts' dangerouslySetInnerHTML={{__html: accountsData}}/>}
            </div>
        </div>
    )
};

export default Accounts;