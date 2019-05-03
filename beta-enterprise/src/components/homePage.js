import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Home extends Component {
  render() {
    return (
      <div className="jumbotron text-center bg-dark">
        <h1>DataAgora</h1>
        <h4>The first smart data exchange.</h4>
        <div className="margin-top-sm">
          <Link to="dashboard" className="btn btn-lg btn-transparent">Access Beta</Link>
        </div>
      </div>
    );
  }
}

export default Home;
