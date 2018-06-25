import React from "react";

class Notatki extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      notatki: {}
    };
  }

  packNotes = () => {
    let notatki = <h3>awdawd</h3>;
    return notatki;
  };

  render() {
    return (
      <div>
        <button onClick={this.addNote}> Dodaj dział </button>
        {this.packNotes()}
      </div>
    );
  }
}

export default Notatki;
