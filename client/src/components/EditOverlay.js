import React, { Component } from 'react'

export class EditOverlay extends Component {
    constructor(props) {
        super(props);

        this.state = {
            text: props.el.textContent,
            editable: true
        }
    }
    render() {
        const handleTextElChange = (e) => {
            this.state.text = e.target.value;
        }

        return (
            // is statement for displaying \/ else return null to return empty div for template.js
            <div className='editOverlay'>
                <div className='editBox'>
                    <form>
                        <input value={this.state.text} type="text" onChange={handleTextElChange}/>
                    </form>
                </div>
            </div>
        )
    }
}

export default EditOverlay
