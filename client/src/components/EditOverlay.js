import React, { useEffect, useCallback, useRef } from 'react';
import { MdClose } from 'react-icons/md';
import '../style/EditOverlay.css';

const EditOverlay = ({ elementText, overlay, isTextOverlay, setOverlay, setElementText, element, editable, setEditable, editElement }) => {
    const overlayRef = useRef();

    const closeOverlay = (e) => {
        if (overlayRef.current === e.target) {
            setOverlay(false);
        }
    }

    const keyPress = useCallback(
        e => {
            if (e.key === "Escape" && overlay) {
                setOverlay(false);
            }
        }, [overlay]
    );

    useEffect(() => {
        document.addEventListener('keydown', keyPress);
        return () => document.removeEventListener('keydown', keyPress);
    }, [keyPress]);



    const textOverlay = () => {
        return (
            // Add blur to onchange event? to reduce lag idk https://delgersaikhann.medium.com/react-input-model-lag-181c22043c29
            <>
                {/* <input type="text" value={elementText} onChange={e => setElementText(e.target.value)}/> */}
                <textarea value={elementText} onChange={e => setElementText(e.target.value)} cols="65" rows="10" wrap="hard"/>
            </>
        )
    }

    const imgOverlay = () => {
        return (
            <>
                <h1>image</h1>
            </>
        )
    }

    const callEditElement = (e) => {
        e.preventDefault();

        editElement(element, elementText, isTextOverlay, editable);
        setOverlay(false);
    }

    return (
        <div className='overlayContainer' ref={overlayRef} onClick={closeOverlay}>
            <div className='editBoxContainer'>
                <div className='editBox'>
                    <div className='overlayCloseBtn' onClick={() => setOverlay(false)}><MdClose /></div>
                    <form onSubmit={(e) => callEditElement(e)}>
                        { isTextOverlay ? textOverlay() : imgOverlay() }
                        <div className='overlayCheckboxContainer'>
                            <label for="isEditable">Is te bewerken door een klant:</label>
                            <input className='overlayCheckbox' name="isEditable" type="checkbox" checked={editable} onChange={() => setEditable(prev => !prev)}/>
                        </div>
                        <div className='overlayFormBtns'>
                            <input type="reset" value="Annuleren" className='overlayAnnulerenBtn' onClick={() => setOverlay(false)} />
                            <input type="submit" value="Bewerken" className='overlayBewerkenBtn' />
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default EditOverlay;
