import React, { useState } from 'react'
import '../style/Template.css';

const Template = () => {

    const [template, setTemplate] = useState("");

    // const data = new FormData();

    // const handleChange = e => {
    //     const fileData = document.querySelector('input[type="file"]').files[0];
    //     data.append("File", fileData);
    // };

    const handleChangeFiles = e => {
        let arr = Object.entries(e.target.files)
        let isValid = false;
        let htmlFile;
        let cssFile;
        var imgDict = {};

        for (let i = 0; i < arr.length; i++) {
            const el = arr[i];

            // Image Files
            if (el[1].name.includes('.png') || el[1].name.includes('.jpg') || el[1].name.includes('.jpeg')) {
                let imgFile = el[1];

                let imgReader = new FileReader();
                imgReader.readAsDataURL(imgFile);

                imgReader.onloadend = function(){
                    let dataUrl = imgReader.result;
                    imgDict[el[1].name] = dataUrl;
                }
            }
            // CSS File
            else if (el[1].name.includes('.css')) {
                let cssReader = new FileReader();
                cssReader.readAsText(el[1]);

                cssReader.onloadend = function(){
                    cssFile = cssReader.result;
                }
            }
            //HTML File
            else if (el[1].name.includes('.html')) {
                isValid = true;

                htmlFile = el[1];

                let htmlReader = new FileReader();
                htmlReader.readAsBinaryString(htmlFile);

                htmlReader.onloadend = function(){
                    let f = new File([htmlReader.result], htmlFile.name, {type: "text/html", lastModified: new Date(0)})
                    let tempReader = new FileReader();
                    tempReader.readAsText(f);

                    tempReader.onloadend = function(){
                        let templateString = tempReader.result;

                        let parser = new DOMParser();
                        let parsedTemplate = parser.parseFromString(templateString, 'text/html');

                        console.log(cssFile);

                        //TODO: Parse .css file and add styling per class to each respective html element.
                        //TODO: splice .css file from arr
                        //TODO: Change all the .png's inside arr to DataUrl's and change the .css image url's with the dataUrl's
                    }
                }

                
                // setTemplate(htmlFile);
            }
        }

        if (isValid === false) {
            const input = document.getElementById('DirInput');
            input.value = null;
            alert("Invalid folder, please select another one!");
            
            return
        }
    };

    const uploadDir = (e) => {
        e.preventDefault()

        // if (template === "") {
        //     alert("Make template first!");
        // } else {
        //     console.log(template);
        // }

        // console.log("Post")
        // fetch('/singlefile', {
        //     method: 'POST',
        //     body: data,
        // })
        // .then(res =>  res.json())
        // .catch(error => console.log('Authorization failed : ' + error.message));
    }

    return (
        <div>
            <form method="post" id="DirForm" onSubmit={(e) => uploadDir(e)}>
                <input name='Dir' className='DirInputBar' id='DirInput' type='file' multiple="" directory="" webkitdirectory="" mozdirectory="" onChange={handleChangeFiles} />
                {/* <input name='File' className='FileInputBar' type='file' onChange={handleChange}/> */}
                <input type="submit" value="Upload" />
            </form>
        </div>
    )
}

export default Template
