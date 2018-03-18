import React from 'react';
import Reflux from 'reflux';
import { Link } from 'react-router-dom';
import AuthStore from './../../stores/AuthStore';
import logo from './logo.png';

import './loginHeader.css';

class Header extends Reflux.Component {
  constructor(props) {
    super(props);
    this.store = AuthStore;
  }

  render() {
    var rightElement;
    if (this.state.isAuthenticated) {
      rightElement = (
        <ul className="navbar-nav ml-auto">
          <li className="nav-item">
              <Link to="account" className="nav-link" href="#"><b>Account</b></Link>
          </li>
          <li className="nav-item">
              <Link to="signout" className="nav-link" href="#">Log out</Link>
          </li>
        </ul>
      );
    } else {
      rightElement = (
        <ul className="navbar-nav ml-auto">
          <li className="nav-item">
              <Link to="signin" className="nav-link" href="#"><b>Sign In</b></Link>
          </li>
        </ul>
      );
    }

    return (
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark margin-bottom">
        <div className="container-fluid">
          <Link to="/" className="navbar-brand">
            <img src={logo} className="header-logo" alt="logo" />
          </Link>

          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>

          <div id="navbarNav" className="navbar-collapse collapse w-100 order-3 dual-collapse2">
            { rightElement }
          </div>
        </div>
      </nav>
    );
  }
}

export default Header;
