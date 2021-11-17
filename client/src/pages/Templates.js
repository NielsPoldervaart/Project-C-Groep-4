import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router';
import { useNavigate } from 'react-router-dom';
import { FaRegTrashAlt, FaRegEye, FaPlusCircle } from 'react-icons/fa';
import '../style/Templates.css';

const Templates = () => {
    let navigate = useNavigate();

    const { company_id } = useParams()
    const [templates, setTemplates] = useState([])

    useEffect(() => {
        fetch(`/templates/${company_id}`).then(
            res => res.json()
          ).then(
            data => {
              setTemplates(data)
            }
          )
    }, [company_id])

    return (
        <div className="Body">
            <h1 className="CompanyName">Company Name</h1>
            <ul className="TemplateList">
                {
                    templates.map((template) => 
                        <div className="TemplateComp">
                            <h2 className="TitleCard">Template {template.template_id}</h2>
                            <div key={template.template_id} className="TemplateCard">
                                <p className="CardIcon View" onClick={() => navigate(`/${company_id}/${template.template_id}`)}><FaRegEye /></p>
                                <p className="CardIcon Delete"><FaRegTrashAlt /></p>
                            </div>
                        </div>
                    )
                }
                <div className="NewTempBox">
                    <FaPlusCircle className="NewTempButton" onClick={() => console.log("Select new template")}/>
                </div>
            </ul>

        </div>
    );
};
  
export default Templates;