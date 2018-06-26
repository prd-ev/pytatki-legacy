import React from "react";
import data from "../static/notatki.json";
import AddNote from "./AddNote.jsx";

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      notatki: data
    };
  }

  updateNotes = updated_notes => {
    this.setState((prevState, props) => ({
      notatki: updated_notes
    }));
  };

  render() {
    return (
      <div>
        <AddNote notatki={this.state.notatki} update={this.updateNotes} />
      </div>
    );
  }
}

export default Notatki;
