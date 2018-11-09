import React from "react";
import ComponentStyle from "../scss/AddContent.scss";

const AddUsergroup = props => {
  let addUsergroup = e => {
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
        success => alert("success") // Handle the success response object
      )
      .catch(
        error => console.log(error) // Handle the error response object
      );
  };

  return (
    <div>
      <button
        type="button"
        className="btn"
        data-toggle="modal"
        data-target="#createUsergroup"
      >
        Stwórz nową grupę
      </button>
      <div className="modal" tabIndex="-1" role="dialog" id="createUsergroup">
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Stwórz nową grupę</h5>
              <button
                type="button"
                className="close"
                data-dismiss="modal"
                aria-label="Close"
              >
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body">
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
                <input type="submit" value="Dodaj" />
              </form>
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                data-dismiss="modal"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddUsergroup;
