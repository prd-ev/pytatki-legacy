import React from "react";
import data from "../static/notatki.json";
import AddSubject from "./AddSubject.jsx";

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      notatki: data.map(function(subject) {
        return subject.name;
      })
    };
  }

  render() {
    return (
      <div>
        <AddSubject notatki={this.state.notatki} />
      </div>
    );
  }
}

export default Notatki;
