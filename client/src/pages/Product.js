import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import Loader from '../components/Loader';
import EditOverlay from '../components/EditOverlay';
import '../style/Product.css';

const Product = () => {
    const { company_id, product_id } = useParams();

    const [loading, setLoading] = useState(true);
    const [overlay, setOverlay] = useState(false);
    const [isTextOverlay, setIsTextOverlay] = useState(null);
    const [elementText, setElementText] = useState("");
    const [elementImage, setElementImage] = useState(null);
    const [element, setElement] = useState(null);

    const [userData, setUserData] = useState({});

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

            fetch(`/product/${userData.company_company_id}/${product_id}`, {
                method: 'GET'
            }).then(
                res => res.text()
              ).then(
                data => {
                  editProduct(data);
                }
            )
        }

        fetchData();
    }, [company_id, product_id]);

    const editProduct = (data) => {
        let parser = new DOMParser();
        let parsedProduct = parser.parseFromString(data, "text/html");
        let productHTML = parsedProduct.querySelector("html");
        document.querySelector(".hiddenProduct").appendChild(productHTML);
        
        let templateName = document.querySelector(".hiddenProduct html body div").className.split(" ")[0];

        let children = document.querySelector(`.${templateName}`).children;
        for (var i = 0; i < children.length; i++) {
            var child = children[i];
  
            if (child.classList.contains("templateText")) {
                child.classList.remove("templateText");
            }
            else if (child.classList.contains("templateImage")) {
                child.classList.remove("templateImage");
            }
        }

        setLoading(false);
        document.querySelector(".productBody").appendChild(productHTML);

        document.querySelector(".productBody").addEventListener('click', (e) => {
            if (e.target.classList.contains("editableTxt")) {
                setElementText(e.target.innerText);
                setIsTextOverlay(true);
                setElement(e.target);

                showOverlay();
            }
            else if (e.target.classList.contains("editableImg")) {
                setElementText(e.target.innerText);
                setIsTextOverlay(false);
                setElement(e.target);

                showOverlay();
            }
        });
    }

    const showOverlay = () => {
        setOverlay(prev => !prev);
    }

    const readFile = async (file) => {
        return new Promise((resolve, reject) => {
            let fr = new FileReader();  

            fr.onload = () => {
                resolve(fr.result)
            };
            fr.onerror = reject;

            fr.readAsDataURL(file);
        });
    }

    const editElement = async (el, value, isText) => {
        if (isText === true) {
            let className = el.className.split(" ")[0];
            var element = document.getElementsByClassName(className)[0];
            element.textContent = value;
        }
        else {
            let className = el.className.split(" ")[0];
            var element = document.getElementsByClassName(className)[0];

            let dataUrl = await readFile(value);

            element.style.backgroundImage = `url(${dataUrl})`;

        }
    }

    const displayOverlay = () => {
        return (
          <EditOverlay 
            userData={userData} 
            elementText={elementText} 
            overlay={overlay} 
            isTextOverlay={isTextOverlay} 
            setOverlay={setOverlay} 
            setElementText={setElementText} 
            element={element} 
            editable={null} 
            setEditable={null} 
            editElement={editElement} 
            editType="product" 
            setElementImage={setElementImage}
            elementImage={elementImage}
          />
        )
    }

    const displayLoader = () => {
        return (
          <>
            <div className='loaderDiv'>
              <Loader />
            </div>
            <div className='hiddenProduct' style={{display: 'none'}}></div>
          </>
        )
    }

    const uploadEdit = (e, userData) => {
        e.preventDefault();

        let htmlString = document.querySelector(".productBody").innerHTML;
        let productName = document.querySelector(".productBody html body div").className.split(" ")[0];
        let updatedProduct = new File([htmlString], `${productName}.html`, {type: "text/html", lastModified: new Date(0)});

        const data = new FormData();
        data.append("updated_product", updatedProduct);

        fetch(`/product/${userData.company_company_id}/${product_id}`, {
            method: 'POST',
            body: data,
        })
        .then(res => {
            res.json();
            window.location.href = `/products/${userData.company_company_id}`;
        })
        .catch(error => console.log('Authorization failed : ' + error.message));
    }

    const displayElement = () => {
        return (
            <>
                <div className='editPage'>
                    <div className="productBody">
                    </div>
                    <div className='editFunctionBtns'>
                        <form onSubmit={(e) => uploadEdit(e)}>
                            <input type="button" value="Annuleren" className='editAnnulerenBtn' onClick={() => window.location.href = `/products/${userData.company_company_id}`}/>
                            <input type="submit" value="Opslaan" className='editOpslaanBtn' onClick={(e) => uploadEdit(e, userData)}/>
                        </form>
                    </div>
                </div>
                { overlay ? displayOverlay() : null }
            </>
        )
    }

    return (
        <>
            { loading ? displayLoader() : displayElement() }
        </>
    )
}

export default Product