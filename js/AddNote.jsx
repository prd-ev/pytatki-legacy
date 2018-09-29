import React from "react";

function uploadNote(e) {
  e.preventDefault();
  let file = document.getElementById('file').files[0];
  fetch('http://127.0.0.1:5000/notatki', {
    method: 'POST',
    headers: {
      "Content-Type": "You will perhaps need to define a content-type here"
    },
    body: file // This is your file object
  }).then(
    response => response.json() // if the response is a JSON object
  ).then(
    success => console.log(success) // Handle the success response object
  ).catch(
    error => console.log(error) // Handle the error response object
  );
}

const AddNote = () => {
  return (
    <form onSubmit={uploadNote}>
      <input type="text"></input>
      <input id="file" type="file"></input>
      <input type="submit"></input>
    </form>
  )
};


export default AddNote;
