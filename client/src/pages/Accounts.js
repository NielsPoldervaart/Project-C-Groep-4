import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router';
import React, { useState, useEffect } from 'react'
import '../style/Accounts.css'
import Loader from '../components/Loader';

const Accounts = () => {
    let navigate = useNavigate();

    const { company_id } = useParams();

    const [awaitingUsers, setAwaitingUsers] = useState([]);
    const [verifiedUsers, setVerifiedUsers] = useState([]);
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
                setAwaitingUsers(data.Awaiting_users);
                setVerifiedUsers(data.Verified_users);
                setLoading(false);
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
        return (
            <div>
                <div className='accountsList'>
                    <div className='awaitingUsers'> Accounts in afwachting
                        <div className='userInfo'>
                            <p className='id'>Id</p>
                            <p className='email'>Email</p>
                            <p className='username'>Gebruikersnaam</p>
                            <p className='role'>Rol</p>
                        </div>
                        {
                            awaitingUsers.map((user) => 
                                <div className='userInfo'>
                                    <p className='id'>{user.user_id}</p>
                                    <p className='email'>{user.email}</p>
                                    <p className='username'>{user.username}</p>
                                    <p className='role'>{user.user_role}</p>
                                    <button className='acceptButton'>✓</button>
                                    <button className='declineButton'>✗</button>
                                </div> 
                            )
                        }
                    </div>
                    <div className='verifiedUsers'> Bestaande accounts
                        <div className='userInfo'>
                            <p className='id'>Id</p>
                            <p className='email'>Email</p>
                            <p className='username'>Gebruikersnaam</p>
                            <p className='role'>Rol</p>
                        </div>
                        {
                            verifiedUsers.map((user) => 
                                <div className='userInfo'>
                                    <p className='id'>{user.user_id}</p>
                                    <p className='email'>{user.email}</p>
                                    <p className='username'>{user.username}</p>
                                    <p className='role'>{user.user_role}</p>
                                </div>
                            )
                        }
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="Accounts">
            <div className="AccountsText">
                {loading ? DisplayLoader() : DisplayAccounts()}
            </div>
        </div>
    )
};

export default Accounts;