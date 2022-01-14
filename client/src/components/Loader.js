import React from 'react'
import '../style/Loader.css';

const Loader = () => {
    return (
        <div className='loaderElement'>
            <div>
                <span className="loader" />
                <h1 className='loaderText'>Loading...</h1>
            </div>
        </div>
    )
}

export default Loader
