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
                    <div className='awaitingUsers'> AWAITING USERS
                        {
                            awaitingUsers.map((user) => 
                                <div className='id'>{user.user_id}
                                    <div className='email'>{user.email}
                                        <div className='username'>{user.username}
                                            <div className='role'>{user.user_role}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )
                        }
                    </div>
                    <div className='verifiedUsers'> VERIFIED USERS
                        {
                            verifiedUsers.map((user) => 
                                <div className='id'>{user.user_id}
                                    <div className='email'>{user.email}
                                        <div className='username'>{user.username}
                                            <div className='role'>{user.user_role}
                                            </div>
                                        </div>
                                    </div>
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