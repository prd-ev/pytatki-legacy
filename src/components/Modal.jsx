import React from "react";
import style from "../scss/Modal.scss";

export default class Modal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      visible: this.props.no_button ? true : false
    };
    this.close = this.close.bind(this);
    this.escDetection = this.escDetection.bind(this);
    document.addEventListener("keydown", this.escDetection, false);
  }

  componentWillUnmount() {
    document.removeEventListener("keydown", this.escDetection, false);
  }

  escDetection(e) {
    if (e.keyCode === 27) {
      this.close();
    }
  }

  close(e) {
    if (this.props.close_action) this.props.close_action();
    this.setState({
      visible: false
    });
  }

  button() {
    if (this.props.no_button) {
      return "";
    }
    return (
      <button
        type="button"
        onClick={() => {
          if (!this.state.visible) {
            if (this.props.action) this.props.action();
            this.setState({ visible: true });
          }
        }}
        className="btn"
      >
        {this.props.name}
      </button>
    );
  }

  render() {
    return (
      <React.Fragment>
        {this.button()}
        {this.state.visible ? (
          <div
            className={style.modal_view}
            onClick={e => {
              e.cancelBubble = true;
              if (e.stopPropagation) e.stopPropagation();
              this.close(e);
            }}
          >
            <div
              className={style.modal}
              onClick={e => {
                e.cancelBubble = true;
                if (e.stopPropagation) e.stopPropagation();
              }}
            >
              <a className={style.close} onClick={this.close}>
                <i className="fas fa-times" />
              </a>
              {this.props.children}
            </div>
          </div>
        ) : null}
      </React.Fragment>
    );
  }
}
