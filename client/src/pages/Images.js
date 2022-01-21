import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router';
import Loader from '../components/Loader';
import '../style/Images.css'

const Images = () => {
    const { company_id } = useParams();

    const [userData, setUserData] = useState({});
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

      fetch(`/gallery/${company_id}/${userData.Images}`).then(
          res => res.json()
      ).then(
          data => {
              userData = data;
              setUserData(data);
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
        <div style={{marginTop: "100px"}}>
            <div className='imageList'>Beeldbank
                <div className='image'>
                  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Solid_blue.svg/225px-Solid_blue.svg.png" alt="blue" width={"225px"} height={"225px"} margin={"10px"}/>
                  <img src="https://cdn.webshopapp.com/shops/66605/files/264371468/oracal-970-canary-yellow.jpg" alt="yellow" width={"225px"} height={"225px"}/>
                  <img src="https://www.onestopaerosols.co.uk/img/colours/ral-3028-pure-red.jpg" alt="red0" width={"225px"} height={"225px"}/>
                  <img src="https://upload.wikimedia.org/wikipedia/commons/f/f3/Green.PNG" alt="green" width={"225px"} height={"225px"}/>
                  <img src="https://media.tarkett-image.com/large/TH_3912025_3914025_800_800.jpg" alt="purple" width={"225px"} height={"225px"}/>
                  <img src="https://www.formica.com/nl-be/-/media/formica/emea/products/swatch-images/f0232/f0232-swatch.jpg?rev=5789750fca87402a9b25527ed5e9ddfa" alt="pink" width={"225px"} height={"225px"}/>
                  <img src="http://yarwoodleather.com/wp-content/uploads/2016/12/Yarwood-Leather-Style-Bright-Orange-01-scaled.jpg" alt="orange" width={"225px"} height={"225px"}/>
                  <img src="https://www.druma.nl/media/catalog/product/cache/87dec26021d579f23321b181f53e28bd/l/i/light-blue.jpg" alt="lightblue" width={"225px"} height={"225px"}/>
                </div>
            </div>
        </div>
      )
    }

    return (
        <div className="Images">
            <div className="ImagesText">
                { loading ? DisplayLoader() : DisplayElement()}
            </div>
        </div>
    )
};

export default Images;