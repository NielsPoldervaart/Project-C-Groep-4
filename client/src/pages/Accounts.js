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
        //TODO: delete declined account from database
    }

    const DisplayLoader = () => {
        return (
          <div className='loaderDiv'>
            <Loader />
          </div>
        )
    }

    return (
        <div className="Accounts">
            <div className="AccountsText">
                {loading ? DisplayLoader() : <div className='loadedAccounts' dangerouslySetInnerHTML={{__html: accountsData}}/>}
            </div>
        </div>
    )
};

export default Accounts;