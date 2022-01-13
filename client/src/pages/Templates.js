import React, { useState, useEffect, useRef } from 'react'
import { useParams } from 'react-router';
import { useNavigate } from 'react-router-dom';
import { FaRegTrashAlt, FaRegEye, FaPlusCircle } from 'react-icons/fa';
import Loader from '../components/Loader';
import '../style/Templates.css';

const Templates = () => {
    let navigate = useNavigate();

    const { company_id } = useParams();

    const [templates, setTemplates] = useState([]);
    const [company, setCompany] = useState([]);
    const [loading, setLoading] = useState(true);
    const [madeTemplate, setMadeTemplate] = useState(false);

    const inputFile = useRef(null);

    useEffect(() => {
        fetch(`/templates/${company_id}`).then(
          res => res.json()
        ).then(
          data => {
            setTemplates(data)
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
    }, [company_id]);

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

        setMadeTemplate(true);

        var templateHTML = parsedTemplate.querySelector("html");
        document.querySelector(".templateBody").appendChild(templateHTML);
        let htmlString = document.querySelector(".templateBody").innerHTML;

        setMadeTemplate(false);

        
        let template = new File([htmlString], htmlArr[0].name, {type: "text/html", lastModified: new Date(0)});
        uploadFile(template);

        // document.querySelector(".templateBody").addEventListener('click', (e) => {
        //     if (e.target.classList.contains("templateText") || e.target.classList.contains("templateImage")) {
        //         // e.target.classList.add("selectedElement");
        //     }
        // });
      }

    const uploadFile = (file) => {

      const data = new FormData();
      data.append("File", file);

      if (file === null) {
          alert("Make template first!");
      } else {
          console.log(file);
      }

      console.log("Post");
      // fetch('/singlefile', {
      //     method: 'POST',
      //     body: data,
      // })
      // .then(res => {
      //   res.json()
      //   console.log(res);
      // })
      // .catch(error => console.log('Authorization failed : ' + error.message));
    }

    const DisplayLoader = () => {
      return (
        <div className='loaderDiv'>
          <Loader />
        </div>
      )
    }

    const DisplayHidden = () => {
      return (
        <div className='templateBody' style={{display: 'none'}}>
        </div>
      )
    }

    const DisplayElement = () => {
      if (templates.errorCode === 401) {
        navigate(`/login`)
      }
      else {
        return (
          <div className="TemplatesBody">
          
            <h1 className="CompanyName">{company.Company_name}</h1>
            <ul className="TemplateList">
                {
                    templates.map((template) => 
                        <div className="TemplateComp"  key={template.template_id}>
                            <h2 className="TitleCard">Template {template.template_id}</h2>
                            <div className="TemplateCard">
                                <p className="CardIcon View" onClick={() => navigate(`/${company_id}/${template.template_id}`)}><FaRegEye /></p>
                                <p className="CardIcon Delete"><FaRegTrashAlt /></p>
                            </div>
                        </div>
                    )
                }
                <div className="NewTempBox">
                    <FaPlusCircle className="NewTempButton" onClick={() => inputFile.current.click()}/>
                    <input name='Dir' id='DirInput' type='file' multiple="" directory="" webkitdirectory="" mozdirectory="" ref={inputFile} style={{display: 'none'}} onChange={splitFiles} />
                </div>
            </ul>
            { madeTemplate ? DisplayHidden() : null }
          </div>
        )
      }
    }

    return (
      <div>
          { loading ? DisplayLoader() : DisplayElement() }
      </div>
    );
};
  
export default Templates;