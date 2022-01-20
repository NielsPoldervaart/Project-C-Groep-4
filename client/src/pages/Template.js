import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import Loader from '../components/Loader';
import EditOverlay from '../components/EditOverlay';
import '../style/Template.css';

const Template = () => {
    const { company_id, template_id } = useParams();

    const [loading, setLoading] = useState(true);
    const [overlay, setOverlay] = useState(false);
    const [isTextOverlay, setIsTextOverlay] = useState(null);
    const [elementText, setElementText] = useState("");
    const [element, setElement] = useState(null);
    const [editable, setEditable] = useState(true);

    const [userData, setUserData] = useState({});

    useEffect(() => {
        async function fetchData() {
            let userData = {};

            await fetch(`/login`).then(
                res => res.json()
            ).then(
                data => {
                    if (data.Code === 500 || data.Code === 404) {
                        window.location.href = "/login";
                    } else {
                        userData = data;
                        setUserData(data);
                    }
                }
            )

            fetch(`/template/${userData.company_company_id}/${template_id}`, {
                method: 'GET'
            }).then(
                res => res.text()
              ).then(
                data => {
                    setLoading(false);
                    editTemplate(data);
                }
            )
        }

        fetchData();
    }, [company_id, template_id]);

    const editTemplate = (data) => {
        let parser = new DOMParser();
        let parsedTemplate = parser.parseFromString(data, "text/html");

        var templateHTML = parsedTemplate.querySelector("html");
        document.querySelector(".templateBody").appendChild(templateHTML);

        document.querySelector(".templateBody").addEventListener('click', (e) => {
            if (e.target.classList.contains("templateText")) {
                setElementText(e.target.innerText);
                setIsTextOverlay(true);
                setElement(e.target);
                if (e.target.classList.contains("editable")) {
                    setEditable(true);
                }
                else {
                    setEditable(false);
                }

                showOverlay();
            }
            else if (e.target.classList.contains("templateImage")) {
                setIsTextOverlay(false);
                setElement(e.target);
                if (e.target.classList.contains("editable")) {
                    setEditable(true);
                }
                else {
                    setEditable(false);
                }

                showOverlay();
            }
        });
    }

    const showOverlay = () => {
        setOverlay(prev => !prev);
    }

    const editElement = (el, value, isText, editable) => {
        if (isText === true) {
            let className = el.className.split(" ")[0];
            var element = document.getElementsByClassName(className)[0];
            element.textContent = value

            if (element.classList.contains("editable") && !editable) {
                element.classList.remove("editable");
            }
            else if (!element.classList.contains("editable") && editable) {
                element.classList.add("editable");
            }
        }
        else {
            console.log(el);
            console.log(value);
        }
    }

    const displayOverlay = () => {

        return (
            <EditOverlay elementText={elementText} overlay={overlay} isTextOverlay={isTextOverlay} setOverlay={setOverlay} setElementText={setElementText} element={element} editable={editable} setEditable={setEditable} editElement={editElement}/>
        )
    }

    const displayLoader = () => {
        return (
          <div className='loaderDiv'>
            <Loader />
          </div>
        )
    }

    const uploadEdit = (e, userData) => {
        e.preventDefault();

        let htmlString = document.querySelector(".templateBody").innerHTML;
        let templateName = document.querySelector(".templateBody html body div").className.split(" ")[0];
        let updatedTemplate = new File([htmlString], templateName, {type: "text/html", lastModified: new Date(0)});

        const data = new FormData();
        data.append("file", updatedTemplate);

        // fetch(`/template/${userData.company_company_id}/${template_id}`, {
        //     method: 'POST',
        //     body: data,
        // })
        // .then(res => {
        //     res.json();
        //     console.log(res);
        //     // window.location.href = `/${userData.company_company_id}`;
        // })
        // .catch(error => console.log('Authorization failed : ' + error.message));
    }

    const displayElement = () => {
        return (
            <div>
                <div className='editPage'>
                    <div className="templateBody">
                    </div>
                    <div className='editFunctionBtns'>
                        <form onSubmit={(e) => uploadEdit(e)}>
                            <input type="button" value="Annuleren" className='editAnnulerenBtn' onClick={() => window.location.href = `/${userData.company_company_id}`}/>
                            <input type="submit" value="Opslaan" className='editOpslaanBtn' onClick={(e) => uploadEdit(e, userData)}/>
                        </form>
                    </div>
                </div>
                { overlay ? displayOverlay() : null }
            </div>
        )
    }

    return (
        <div>
            { loading ? displayLoader() : displayElement() }
        </div>
    )
}

export default Template
