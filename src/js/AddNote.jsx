import React from "react";
import ComponentStyle from '../scss/AddContent.scss';

const AddNote = (props) => {
  return (
    <form id="form" className={ComponentStyle.form} onSubmit={props.uploadNote}>
      <span>Dodaj notatkę w aktualnym folderze </span>
      <input required type="text" name="title"></input>
      <input required id="file" type="file" name="file"></input>
      <input type="submit"></input>
    </form>
  );
};


export default AddNote;
