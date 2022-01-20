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
    const [templateId, setTemplateId] = useState(null);
    const [selectTemplate, setSelectTemplate] = useState(false);
    const [userData, setUserData] = useState(null);

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

    const readFile = async (file) => {
        if (checkFile(file) === "html") {
            return new Promise((resolve, reject) => {
                let fr = new FileReader();  
    
                fr.onload = () => {
                  resolve(fr.result)
                };
                fr.onerror = reject;
    
                fr.readAsBinaryString(file);
            });
        }
        else if (checkFile(file) === null) {
            console.error("Error, checkFile returned null");
        }
    }

    const createBaseProduct = async (imgArr, cssArr, htmlArr) => {
      
        // TODO: select template, get template file, parse file here

        // setMadeProduct(true);

        // var templateHTML = parsedTemplate.querySelector("html");
        // document.querySelector(".templateBodyHidden").appendChild(templateHTML);
        // let htmlString = document.querySelector(".templateBodyHidden").innerHTML;

        // setMadeProduct(false);

        // let newTemplate = new File([htmlString], htmlArr[0].name, {type: "text/html", lastModified: new Date(0)});
        // uploadFile(newTemplate);
    }

    const uploadFile = (file) => {
      const data = new FormData();
      data.append("template_file", file);

      fetch(`/products/${company_id}`, {
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
      fetch(`/product/${company_id}/${productID}`, {
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

    const DisplayHidden = () => {
      return (
        <div className='templateBodyHidden' style={{display: 'none'}}>
        </div>
      )
    }

    const DisplayTemplate = async (template) => {
        setLoading(true);

        let selectedTemplate;

        await fetch(`/template/${userData.company_company_id}/${template}`, {
            method: 'GET'
        }).then(
            res => res.text()
          ).then(
            data => {
                setLoading(false);
                selectedTemplate = data;
            }
        )

        let html = await readFile(selectedTemplate);

        return (
            <>
                <div className='selectedTemplateBody'>
                </div>
            </>
        )

    }

    const DisplayProducts = () => {
        return (
          <div className="TemplatesBody">
            <ul className="TemplateList">
                {
                    products.map((product) => 
                        <div className="TemplateComp"  key={product.product_id}>
                            <h2 className="TitleCard">Product {product.product_id}</h2>
                            <div className="TemplateCard">
                                <p className="CardIcon View" onClick={() => navigate(`/product/${company_id}/${product.product_id}`)}><FaRegEye /></p>
                                <p className="CardIcon Delete" onClick={() => deleteProduct(product.product_id)}><FaRegTrashAlt /></p>
                            </div>
                        </div>
                    )
                }
                <div className="NewTempBox">
                    <FaPlusCircle className="NewTempButton" onClick={() => setSelectTemplate(true)}/>
                </div>
            </ul>
            { madeProduct ? DisplayHidden() : null }
          </div>
        )
    }

    const DisplayElement = () => {
        return (
            <>
                { selectTemplate && templateId === null ? <SelectTemplate setTemplateId={setTemplateId} setSelectTemplate={setSelectTemplate} setSelectTemplate={setSelectTemplate} /> : templateId !== null ? DisplayTemplate(templateId) : DisplayProducts() }
            </>
        )
    }

    return (
        <>
            { loading ? DisplayLoader() : DisplayElement() }
        </>
    );
};

export default Products
