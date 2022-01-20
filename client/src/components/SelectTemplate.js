import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom';
import { FaRegEye } from 'react-icons/fa';
import Loader from '../components/Loader';
import '../style/Templates.css';
import '../style/SelectedTemplate.css';

const SelectTemplate = ({loadTemplate, setSelectTemplate}) => {
    let navigate = useNavigate();

    const [templates, setTemplates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [company, setCompany] = useState(null);

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
                }
            }
        )

        fetch(`/templates/${userData.company_company_id}`).then(
          res => res.json()
        ).then(
          data => {
            setTemplates(data);
            setLoading(false);
          }
        )
  
        fetch(`/company/${userData.company_company_id}`).then(
          res => res.json()
        ).then(
          data => {
            setCompany(data)
          }
        )
    }

    fetchData();
    }, []);

    const DisplayLoader = () => {
      return (
        <div className='loaderDiv'>
          <Loader />
        </div>
      )
    }

    const DisplayElement = () => {
        return (
            <>
                <div className='productsBackBtnContainer'>
                    <button className='productsBackBtn' onClick={() => setSelectTemplate(prev => !prev)}>Ga Terug</button>
                </div>
                <div className="TemplatesBody">
                    <ul className="TemplateList">
                        {
                            templates.templates.map((template) => 
                                <div className="TemplateComp"  key={template.template_id}>
                                    <h2 className="TitleCard">Template {template.template_id}</h2>
                                    <div className="TemplateCard">
                                        <p className="CardIcon View" onClick={() => loadTemplate(template.template_id)}><FaRegEye /></p>
                                    </div>
                                </div>
                            )
                        }
                    </ul>
                </div>
            </>
            
        )
    }

    return (
      <div>
          { loading ? DisplayLoader() : DisplayElement() }
      </div>
    );
};
  
export default SelectTemplate;