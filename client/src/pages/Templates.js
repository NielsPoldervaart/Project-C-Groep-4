import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router';

const Templates = () => {
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
        <div>
            <ul>
                {
                    templates.map((template) => 
                    
                        <li key={template.template_id}>
                            {template.template_id} - {template.company_name} - {template.template_file} 
                        </li>
                    )
                }
            </ul>

        </div>
    );
};
  
export default Templates;