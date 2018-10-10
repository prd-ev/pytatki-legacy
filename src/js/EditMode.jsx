import React from 'react'

const EditMode = (props) => {
    if (props.isOn) {
        return (
            <div>
                <button onClick={props.changeMode}>Wyjdź z trybu edycji</button>
            </div>
        )

    }
    return (
        <div>
            <button onClick={props.changeMode}>Włącz tryb edycji</button>
        </div>
    )
}
export default EditMode;