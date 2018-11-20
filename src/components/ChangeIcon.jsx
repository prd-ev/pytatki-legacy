import React from "react";
import style from "../scss/ChangeIcon.scss";

export default function ChangeIcon(props) {
  let changeIcon = folderId => () => {
    let form = document.getElementById("icon-form");
    const icon = form[1].files[0];
    let formData = new FormData();
    formData.append("icon", icon);
    fetch(props.that.state.siteUrl + "/add/icon/" + folderId, {
      method: "POST",
      body: formData
    })
      .then(
        response => response.json() // if the response is a JSON object
      )
      .then(
        success => alert(success.data) // Handle the success response object
      )
      .catch(
        error => console.log(error) // Handle the error response object
      );
    props.that.setState({
      idToChangeIcon: null
    });
    props.that.updateContent();
  };

  if (props.that.state.idToChangeIcon) {
    return (
      <div className={style.addIcon}>
        <p>Udostępnij własną ikonę</p>
        <form
          id="icon-form"
          className={style.form}
          onSubmit={() => changeIcon(props.that.state.idToChangeIcon)}
        >
          <label htmlFor="noteFile">Nowa ikona</label>
          <br />
          <input required type="file" name="file" />
        </form>
        <span onClick={changeIcon(props.that.state.idToChangeIcon)}>Zmień</span>
        <span onClick={() => props.that.setState({ idToChangeIcon: null })}>
          Anuluj
        </span>
      </div>
    );
  } else {
    return null;
  }
}
