import React from "react";
import ComponentStyle from "../scss/AddContent.scss";
import Modal from "./Modal.jsx";

const AddUsergroup = props => {
  const addUsergroup = e => {
    e.preventDefault();
    fetch(
      props.that.state.siteUrl +
        `/api/?query=mutation{createUsergroup(name: "${
          document.getElementById("addUsergroupForm")[0].value
        }", description: "${
          document.getElementById("addUsergroupForm")[1].value
        }", access_token: "${props.that.state.token}")}`,
      { method: "POST" }
    )
      .then(
        response => response.json() // if the response is a JSON object
      )
      .then(
        success => {
          alert("success");
          if (props.action) props.action();
        } // Handle the success response object
      )
      .catch(
        error => console.error(error) // Handle the error response object
      );
  };

  return (
    <div>
      <Modal name="Stwórz nowę grupę">
        <h5>Stwórz nową grupę</h5>
        <div>
          <form
            id="addUsergroupForm"
            className={ComponentStyle.form}
            onSubmit={addUsergroup}
          >
            <label htmlFor="groupName">Nazwa grupy</label>
            <br />
            <input required name="title" type="text" id="groupName" />
            <br />
            <label htmlFor="description">Opis grupy</label>
            <br />
            <input required name="title" type="text" id="description" />
            <br />
            <input type="submit" className="btn" value="Dodaj" />
          </form>
        </div>
      </Modal>
    </div>
  );
};

export default AddUsergroup;
