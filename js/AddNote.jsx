import React from "react";

function uploadNote(e) {
  e.preventDefault();
  const form = document.getElementById('form');
  const files = form[1];
  var formData = new FormData(files);
  fetch('http://127.0.0.1:5000/add/', {
    method: 'POST',
    headers: {
      "Content-Type": "multipart/form-data"
    },
    body: formData
  }).then(
    response => response.text() // if the response is a JSON object
  ).then(
    success => console.log(success) // Handle the success response object
  ).catch(
    error => console.log(error) // Handle the error response object
  );
}

const AddNote = () => {
  return (
    <form id="form" onSubmit={uploadNote}>
      <span>Dodaj notatkę w aktualnym folderze</span>
      <input type="text" name="title"></input>
      <input id="file" type="file" name="file"></input>
      <input type="submit"></input>
    </form>
  )
};


export default AddNote;
