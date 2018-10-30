import React from 'react';
import PropTypes from 'prop-types'
import ComponentStyle from '../scss/EditMode.scss';

const EditMode = (props) => {
    if (props.isOn) {
        return (
            <div>
                <button className="btn" onClick={props.changeMode}>Wyjdź z trybu edycji</button>
            </div>
        )

    }
    return (
        <div>
            <button className="btn" onClick={props.changeMode}>Włącz tryb edycji</button>
        </div>
    );
};

EditMode.propTypes = {
    changeMode: PropTypes.func
}

export default EditMode;