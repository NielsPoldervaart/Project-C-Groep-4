import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router';
import '../style/Template.css';
import Loader from '../components/Loader';

const Template = () => {

    const { company_id, template_id } = useParams()
    const [templateData, setTemplateData] = useState("")
    const [loading, setLoading] = useState(true);
    
    const [values, setValues] = useState({
      title: "",
      text: "",
      image: "",
    });

    const HandleTitleChange = (e) => {
      setValues({...values, title: e.target.value})
    }

    const HandleTextChange = (e) => {
      setValues({...values, text: e.target.value})
    }

    const HandleImageChange = (e) => {
      setValues({...values, image: e.target.value})
    }

    const HandleSubmit = (e) => {
      e.preventDefault();
      alert('De template is opgeslagen!')
    }

    useEffect(() => {
        fetch(`/template/${company_id}/${template_id}`).then(
            res => res.text()
          ).then(
            data => {
              setTemplateData(data)
              setLoading(false)
            }
          )
    }, [company_id, template_id])

    const DisplayLoader = () => {
      return (
        <div className='loaderDiv'>
          <Loader />
        </div>
      )
    }

    return (
        <div className="EditTempComp">
            <div className="TemplateBox" id='TemplateBox'>
              {/* <iframe src="../templates/template1.html" className="LoadedTemplate"/> */}
              {loading ? DisplayLoader() : <div className='loadedTemplate' dangerouslySetInnerHTML={{__html: templateData}}/>}
            </div>
        </div>
    );
};
  
export default Template;