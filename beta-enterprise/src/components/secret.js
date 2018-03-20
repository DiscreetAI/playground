import React, { Component } from 'react';

class Secret extends Component {
  render() {
    window.setTimeout(function(){
        window.location.href = 'https://demo.dataagora.com';
    }, 3000);

    return (
      <div className="jumbotron text-center bg-dark">
        <h2 style={{color: "white"}}>This page is currently under construction.</h2>
        <h3 style={{color: "white"}}> You are being redirected <a href="https://demo.dataagora.com">to our demo.</a></h3>
      </div>
    );
  }
}

export default Secret;
