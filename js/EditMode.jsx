import React from 'react'

export default (props) => {
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
