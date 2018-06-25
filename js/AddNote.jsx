import React from "react";

class AddNote extends React.Component {
  constructor(props) {
    super(props);
  }

  handleSubmit = e => {
    let updated_notes = this.props.notatki;
    for (let value of updated_notes) {
      if (document.getElementById("subject").value === value["subject"]) {
        if (value["topic"] === document.getElementById("topic").value) {
          if (value["name"] !== document.getElementById("note").value) {
            updated_notes = [
              ...updated_notes,
              {
                name: document.getElementById("note").value,
                dir: "lalala",
                subject: document.getElementById("subject").value,
                topic: document.getElementById("topic").value
              }
            ];
          }
        }
      }
    }
    console.log(updated_notes);
    e.preventDefault();
    this.props.update(updated_notes);
  };

  packNotes = () => {
    let notatki = [];
    for (let value of this.props.notatki) {
      notatki.push(<h3 key={value["name"]}>{value["name"]}</h3>);
    }
    return notatki;
  };

  packTopicOptions = () => {
    let topic_options = [];
    for (let value of this.props.notatki) {
      topic_options.push(
        <option key={value["name"]}>{value["topic"]}</option>
      );
    }
    return topic_options;
  };

  packSubjectOptions = () => {
    let subject_options = [];
    for (let value of this.props.notatki) {
      subject_options.push(
        <option key={value["name"]}>{value["subject"]}</option>
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
