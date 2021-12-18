import React, { useState } from 'react'
import '../style/Template.css';

const Template = () => {


    const data = new FormData();

    const handleChange = e => {
        const fileData = document.querySelector('input[type="file"]').files[0];
        data.append("File", fileData);
    };

    const uploadDir = (e) => {
        e.preventDefault()

        console.log("Post")
        fetch('/singlefile', {
            method: 'POST',
            body: data,
        })
        .then(res =>  res.json())
        .catch(error => console.log('Authorization failed : ' + error.message));
    }

    return (
        <div>
            <form method="post" action id="DirForm" onSubmit={(e) => uploadDir(e)}>
                {/* <input className='DirInputBar' type='file' multiple="" directory="" webkitdirectory="" mozdirectory="" onChange={handleChange}/> */}
                <input name='File' className='DirInputBar' type='file' onChange={handleChange}/>
                <input class="button" type="submit" value="Upload" />
            </form>
        </div>
    )
}

export default Template
