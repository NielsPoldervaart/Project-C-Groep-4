import React, { useState } from 'react'
import '../style/Template.css';
import Loader from '../components/Loader';

const Template = () => {

    const [template, setTemplate] = useState(null);
    const [loading, setLoading] = useState(false);
    const [hasTemplate, setHasTemplate] = useState(false);

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
        setLoading(true);
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
            createBaseTemplate(imgArr, cssArr, htmlArr);
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

    const createBaseTemplate = async (imgArr, cssArr, htmlArr) => {
        let newCss = await overwriteCss(cssArr, imgArr);
        let newHtml = await overwriteHtml(htmlArr, imgArr);

        setHasTemplate(true);

        let parser = new DOMParser();
        let parsedTemplate = parser.parseFromString(newHtml, "text/html");
        parsedTemplate.querySelector("head link").remove();

        let styleElement = document.createElement("STYLE");
        styleElement.textContent = newCss; 
        parsedTemplate.querySelector("head").appendChild(styleElement);

        let templateName = htmlArr[0].name;
        templateName = `.${templateName.replace('.html', '')}`;
        parsedTemplate.querySelector(templateName).style.overflow = "hidden";

        let children = parsedTemplate.querySelector(templateName).children
        for (var i = 0; i < children.length; i++) {
            var child = children[i];
            if (child.textContent !== "") {
                child.classList.add("templateText");
            }
        }

        imgArr.forEach(img => {
            let a = `${img.name.replace('.png', '')}`;
            for (var i = 0; i < children.length; i++) {
                var child = children[i];
                if (child.classList.contains(a)) {
                    child.classList.add("templateImage");
                }
            }
        });

        setLoading(false);

        var templateHTML = parsedTemplate.querySelector("html");
        document.querySelector(".templateBody").appendChild(templateHTML);

        // document.querySelector(".templateBody").addEventListener('click', (e) => {
        //     if (e.target.classList.contains("templateText") || e.target.classList.contains("templateImage")) {
        //         // e.target.classList.add("selectedElement");
        //     }
        // });
        
        // let htmlString = document.querySelector(".templateBody").innerHTML;
        // let template = new File([htmlString], htmlArr[0].name, {type: "text/html", lastModified: new Date(0)});
        // setTemplate(template);
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

    const DisplayLoader = () => {
        return (
          <div className='loaderDiv'>
            <Loader />
          </div>
        )
    }

    const DisplayElement = () => {
        if (loading === false && hasTemplate === false) {
            return (
                <form method="post" id="DirForm">
                    <input name='Dir' className='DirInputBar' id='DirInput' type='file' multiple="" directory="" webkitdirectory="" mozdirectory="" onChange={splitFiles} />
                </form>
            )
        }
        else {
            return (
                <div>
                    <div className='headerSpacing' />
                    <div className='templateBody'>

                    </div>
                </div>
                
            )
        }
    }

    // TODO: add if statement to or display upload shit, or the template with the custom menu
    return (
        <div>
            { loading ? DisplayLoader() : DisplayElement() }
        </div>
        
    )
}

export default Template
