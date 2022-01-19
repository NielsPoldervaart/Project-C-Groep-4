import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import Loader from '../components/Loader';
import EditOverlay from '../components/EditOverlay';
import '../style/Template.css';

const Template = () => {
    const { company_id, template_id } = useParams();

    const [loading, setLoading] = useState(true);
    const [textElProps, setTextElProps] = useState({
        text: "",
        editable: true,
    });

    useEffect(async () => {
        let userData = {};

        await fetch(`/login`).then(
            res => res.json()
        ).then(
            data => {
                if (data.Code === 500 || data.Code === 404) {
                    window.location.href = "/login";
                } else {
                    userData = data;
                }
            }
        )

        fetch(`/template/${userData.company_company_id}/${template_id}`).then(
            res => res.text()
          ).then(
            data => {
                setLoading(false);
                editTemplate(data);
            }
          )
    }, [company_id, template_id]);


    // Set element as state. when the element has been set as state, call editOverlay with the element as prop. As return use the html from the editOverlay component to render for the editBox
    const editBox = (el) => {
        setTextElProps({...textElProps, text: el.textContent});
        // document.querySelector(".editOverlay").style.display = "flex";
        return (
            <div>
                <EditOverlay el={el} />
            </div>
        )
    }

    const editTemplate = (data) => {
        let parser = new DOMParser();
        let parsedTemplate = parser.parseFromString(data, "text/html");

        var templateHTML = parsedTemplate.querySelector("html");
        document.querySelector(".templateBody").appendChild(templateHTML);

        document.querySelector(".templateBody").addEventListener('click', (e) => {
            if (e.target.classList.contains("templateText") || e.target.classList.contains("templateImage")) {
                // e.target.classList.add("selectedElement");
                editBox(e.target);
            }
        });
    }

    const displayLoader = () => {
        return (
          <div className='loaderDiv'>
            <Loader />
          </div>
        )
    }

    const displayElement = () => {
        return (
            <div>
                <div className='editPage'>
                    <div className="templateBody">
                    </div>
                </div>
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
