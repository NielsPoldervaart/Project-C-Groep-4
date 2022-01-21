import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router';
import { useNavigate } from 'react-router-dom';
import { FaRegTrashAlt, FaRegEye, FaPlusCircle } from 'react-icons/fa';
import SelectTemplate from '../components/SelectTemplate';
import Loader from '../components/Loader';
import '../style/Products.css';

const Products = () => {
    let navigate = useNavigate();

    // URL Parameters
    const { company_id } = useParams();

    // State variables
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectTemplate, setSelectTemplate] = useState(false);
    const [templateReady, setTemplateReady] = useState(false);
    const [userData, setUserData] = useState(null);
    const [templateID, setTemplateID] = useState(null);

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
                    setUserData(data);
                }
            }
        )

        fetch(`/products/${userData.company_company_id}`).then(
          res => res.json()
        ).then(
            data => {
                setProducts(data);
                setLoading(false);
            }
        )
    }

    fetchData();
    }, [company_id]);

    // Loads the template when this function is called inside the <SelectTemplate /> component
    const loadTemplate = async (templateId) => {
        setLoading(true);
        setTemplateID(templateId);

        await fetch(`/template/${userData.company_company_id}/${templateId}`, {
            method: 'GET'
        }).then(
            res => res.text()
          ).then(
            data => {
                setLoading(false);
                DisplayTemplate(data);
            }
        )
    }

    // Makes a POST request with the templateId to make a product based of off the template with the id of templateId
    const uploadFile = (templateId) => {
        if (templateId === null) {
            console.error("No file to upload!");
            return
        }

        const data = new FormData();
        data.append("template_id", templateId);

        fetch(`/products/${userData.company_company_id}`, {
            method: 'POST',
            body: data,
        })
        .then(res => {
            res.json();
            window.location.reload();
        })
        .catch(error => console.log('Authorization failed : ' + error.message));
    }

    // Deletes the product
    const deleteProduct = (productID) => {
      fetch(`/product/${userData.company_company_id}/${productID}`, {
        method: 'DELETE'
      })
      .then(res => {
        res.json()
        window.location.reload();
      })
      .catch(error => console.log('Authorization failed : ' + error.message));
    }

    const DisplayLoader = () => {
      return (
        <div className='loaderDiv'>
          <Loader />
        </div>
      )
    }

    // Displays the template in the window after the fetch request is complete
    const DisplayTemplate = (template) => {
        setTemplateReady(true);
        setSelectTemplate(false);
        setLoading(false);

        let parser = new DOMParser();
        let parsedTemplate = parser.parseFromString(template, "text/html");

        var templateHTML = parsedTemplate.querySelector("html");
        document.querySelector(".templateBody").appendChild(templateHTML);
    }

    const TemplatesBody = () => {
        return (
            <div className="TemplatesBody">
                <ul className="TemplateList">
                    {
                        products.map((product) => 
                            <div className="TemplateComp"  key={product.product_id}>
                                <h2 className="TitleCard">Product {product.product_id}</h2>
                                <div className="TemplateCard">
                                    <p className="CardIcon View" onClick={() => navigate(`/product/${userData.company_company_id}/${product.product_id}`)}><FaRegEye /></p>
                                    <p className="CardIcon Delete" onClick={() => deleteProduct(product.product_id)}><FaRegTrashAlt /></p>
                                </div>
                            </div>
                        )
                    }
                    <div className="NewTempBox">
                        <FaPlusCircle className="NewTempButton" onClick={() => setSelectTemplate(true)}/>
                    </div>
                </ul>
            </div>
        )
    }

    const DisplayHidden = () => {
        return (
            <div className='templateBodyHidden' style={{display: 'none'}}>
            </div>
        )
    }

    const DisplayProducts = () => {
        return (
            <>
                { templateReady ? (
                    <>
                        <div className='templateBody'></div>
                        <div className='templateSelectOverlay'>
                            <div className='templateSelectBtns'>
                                <button className='selectBackBtn' onClick={() => setTemplateReady(false)}>Ga Terug</button>
                                <button className='selectTemplateBtn' onClick={() => uploadFile(templateID)}>Selecteer Template</button>
                            </div>
                        </div>
                    </>
                ) : TemplatesBody() }
            </>
        )
    }

    const DisplayElement = () => {
        return (
            <>
                { selectTemplate ? <SelectTemplate loadTemplate={loadTemplate} setSelectTemplate={setSelectTemplate}/> : DisplayProducts() }
            </>
        )
    }

    return (
        <>
            { loading ? DisplayLoader() : DisplayElement() }
            {  DisplayHidden() }
        </>
    );
};

export default Products
