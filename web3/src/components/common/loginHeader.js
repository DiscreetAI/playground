import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import logo from './logo.png';

import './loginHeader.css';

class Header extends Component {
  render() {
    return (
      <nav className="navbar navbar-expand-lg navbar-light bg-light pad-bottom">
        <div className="container-fluid">
          <Link to="/" className="navbar-brand">
            <img src={logo} className="App-logo" alt="logo" />
          </Link>

          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>

          <div id="navbarNav" className="navbar-collapse collapse w-100 order-3 dual-collapse2">
            <ul className="navbar-nav ml-auto">
                <li className="nav-item">
                    <Link to="signin" className="nav-link" href="#">Sign In</Link>
                </li>
            </ul>
        </div>
        </div>
      </nav>
    );
  }
}


// <div className="collapse navbar-collapse" id="navbarNav">
//   <ul className="navbar-nav mr-auto mt-2 mt-lg-0 d-none">
//
//     <li className="nav-item active">
//       <Link to="app" className="nav-link">Home</Link>
//     </li>
//
//     <li className="nav-item active">
//       <Link to="app" className="nav-link">Something Else</Link>
//     </li>
//   </ul>
//   <div className="my-2 my-lg-10">
//     <Link to="login">Login</Link>
//   </div>
// </div>

// <ul className="nav navbar-nav">
//   <li><Link to="app">Home</Link></li>
//   <li><Link to="login">Login</Link></li>
// </ul>
// <nav className="navbar navbar-default">
//   <div className="container-fluid">
//     <Link to="app" className="navbar-brand">
//       <img src={logo} className="App-logo" alt="logo" />
//     </Link>
//     <ul className="nav navbar-nav">
//       <li><Link to="app">Home</Link></li>
//       <li><Link to="login">Login</Link></li>
//     </ul>
//   </div>
// </nav>

export default Header;
