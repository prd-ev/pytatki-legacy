import React from "react";
import PropTypes from "prop-types";

const EditMode = props => {
  return (
    <div>
      <button className="btn" onClick={props.changeMode}>
        {props.isOn ? "Wyjdź z trybu edycji" : "Włącz tryb edycji"}
      </button>
    </div>
  );
};

EditMode.propTypes = {
  changeMode: PropTypes.func
};

export default React.memo(EditMode);
