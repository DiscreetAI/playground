import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Home extends Component {
  render() {
    return (
      <div className="jumbotron text-center">
        <h1>DataAgora</h1>
        <p>The first smart data exchange.</p>
        <Link to="signin" className="btn btn-primary">Sign in</Link>
      </div>
    );
  }
}

export default Home;
