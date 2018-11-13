import React from "react";
import style from "../scss/Modal.scss";

export default class Modal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      visible: false
    };
  }

  render() {
    return (
      <React.Fragment>
        <button
          type="button"
          onClick={() => {
            if (!this.state.visible) {
              this.props.action();
              this.setState({ visible: true });
            }
          }}
          className="btn bar"
        >
          {this.props.name}
        </button>
        {this.state.visible ? (
          <div className={style.modal}>
            <a
              className={style.close}
              onClick={() =>
                this.setState({
                  visible: false
                })
              }
            >
              <i className="fas fa-times" />
            </a>
            {this.props.children}
          </div>
        ) : null}
      </React.Fragment>
    );
  }
}
