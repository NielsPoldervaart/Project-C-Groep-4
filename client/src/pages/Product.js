import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import Loader from '../components/Loader';
import EditOverlay from '../components/EditOverlay';
import ReadFile from '../components/ReadFile';
import '../style/Product.css';

const Product = () => {
    // URL Paramaters
    const { company_id, product_id } = useParams();

    // State variables
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

    // Edits the products after the fetch is complete
    const editProduct = (data) => {
        let parser = new DOMParser();
        let parsedProduct = parser.parseFromString(data, "text/html");
        let productHTML = parsedProduct.querySelector("html");
        document.querySelector(".hiddenProduct").appendChild(productHTML);
        
        // Gets the name of the template by getting the first class of the div inside the querySelector
        let templateName = document.querySelector(".hiddenProduct html body div").className.split(" ")[0];

        // Gets all children elements inside the template
        let children = document.querySelector(`.${templateName}`).children;
        for (var i = 0; i < children.length; i++) {
            var child = children[i];
  
            // Removed the templateText and templateImage classes from the child elements
            if (child.classList.contains("templateText")) {
                child.classList.remove("templateText");
            }
            else if (child.classList.contains("templateImage")) {
                child.classList.remove("templateImage");
            }
        }

        // Removes Loader from screen and appends the html of the template to the page
        setLoading(false);
        document.querySelector(".productBody").appendChild(productHTML);

        // EventListener to see if a editable element has been clicked
        document.querySelector(".productBody").addEventListener('click', (e) => {
            if (e.target.classList.contains("editableTxt")) {
                // Sets state values to the e.target values
                setElementText(e.target.innerText);
                setIsTextOverlay(true);
                setElement(e.target);

                // Displays the edit overlay
                showOverlay();
            }
            else if (e.target.classList.contains("editableImg")) {
                // Sets state values to the e.target values
                setElementText(e.target.innerText);
                setIsTextOverlay(false);
                setElement(e.target);

                // Displays the edit overlay
                showOverlay();
            }
        });
    }

    // Sets the setOverlay state to the opposite of the current boolean value
    const showOverlay = () => {
        setOverlay(prev => !prev);
    }

    // Edits the element with the values set inside the <EditOverlay /> component
    const editElement = async (el, value, isText) => {
        if (isText === true) {
            let className = el.className.split(" ")[0];
            var element = document.getElementsByClassName(className)[0];
            element.textContent = value;
        }
        else {
            let className = el.className.split(" ")[0];
            var element = document.getElementsByClassName(className)[0];

            let dataUrl = await ReadFile(value);
            element.style.backgroundImage = `url(${dataUrl})`;
        }
    }

    // Calls the <EditOverlay /> component with all the props required
    // In this case the props are State values, Function references or a string
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

    // Displays the <Loader /> component while setLoading === true
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

    // Uploads the edited file to the FTP server
    const uploadEdit = (e, userData) => {
        e.preventDefault();

        // Creates htmlString from the elements inside ".productBody"
        let htmlString = document.querySelector(".productBody").innerHTML;
        let productName = document.querySelector(".productBody html body div").className.split(" ")[0];

        // Creates new file with the html code
        let updatedProduct = new File([htmlString], `${productName}.html`, {type: "text/html", lastModified: new Date(0)});

        // Creates a FormData object with the key "updated_product" and the value updatedProduct
        const data = new FormData();
        data.append("updated_product", updatedProduct);

        // Creates the POST request to the backend
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