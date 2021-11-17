import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router';
import '../style/Template.css';

const Template = () => {
    const { company_id, template_id } = useParams()
    
    const [template, setTemplate] = useState([])

    useEffect(() => {
        fetch(`/template/${company_id}/${template_id}`).then(
            res => res.json()
          ).then(
            data => {
              setTemplate(data)
              console.log(data)
            }
          )
    }, [company_id, template_id])

    return (
        <div className="EditTempComp">
            <div className="EditBox">
              <h1>test</h1>
            </div>
            <div className="TemplateBox">

            </div>
        </div>
    );
};
  
export default Template;