import React from "react";

class AddNote extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      current_topics: []
    };
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

  packTopicOptions =()=>{
    let topic_options_temp = [];
    let topic_options = [];
    for (let temp_value of this.props.notatki) {
      if (
        topic_options_temp.indexOf(temp_value["topic"]) < 0 &&
        document.getElementById("subject").value == temp_value["subject"]
      ) {
        topic_options_temp.push(temp_value["topic"]);
      }
    }
    for (let value of topic_options_temp) {
      topic_options.push(<option key={value}>{value}</option>);
    }
    if (this.state.current_topics !== topic_options) {
      this.setState({
        current_topics: topic_options
      });
    }
  }

  componentDidMount() {
    this.packTopicOptions()
  }


  packSubjectOptions = () => {
    let subject_options_temp = [];
    let subject_options = [];
    for (let temp_value of this.props.notatki) {
      if (subject_options_temp.indexOf(temp_value["subject"]) < 0) {
        subject_options_temp.push(temp_value["subject"]);
      }
    }
    for (let value of subject_options_temp) {
      subject_options.push(<option key={value}>{value}</option>);
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
          <select id="topic">{this.state.current_topics}</select>
          Nazwa notatki <input type="text" id="note" />
          <input type="submit" value="Dodaj notatkę" />
        </form>
        {this.packNotes()}
      </div>
    );
  }
}

export default AddNote;
