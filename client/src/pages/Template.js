import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import Loader from '../components/Loader';
import EditOverlay from '../components/EditOverlay';
import ReadFile from '../components/ReadFile';
import '../style/Template.css';

const Template = () => {
    // URL Parameters
    const { company_id, template_id } = useParams();

    // State variables
    const [loading, setLoading] = useState(true);
    const [overlay, setOverlay] = useState(false);
    const [isTextOverlay, setIsTextOverlay] = useState(null);
    const [elementText, setElementText] = useState("");
    const [elementImage, setElementImage] = useState(null);
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

    // Edits the template after the fetch is complete
    const editTemplate = (data) => {
        let parser = new DOMParser();
        let parsedTemplate = parser.parseFromString(data, "text/html");

        // Displays the template in the window
        var templateHTML = parsedTemplate.querySelector("html");
        document.querySelector(".templateBody").appendChild(templateHTML);

        // EventListener to see if a editable element has been clicked
        document.querySelector(".templateBody").addEventListener('click', (e) => {
            if (e.target.classList.contains("templateText")) {
                setElementText(e.target.innerText);
                setIsTextOverlay(true);
                setElement(e.target);
                if (e.target.classList.contains("editableTxt")) {
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
                if (e.target.classList.contains("editableImg")) {
                    setEditable(true);
                }
                else {
                    setEditable(false);
                }

                showOverlay();
            }
        });
    }

    // Sets the setOverlay state to the opposite of the current boolean value
    const showOverlay = () => {
        setOverlay(prev => !prev);
    }

    // Edits the element with the values set inside the <EditOverlay /> component
    const editElement = async (el, value, isText, editable) => {
        if (isText === true) {

            let className = el.className.split(" ")[0];
            var element = document.getElementsByClassName(className)[0];
            element.textContent = value;

            if (element.classList.contains("editableTxt") && !editable) {
                element.classList.remove("editableTxt");
            }
            else if (!element.classList.contains("editableTxt") && editable) {
                element.classList.add("editableTxt");
            }
        }
        else {
            let className = el.className.split(" ")[0];
            var element = document.getElementsByClassName(className)[0];

            if (element.classList.contains("editableImg") && !editable) {
                element.classList.remove("editableImg");
            }
            else if (!element.classList.contains("editableImg") && editable) {
                element.classList.add("editableImg");
            }

            let dataUrl = await ReadFile(value);

            element.style.backgroundImage = `url(${dataUrl})`;
        }
    }

    // Calls the <EditOverlay /> component with all the props required
    // In this case the props are State values, Function references or a string
    const displayOverlay = () => {
        return (
            <EditOverlay 
                userData={userData} 
                elementText={elementText} 
                overlay={overlay} 
                isTextOverlay={isTextOverlay} 
                setOverlay={setOverlay} 
                setElementText={setElementText} 
                element={element} 
                editable={editable} 
                setEditable={setEditable} 
                editElement={editElement} 
                editType="template" 
                setElementImage={setElementImage}
                elementImage={elementImage}
            />
        )
    }

    // Displays the <Loader /> component while setLoading === true
    const displayLoader = () => {
        return (
          <div className='loaderDiv'>
            <Loader />
          </div>
        )
    }

    // Makes a POST request to upload the edited template to the FTP server
    const uploadEdit = (e, userData) => {
        e.preventDefault();

        // Creates htmlString from the elements inside ".templateBody"
        let htmlString = document.querySelector(".templateBody").innerHTML;
        let templateName = document.querySelector(".templateBody html body div").className.split(" ")[0];

        // Creates new file with the html code
        let updatedTemplate = new File([htmlString], `${templateName}.html`, {type: "text/html", lastModified: new Date(0)});

        // Creates a FormData object with the key "updated_template" and the value updatedTemplate
        const data = new FormData();
        data.append("updated_template", updatedTemplate);

        // Creates the POST request to the backend
        fetch(`/template/${userData.company_company_id}/${template_id}`, {
            method: 'POST',
            body: data,
        })
        .then(res => {
            res.json();
            console.log(res);
            window.location.href = `/templates/${userData.company_company_id}`;
        })
        .catch(error => console.log('Authorization failed : ' + error.message));
    }

    const displayElement = () => {
        return (
            <div>
                <div className='editPage'>
                    <div className="templateBody">
                    </div>
                    <div className='editFunctionBtns'>
                        <form onSubmit={(e) => uploadEdit(e)}>
                            <input type="button" value="Annuleren" className='editAnnulerenBtn' onClick={() => window.location.href = `/templates/${userData.company_company_id}`}/>
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
