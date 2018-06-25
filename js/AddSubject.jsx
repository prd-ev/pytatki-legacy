import React from "react";

class AddSubject extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      notatki: this.props.notatki
    };
  }

  handleSubmit = e => {
    this.setState((prevState, props) => ({
      notatki: [...prevState.notatki, document.getElementById("subject").value]
    }));
    e.preventDefault();
  };

  packNotes = () => {
    let notatki = [];
    for (let value of this.state.notatki) {
      notatki.push(<h3>{value}</h3>);
    }
    return notatki;
  };

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          Nazwa działu <input type="text" id="subject" />
          <input type="submit" value="Dodaj dział" />
        </form>
        {this.packNotes()}
      </div>
    );
  }
}

export default AddSubject;
