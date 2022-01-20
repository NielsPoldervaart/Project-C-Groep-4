import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router';
import { useNavigate } from 'react-router-dom';
import Loader from '../components/Loader';
import '../style/Images.css'

const Images = () => {
    let navigate = useNavigate();

    const { company_id } = useParams()

    const [images, setImages] = useState([])
    const [company, setCompany] = useState([])
    const [imagesData, setImagesData] = useState("")
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`/images/${company_id}`).then(
          res => res.json()
        ).then(
          data => {
            setImages(data)
            setLoading(false)
          }
        )

        fetch(`/company/${company_id}`).then(
          res => res.json()
        ).then(
          data => {
            setCompany(data)
          }
        )
    }, [company_id])

    const DisplayLoader = () => {
      return (
        <div className='loaderDiv'>
          <Loader />
        </div>
      )
    }

    return (
        <div className="Images">
            <div className="ImagesText">
                { loading ? DisplayLoader() :  <div className='loadedAccounts' dangerouslySetInnerHTML={{__html: imagesData}}/>}
            </div>
        </div>
    )
};

export default Images;