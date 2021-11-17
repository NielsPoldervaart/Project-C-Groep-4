import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router';

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
        <div>
            <h1>Template - {template_id}</h1>
            <p>
                Company ID = {template.Company_company_id}
                <br/>
                File Path = {template.Template_file} - Template ID = {template.template_id}
                <br/>
            </p>
        </div>
    );
};
  
export default Template;