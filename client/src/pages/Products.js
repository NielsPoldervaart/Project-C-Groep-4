import React, { useState, useEffect, useRef } from 'react'
import { useParams } from 'react-router';
import { useNavigate } from 'react-router-dom';
import { FaRegTrashAlt, FaRegEye, FaPlusCircle } from 'react-icons/fa';
import SelectTemplate from '../components/SelectTemplate';
import Loader from '../components/Loader';
import '../style/Products.css';

const Products = () => {
    let navigate = useNavigate();

    const { company_id } = useParams();

    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [madeProduct, setMadeProduct] = useState(false);
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

    const checkFile = (file) => {
        if (file.name.includes('.html')) {
            return "html"
        }
        else {
            return null
        }
    }

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

    const uploadFile = (templateId) => {
        if (templateId === null) {
            console.error("No file to upload!");
            return
        }

        // let templateName = document.querySelector(".templateBody html body div").className.split(" ")[0];
        // let htmlString = document.querySelector(".templateBody").innerHTML;

        // let parser = new DOMParser();
        // let parsedTemplate = parser.parseFromString(htmlString, "text/html");

        // let children = parsedTemplate.querySelector(`.${templateName}`).children
        // for (var i = 0; i < children.length; i++) {
        //     var child = children[i];
  
        //     if (child.classList.contains("templateText")) {
        //         child.classList.remove("templateText");
        //     }
        //     else if (child.classList.contains("templateImage")) {
        //         child.classList.remove("templateImage");
        //     }
        // }

        // var templateHTML = parsedTemplate.querySelector("html");
        // document.querySelector(".templateBodyHidden").appendChild(templateHTML);
        // htmlString = document.querySelector(".templateBodyHidden").innerHTML;

        // let newTemplate = new File([htmlString], `${templateName}.html`, {type: "text/html", lastModified: new Date(0)});

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
