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

    return (
        <div className="EditTempComp">
            <div className="EditBox">
              <form onSubmit={HandleSubmit} className="TempForm">

                <div className="TitleComp">
                  <label className="TitleLabel">Title</label>
                  <input className="TitleField" type="title" name="title" value={values.title} onChange={HandleTitleChange}/>
                </div>
                
                <div className="TextComp">
                  <label className="TextLabel">Text</label>
                  <textarea className="TextField" value={values.text} name="text" onChange={HandleTextChange} />
                </div>

                <div className="SelectComp">
                  <label className="SelectLabel">Background image</label>
                  <select className="SelectBox" value={values.image} onChange={HandleImageChange}>
                    <option className="SelectOption" value="https://via.placeholder.com/350x250/FF00BA/FFFFFF/?text=Achtergrond-1">Achtergrond-1</option>
                    <option className="SelectOption" value="https://via.placeholder.com/350x250/D22E12/FFFFFF/?text=Achtergrond-2">Achtergrond-2</option>
                    <option className="SelectOption" value="https://via.placeholder.com/350x250/4D4D4D/FFFFFF/?text=Achtergrond-3">Achtergrond-3</option>
                  </select>
                </div>

                <div className="ButtonsComp">
                  <input className="DeleteButton" type="button" value="Delete" onClick={() => window.confirm('Weet u zeker dat u de template wilt verwijderen?')} />
                  <input className="SaveButton" type="submit" value="Save" />
                </div>
                
              </form>
            </div>
            <div className="TemplateBox" id='TemplateBox'>
              {/* <iframe src="../templates/template1.html" className="LoadedTemplate"/> */}
              {loading ? <Loader /> : <div dangerouslySetInnerHTML={{__html: templateData}}/>}
            </div>
        </div>
    );
};
  
export default Template;