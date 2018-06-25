import React from "react";

class AddNote extends React.Component {
  constructor(props) {
    super(props);
  }

  handleSubmit = e => {
    for (let value of this.props.notatki) {
      if (document.getElementById("subject").value === value["subject"]) {
        if (value["topic"] === document.getElementById("topic")) {
          if (value["name"] !== document.getElementById("note")) {
          }
        }
      }
    }
    e.preventDefault();
    this.props.update(updated_notes);
  };

  packNotes = () => {
    let notatki = [];
    for (let value of this.props.notatki) {
      notatki.push(<h3 key={value["subject"]}>{value["subject"]}</h3>);
    }
    return notatki;
  };

  packTopicOptions = () => {
    let topic_options = [];
    for (let value of this.props.notatki) {
      topic_options.push(
        <option key={value["topic"]}>{value["topic"]}</option>
      );
    }
    return topic_options;
  };

  packSubjectOptions = () => {
    let subject_options = [];
    for (let value of this.props.notatki) {
      subject_options.push(
        <option key={value["subject"]}>{value["subject"]}</option>
      );
    }
    return subject_options;
  };

  render() {
    return (
      <div style={{marginTop: "100px"}}>
        <form onSubmit={this.handleSubmit}>
          Przedmiot
          <select id="subject">{this.packSubjectOptions()}</select>
          Dział
          <select id="topic">{this.packTopicOptions()}</select>
          Nazwa notatki <input type="text" id="note" />
          <input type="submit" value="Dodaj notatkę" />
        </form>
        {this.packNotes()}
      </div>
    );
  }
}

export default AddNote;
