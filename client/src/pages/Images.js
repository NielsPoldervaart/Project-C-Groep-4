import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router';
import { useNavigate } from 'react-router-dom';
import Loader from '../components/Loader';
import '../style/Images.css'

const Images = () => {
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

      fetch(`/images/${userData.company_company_id}`).then(
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

    const DisplayElement = () => {
      return (
        <div>
            <div className='imageList'>
                <div className='image'>
                </div>
            </div>
        </div>
      )
    }

    return (
        <div className="Images">
            <div className="ImagesText">
                { loading ? DisplayLoader() :  DisplayElement()}
            </div>
        </div>
    )
};

export default Images;