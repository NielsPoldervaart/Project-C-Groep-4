import React, { useState } from 'react'
import '../style/Template.css';

const Template = () => {

    const [template, setTemplate] = useState(null);

    // const data = new FormData();

    // const handleChange = e => {
    //     const fileData = document.querySelector('input[type="file"]').files[0];
    //     data.append("File", fileData);
    // };

    const testStyle = {
        display: 'none',
    }

    const splitFiles = e => {
        let arr = Object.entries(e.target.files);
        let hasCSS = false;
        let hasHTML = false;

        let imgArr = [];
        let cssArr = [];
        let htmlArr = [];

        for (let i = 0; i < arr.length; i++) {
            const el = arr[i];

            // Image Files
            if (el[1].name.includes('.png') || el[1].name.includes('.jpg') || el[1].name.includes('.jpeg')) {

                let imgReader = new FileReader();
                
                imgReader.onloadend = () => {
                    imgArr.push({name: el[1].name, data: imgReader.result});
                }
                imgReader.readAsDataURL(el[1]);
            }
            // CSS File
            else if (el[1].name.includes('.css')) {
                hasCSS = true;

                let cssReader = new FileReader();
                
                cssReader.onloadend = () => {
                    cssArr.push({name: el[1].name, data: cssReader.result});
                }
                cssReader.readAsBinaryString(el[1]);
                
            }
            // HTML Files
            else if (el[1].name.includes('.html')) {
                hasHTML = true;
                
                let htmlReader = new FileReader();
                
                htmlReader.onloadend = () => {
                    htmlArr.push({name: el[1].name, data: htmlReader.result});
                }
                htmlReader.readAsBinaryString(el[1]);

            }
        }

        if (hasHTML === false || hasCSS === false) {
            const input = document.getElementById('DirInput');
            input.value = null;
            alert("Invalid folder, please select another one!");
            
            return
        }
        else {
            console.log(imgArr, cssArr, htmlArr);
            console.log(imgArr.length, cssArr.length, htmlArr.length);
            // createBaseProduct(imgArr, cssArr, htmlArr);
        }

    }

    // const createBaseProduct = (imgArr, cssArr, htmlArr) => {
        
    //     console.log(imgArr, cssArr, htmlArr);
    //     console.log(imgArr.length, cssArr.length, htmlArr.length);

    //     // let f = new File([htmlArr[0].data], htmlArr[0].name, {type: "text/html", lastModified: new Date(0)})
    //     // let tempReader = new FileReader();
    //     // tempReader.readAsText(f);

    //     // tempReader.onloadend = () => {
    //     //     let templateString = tempReader.result;

    //     //     let parser = new DOMParser();
    //     //     let parsedTemplate = parser.parseFromString(templateString, 'text/html');
    //     //     parsedTemplate.querySelector("head link").remove();

    //     //     var styleElement = document.createElement("STYLE");
    //     //     styleElement.innerHTML = cssArr[0].data; 
    //     //     parsedTemplate.querySelector("head").appendChild(styleElement);

    //     //     var tempHTML = parsedTemplate.querySelector("html");
    //     //     document.querySelector(".templateBody").appendChild(tempHTML);

    //     //     // For each element inside the dict, grab the key and add . infront of key
    //     //     // then for each element that contains the value above ^ replace the backgroundImage calue with the dataURL
    //     //     // check if there is a way to disable the error message that pops up
    //     //     // check for a way to disable the style from the template to apply on the website and vice versa

    //     //     // console.log(parsedTemplate.querySelectorAll('body *'));
    //     //     // setTemplate(parsedTemplate);
    //     //     // console.log(parsedTemplate);
    //     // }
    // }

    const uploadDir = (e) => {
        e.preventDefault()

        var el = document.querySelector(".x13a0159baggerenschoonouwenapril2020");
        var test = window.getComputedStyle(el);
        
        console.log(test.backgroundImage);

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
                <input name='Dir' className='DirInputBar' id='DirInput' type='file' multiple="" directory="" webkitdirectory="" mozdirectory="" onChange={splitFiles} />
                {/* <input name='File' className='FileInputBar' type='file' onChange={handleChange}/> */}
                <input type="submit" value="Upload" />
            </form>
            <div className='templateBody' style={testStyle}>

            </div>
        </div>
    )
}

export default Template
