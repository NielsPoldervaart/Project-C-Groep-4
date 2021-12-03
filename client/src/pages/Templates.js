import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router';
import { useNavigate } from 'react-router-dom';
import { FaRegTrashAlt, FaRegEye, FaPlusCircle } from 'react-icons/fa';
import '../style/Templates.css';

const Templates = () => {
    let navigate = useNavigate();

    const { company_id } = useParams()

    const [templates, setTemplates] = useState([])
    const [company, setCompany] = useState([])

    useEffect(() => {
        fetch(`/templates/${company_id}`).then(
          res => res.json()
        ).then(
          data => {
            setTemplates(data)
          }
        )

        fetch(`/company/${company_id}`).then(
          res => res.json()
        ).then(
          data => {
            setCompany(data)
          }
        )

        DisplayElement()
    }, [company_id])

    const DisplayElement = () => {

      if (templates.errorCode == 403) {
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
                    <FaPlusCircle className="NewTempButton" onClick={() => console.log("Select new template")}/>
                </div>
            </ul>

          </div>
        )
      }
    }

    return (
      <div>
        {
          DisplayElement()
        }
      </div>
        

    );
};
  
export default Templates;