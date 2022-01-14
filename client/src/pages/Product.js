import React, { useEffect } from 'react'
import { useParams } from 'react-router';
import '../style/Product.css';

const Template = () => {

    const { company_id, template_id } = useParams();

    useEffect(() => {
        fetch(`/template/${company_id}/${template_id}`).then(
            res => res.text()
          ).then(
            data => {
              console.log(data);
            }
          )
    }, [company_id, template_id]);

    return (
        <div>
        </div>
    );
};
  
export default Template;