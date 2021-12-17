import React, { useState } from 'react'
import '../style/Template.css';

const Template = () => {

    const [files, setFiles] = useState();


    const handleChange = e => {
        setFiles(e.target.files)
    };

    const uploadDir = (e) => {
        e.preventDefault()

        console.log("Post")
        fetch('/folder', {
            method: 'POST',
            body: files,
        })
        .then(res =>  res.json())
        .catch(error => console.log('Authorization failed : ' + error.message));
    }

    return (
        <div>
            <form method="post" action id="DirForm" onSubmit={(e) => uploadDir(e)}>
                <input className='DirInputBar' type='file' multiple="" directory="" webkitdirectory="" mozdirectory="" onChange={handleChange}/>
                <input class="button" type="submit" value="Upload" />
            </form>
        </div>
    )
}

export default Template
