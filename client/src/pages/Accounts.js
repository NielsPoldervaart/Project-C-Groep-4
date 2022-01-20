import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router';
import React, { useState, useEffect } from 'react'
import '../style/Accounts.css'
import Loader from '../components/Loader';

const Accounts = () => {
    let navigate = useNavigate();

    const { company_id } = useParams();

    const [accounts, setAccounts] = useState([]);
    const [company, setCompany] = useState([]);
    const [acceptedAccount, setAcceptedAccount] = useState(false);
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

        fetch(`/${userData.company_company_id}/accounts`).then(
            res => res.json()
        ).then(
            data => {
                setAccounts(data);
                console.log(data);
                setLoading(false);
            }
        )

        fetch(`/company/${userData.company_company_id}`).then(
            res => res.json()
          ).then(
            data => {
              setCompany(data)
            }
        )
    }, [company_id]);

    const DisplayLoader = () => {
        return (
          <div className='loaderDiv'>
            <Loader />
          </div>
        )
    }

    const DisplayAccounts = () => {
        if (accounts.errorCode === 401 || accounts.errorCode === 403) {
            window.location.href = "/login";
          }
        else {
            return (
                <div>
                    <div className='accountsList'>
                        <div className='nonAcceptedAccount'>
                            <div className='account'>
                            </div>
                        </div>
                        <div className='acceptedAccount'>
                            <div className='account'>
                            </div>
                        </div>
                    </div>
                </div>
            )
        }
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