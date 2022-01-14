import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import Loader from '../components/Loader';
import '../style/Template.css';

const Template = () => {
    const { company_id, template_id } = useParams();

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`/template/${company_id}/${template_id}`).then(
            res => res.text()
          ).then(
            data => {
                setLoading(false);
                editTemplate(data);
            }
          )
    }, [company_id, template_id]);

    const editTemplate = (data) => {
        let parser = new DOMParser();
        let parsedTemplate = parser.parseFromString(data, "text/html");

        var templateHTML = parsedTemplate.querySelector("html");
        document.querySelector(".templateBody").appendChild(templateHTML);

        document.querySelector(".templateBody").addEventListener('click', (e) => {
            if (e.target.classList.contains("templateText") || e.target.classList.contains("templateImage")) {
                // e.target.classList.add("selectedElement");
                console.log(e.target);
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
            <div className='editPage'>
                <div className="templateBody">
                </div>
                <div className='editBox'>
                    <button>Save</button>
                    <button>Cancle</button>
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
