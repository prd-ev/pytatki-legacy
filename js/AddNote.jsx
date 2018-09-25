import React from "react";

var new_topic_message = "--Dodaj nowy dział--";
var new_subject_message = "--Dodaj nowy przedmiot--";

class AddNote extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      topics: null,
      current_topics: null,
      subject_input: false,
      topic_input: false
    };
  }

  handleSubmit = e => {
    e.preventDefault();
    let updated_notes = this.props.notatki;
    let topic_notes_list = [];

    if (!topic_notes_list.includes(document.getElementById("note").value)) {
      if (document.getElementById("subject").value === new_subject_message &&
        document.getElementById("new-subject") != null &&
        document.getElementById("new-topic") != null) {
        //do new subject-topic-note
      } else if (document.getElementById("topic").value === new_topic_message && document.getElementById("new-topic") != null) {
        //do new topic-note
      } else if (document.getElementById("topic").value === new_topic_message && document.getElementById("new-topic") == null || document.getElementById("subject").value === new_subject_message && document.getElementById("new-subject") == null) {
        //do nothing
        return null;
      } else {
        //do new note
      }
      document.getElementById("note").value = "";
    }
    this.props.update(updated_notes);
  };

  packTopicOptions = () => {
    var xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
      if (xhttp.status === 200) {
        //this.setState({ notes: xhttp.responseText.split(" ") });
        console.log(xhttp.responseText);
      }
      let result = ['Notatka1', 'Notatka2', 'Notatka3'];
      let topic_options = [];
      for (let value of result) {
        topic_options.push(<option key={value}>{value}</option>);
      }
      topic_options.push(<option key={new_topic_message}>{new_topic_message}</option>);
      this.setState({ topics: topic_options });
    }.bind(this);
    xhttp.open('GET', 'http://127.0.0.1:5000/graphql?query={getContent(id_notegroup:1,id_user:1)}');
    xhttp.send();

};

componentDidMount(){
  this.packTopicOptions();
}

packSubjectOptions = () => {
  if (this.props.subjects) {
    let subject_options = [];
    for (let value of this.props.subjects) {
      subject_options.push(<option key={value}>{value}</option>);
    }
    subject_options.push(<option key={new_subject_message}>{new_subject_message}</option>);
    return subject_options;
  }
  return 0;
};


subjectChange = () => {
  this.packTopicOptions();
  if (document.getElementById("subject").value === new_subject_message) {
    this.setState({ subject_input: true, topic_input: true });
  } else {
    this.setState({ subject_input: false, topic_input: false });
  }

};

topicChange = () => {
  if (document.getElementById("topic").value === new_topic_message) {
    this.setState({ topic_input: true });
  } else {
    this.setState({ topic_input: false });
  }
};

newSubjectInput = () => {
  if (this.state.subject_input) {
    return <input type="text" id="new-subject" />;
  }
};

newTopicInput = () => {
  if (this.state.topic_input) {
    return <input type="text" id="new-topic" />;
  }
};

render() {
  return (<div style={{
    marginTop: "100px"
  }}>
    <form onSubmit={this.handleSubmit}>
      Przedmiot
        <select id="subject" onChange={this.subjectChange}>
        {this.packSubjectOptions()}
      </select>
      {this.newSubjectInput()}
      Dział
        <select id="topic" onChange={this.topicChange}>
        {this.state.topics}
      </select>
      {this.newTopicInput()}
      Nazwa notatki
        <input type="text" id="note" />
      Dodaj plik
        <input type="file" required="required" />
      <input type="submit" value="Dodaj notatkę" />
    </form>
  </div>);
}
}

export default AddNote;
