import React from 'react';
import ReactDOM from 'react-dom';
import { Link, withRouter } from "react-router-dom";
import Reflux from 'reflux';

import AuthStore from './../../stores/AuthStore';
import AuthActions from './../../actions/AuthActions';

import './common.css';

class RegistationForm extends Reflux.Component {

  constructor(props) {
    super(props);
    this.store = AuthStore;
  }

  componentWillUpdate(nextProps, nextState) {
    var isAuthenticated = nextState['isAuthenticated'];
    console.log("reg auth status", isAuthenticated);
    if (isAuthenticated) {
      this.props.history.push("secret");
    }
  }

  _handleSubmit(event) {
    event.preventDefault();

    var registrationObject = {
      "first_name": ReactDOM.findDOMNode(this.refs.fname).value,
      "last_name": ReactDOM.findDOMNode(this.refs.lname).value,
      "company": ReactDOM.findDOMNode(this.refs.organization).value,
      "occupation": ReactDOM.findDOMNode(this.refs.position).value,
      "email": ReactDOM.findDOMNode(this.refs.email).value,
      "password1": ReactDOM.findDOMNode(this.refs.password1).value,
      "password2": ReactDOM.findDOMNode(this.refs.password2).value
    };

    console.log("reg", registrationObject);

    AuthActions.registration(registrationObject);
  }

  render() {
    var errorMessage = "";
    if (this.state.error) {
      errorMessage = (
        <div className='alert alert-danger padding-bottom alert-dismissible fade show' role="alert">
          <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
          { this.state.error }
        </div>
      );
    }


    return (
      <form className="login-form col-12 col-sm-12 col-md-6 offset-md-3">

        { errorMessage }

        <div className="form-group form-row">
          <div className="col">
            <label htmlFor="inputFname">First name</label>
            <input type="text" ref="fname" className="form-control" id="inputFname" placeholder="First name" value="Georgy" readOnly />
          </div>
          <div className="col">
            <label htmlFor="inputLname">Last name</label>
            <input type="text" ref="lname" className="form-control" id="inputLname" placeholder="Last Name" value="Marrero" readOnly />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="inputOrganization">Organization</label>
          <input type="text" ref="organization" className="form-control" id="inputOrganization" placeholder="Current organization" value="DataAgora" readOnly />
        </div>

        <div className="form-group">
          <label htmlFor="inputPosition">Position</label>
          <input type="text" ref="position" className="form-control" id="inputPosition" placeholder="Current position" value="ML Engineer" readOnly />
        </div>

        <div className="form-group">
          <label htmlFor="inputEmail">Email address</label>
          <input type="email" ref="email" className="form-control" id="inputEmail" placeholder="Email address" value="geoxx@gmail.com" readOnly />
        </div>

        <div className="form-group">
          <label htmlFor="inputPassword1">Password</label>
          <input type="password" ref="password1" className="form-control" id="inputPassword1" placeholder="Enter password" value="SomePass123" readOnly />
        </div>

        <div className="form-group">
          <label htmlFor="inputPassword2">Repeat password</label>
          <input type="password" ref="password2" className="form-control" id="inputPassword2" placeholder="Repeat password" value="SomePass123" readOnly />
        </div>

        <div className="form-group text-center">
          <button type="submit" onClick={this._handleSubmit.bind(this)} className="btn btn-transparent">Register</button>
        </div>

        <div className="form-group text-center">
          Already a user? <Link to="signin" className="form-link" href="#">Sign in!</Link>
        </div>
      </form>

    );
  }
}

export default withRouter(RegistationForm);
