import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router';
import React, { useState, useEffect } from 'react'
import '../style/Accounts.css'
import Loader from '../components/Loader';

const Accounts = () => {
    let navigate = useNavigate();

    const { company_id } = useParams();

    const [userData, setUserData] = useState({});
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
                setUserData(data);
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

    const acceptUser = (id) => {
        const data = new FormData();
        data.append("user_id", `${id}`);
        data.append("accepted", "True");

        fetch(`/${userData.company_company_id}/accounts`, {
            method : "POST",
            body : data,
        }).then(res => {
            res.json();
            window.location.reload();
        })
        .catch(error => console.log('Authorization failed : ' + error.message));
    }

    const declineUser = (id) => {
        const data = new FormData();
        data.append("user_id", `${id}`);
        data.append("accepted", "False");

        fetch(`/${userData.company_company_id}/accounts`, {
            method : "POST",
            body : data,
        }).then(res => {
            res.json();
            window.location.reload();
        })
        .catch(error => console.log('Authorization failed : ' + error.message));
    }
    
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
                            <p className='username'>Gebruikersnaam</p>
                            <p className='role'>Rol</p>
                        </div>
                        {
                            awaitingUsers.map((user) => 
                                <div className='userInfo' key={user.user_id}>
                                    <p className='id'>{user.user_id}</p>
                                    <p className='username'>{user.username}</p>
                                    <p className='role'>{user.user_role}</p>
                                    <button className='acceptButton' onClick={() => acceptUser(user.user_id)}>✓</button>
                                    <button className='declineButton' onClick={() => declineUser(user.user_id)}>✗</button>
                                </div> 
                            )
                        }
                    </div>
                    <div className='verifiedUsers'> Bestaande accounts
                        <div className='userInfo'>
                            <p className='id'>Id</p>
                            <p className='username'>Gebruikersnaam</p>
                            <p className='role'>Rol</p>
                        </div>
                        {
                            verifiedUsers.map((user) => 
                                <div className='userInfo' key={user.user_id}>
                                    <p className='id'>{user.user_id}</p>
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