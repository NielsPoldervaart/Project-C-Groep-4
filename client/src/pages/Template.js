import React, { useState } from 'react'
import '../style/Template.css';

const Template = () => {

    const [template, setTemplate] = useState(null);

    // const data = new FormData();

    // const handleChange = e => {
    //     const fileData = document.querySelector('input[type="file"]').files[0];
    //     data.append("File", fileData);
    // };

    const checkFile = (file) => {
        if (file.name.includes('.png') || file.name.includes('.jpg') || file.name.includes('.jpeg')) {
            return "image"
        }
        else if (file.name.includes('.css')) {
            return "css"
        }
        else if (file.name.includes('.html')) {
            return "html"
        }
    }

    const readFile = async (file) => {
        if (checkFile(file) === "image") {
            return new Promise((resolve, reject) => {
                let fr = new FileReader();  
    
                fr.onload = () => {
                  resolve(fr.result)
                };
                fr.onerror = reject;
    
                fr.readAsDataURL(file);
            });
        }
        else if (checkFile(file) === "html" || checkFile(file) === "css") {
            return new Promise((resolve, reject) => {
                let fr = new FileReader();  
    
                fr.onload = () => {
                  resolve(fr.result)
                };
                fr.onerror = reject;
    
                fr.readAsBinaryString(file);
            });
        }
    }

    const splitFiles = async (e) => {
        let arr = Object.entries(e.target.files);
        let hasCSS = false;
        let hasHTML = false;

        let imgArr = [];
        let cssArr = [];
        let htmlArr = [];

        for (let i = 0; i < arr.length; i++) {
            const el = arr[i];

            // Image Files
            if (checkFile(el[1]) === "image") {
                let data = await readFile(el[1]);
                imgArr.push({name: el[1].name, data: data});
            }
            // CSS File
            else if (checkFile(el[1]) === "css") {
                hasCSS = true;

                let data = await readFile(el[1]);
                cssArr.push({name: el[1].name, data: data});
            }
            // HTML Files
            else if (checkFile(el[1]) === "html") {
                hasHTML = true;

                let data = await readFile(el[1]);
                htmlArr.push({name: el[1].name, data: data});
            }
        }

        if (!hasHTML || !hasCSS) {
            const input = document.getElementById('DirInput');
            input.value = null;
            alert("Invalid folder, please select another one!");
            
            return
        }
        else {
            createBaseProduct(imgArr, cssArr, htmlArr);
        }
    }

    const overwriteCss = async (cssArr, imgArr) => {
        let css = cssArr[0].data;

        imgArr.forEach(imgObj => {
            if (css.includes(`assets/${imgObj.name}`)) {
                css = css.replace(`assets/${imgObj.name}`, imgObj.data);
            }
        });

        return css
    }

    const overwriteHtml = async (htmlArr, imgArr) => {
        let html = htmlArr[0].data;

        imgArr.forEach(imgObj => {
            if (html.includes(`assets/${imgObj.name}`)) {
                html = html.replace(`assets/${imgObj.name}`, imgObj.data);
            }
        });

        return html
    }

    const createBaseProduct = async (imgArr, cssArr, htmlArr) => {
        let newCss = await overwriteCss(cssArr, imgArr);
        let newHtml = await overwriteHtml(htmlArr, imgArr);

        let parser = new DOMParser();
        let parsedTemplate = parser.parseFromString(newHtml, "text/html");
        parsedTemplate.querySelector("head link").remove();

        let styleElement = document.createElement("STYLE");
        styleElement.textContent = newCss; 
        parsedTemplate.querySelector("head").appendChild(styleElement);

        let templateName = htmlArr[0].name;
        templateName = `.${templateName.replace('.html', '')}`;
        parsedTemplate.querySelector(templateName).style.overflow = "hidden";

        var templateHTML = parsedTemplate.querySelector("html");
        document.querySelector(".templateBody").appendChild(templateHTML);

        let htmlString = document.querySelector(".templateBody").innerHTML;

        // TODO: wordpress shit

        let f = new File([htmlString], htmlArr[0].name, {type: "text/html", lastModified: new Date(0)});
        let a = await readFile(f);

        console.log(a);

        // setTemplate(parsedTemplate);
        // console.log(parsedTemplate);
    }

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
                <input name='Dir' className='DirInputBar' id='DirInput' type='file' multiple="" directory="" webkitdirectory="" mozdirectory="" onChange={splitFiles} />
                {/* <input name='File' className='FileInputBar' type='file' onChange={handleChange}/> */}
                <input type="submit" value="Upload" />
            </form>
            <div className='templateBody'>

            </div>
        </div>
    )
}

export default Template
