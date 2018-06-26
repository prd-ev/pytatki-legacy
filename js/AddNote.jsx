import React from "react";

class AddNote extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      current_topics: [],
      subject: null
    };
  }

  handleSubmit = e => {
    let updated_notes = this.props.notatki;
    let topic_notes_list = [];
    for (let value of updated_notes) {
      if (
        document.getElementById("subject").value ===
        value.substring(value.indexOf("/") + 1, value.indexOf("/", 1))
      ) {
        if (
          document.getElementById("topic").value ===
          value.substring(value.indexOf("/", 1) + 1, value.lastIndexOf("/"))
        ) {
          topic_notes_list.push(value.substring(value.lastIndexOf("/") + 1));
        }
      }
    }

    if (!topic_notes_list.includes(document.getElementById("note").value)) {
      updated_notes = [
        ...updated_notes,

        "/" +
          document.getElementById("subject").value +
          "/" +
          document.getElementById("topic").value +
          "/" +
          document.getElementById("note").value
      ];
    }
    e.preventDefault();
    this.props.update(updated_notes);
  };

  packNotes = () => {
    let notatki = [];
    for (let value of this.props.notatki) {
      notatki.push(
        <h3 key={value.substring(value.lastIndexOf("/") + 1)}>
          {value.substring(value.lastIndexOf("/") + 1)}
        </h3>
      );
    }
    return notatki;
  };

  packTopicOptions = () => {
    let topic_options_temp = [];
    let topic_options = [];
    for (let temp_value of this.props.notatki) {
      if (
        topic_options_temp.indexOf(
          temp_value.substring(
            temp_value.indexOf("/", 1) + 1,
            temp_value.lastIndexOf("/")
          )
        ) < 0 &&
        document.getElementById("subject").value ==
          temp_value.substring(
            temp_value.indexOf("/") + 1,
            temp_value.indexOf("/", 1)
          )
      ) {
        topic_options_temp.push(
          temp_value.substring(
            temp_value.indexOf("/", 1) + 1,
            temp_value.lastIndexOf("/")
          )
        );
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
  };

  packSubjectOptions = () => {
    let subject_options_temp = [];
    let subject_options = [];
    for (let temp_value of this.props.notatki) {
      if (
        subject_options_temp.indexOf(
          temp_value.substring(
            temp_value.indexOf("/") + 1,
            temp_value.indexOf("/", 1)
          )
        ) < 0
      ) {
        subject_options_temp.push(
          temp_value.substring(
            temp_value.indexOf("/") + 1,
            temp_value.indexOf("/", 1)
          )
        );
      }
    }
    for (let value of subject_options_temp) {
      subject_options.push(<option key={value}>{value}</option>);
    }
    return subject_options;
  };

  componentDidMount() {
    this.packTopicOptions();
  }

  subjectChange = () => {
    this.packTopicOptions();
  };

  render() {
    return (
      <div style={{marginTop: "100px"}}>
        <form onSubmit={this.handleSubmit}>
          Przedmiot
          <select id="subject" onChange={this.subjectChange}>
            {this.packSubjectOptions()}
          </select>
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
