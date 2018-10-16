import React from 'react'
import ComponentStyle from '../scss/EditMode.scss'

const EditMode = (props) => {
    if (props.isOn) {
        return (
            <div>
                <button className={ComponentStyle.btn} onClick={props.changeMode}>Wyjdź z trybu edycji</button>
            </div>
        )

    }
    return (
        <div>
            <button className={ComponentStyle.btn} onClick={props.changeMode}>Włącz tryb edycji</button>
        </div>
    )
}
export default EditMode;