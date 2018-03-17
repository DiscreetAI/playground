import Reflux from 'reflux';
import cookie from 'react-cookies';
import AuthActions from './../actions/AuthActions';
import Endpoints from './../constants/endpoints.js';

class AuthStore extends Reflux.Store {
  constructor () {
    super();
    this.init();
    this.listenables = AuthActions;
  }

  init () {
    if (!this._isAuthenticated()) {
      this._resetState();
    } else {
      // pull cached token if one exists
      this.state = {
        error: false,
        loading: false,
        jwt: this._getJWT(),
        // claims: this._getClaims(),
        isAuthenticated: true
      };
    }
  }

  onLogin (email, password) {
    this._resetState();
    this.loading = true;
    this._changed();

    var endpoint = Endpoints["eauthLogin"];
    console.log(endpoint);

    fetch(
      endpoint, {
        method: 'POST',
        headers: {
          'Content-Type':'application/json',
          'Accept': 'application/json',
          //'Cache': 'no-cache'
        },
        body: JSON.stringify({"email": email, "password": password}),
        //credentials: "include"
      }
    ).then(response => {
      this._handleLoginRegistrationResponse(response, AuthActions.login);
    });
  }

  onLoginCompleted (jwt) {
    this.state.jwt = jwt;
    localStorage.setItem('jwt', jwt);
    this.state.error = false;
    this.state.isAuthenticated = true;
    this.state.loading = false;
    this._deleteCookies();
    this._changed();
    console.log("claims are", this._getClaims());
  }

  onLoginFailed (errorMessage) {
    console.log("Login failed...", errorMessage);
    this._resetState();
    this.state.error = errorMessage;
    this._changed();
  }

  onRegistration (registrationObject) {
    this._resetState();
    this.loading = true;
    this._changed();

    console.log(Endpoints["eauthRegistration"]);

    fetch(
      Endpoints["eauthRegistration"], {
        method: 'POST',
        headers: {
          'Content-Type':'application/json',
          'Accept': 'application/json',
          //'Cache': 'no-cache'
        },
        body: JSON.stringify(registrationObject),
        //credentials: "include"
      }
    ).then(response => {
      this._handleLoginRegistrationResponse(response, AuthActions.registration);
    });
  }

  onRegistrationCompleted (jwt) {
    this.state.jwt = jwt;
    localStorage.setItem('jwt', jwt);
    this.state.error = false;
    this.state.isAuthenticated = true;
    this.state.loading = false;
    this._deleteCookies();
    this._changed();
    console.log("claims are", this._getClaims());
  }

  onRegistrationFailed(errorMessage) {
    console.log("Reg failed...", errorMessage);
    this._resetState();
    this.state.error = errorMessage;
    this._changed();
  }

  onLogout () {
    // clear it all
    this._resetState();
    this._changed();

    // fetch(Endpoints["eauthLogout"],
    // {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type':'application/json',
    //     'Authorization': 'JWT ' + this.state.jwt,
    //     'Accept': 'application/json',
    //     //'X-CSRFToken': cookie.load('csrftoken')
    //     //'Cache': 'no-cache'
    //   },
    //   credentials: "include"
    // }).then(res => {
    //    this._resetState();
    //    this._changed();
    //  }).catch(error => {
    //    // Note: On error we shouldn't log the user out (maybe).
    //    // This is because their session will still be active on the server.
    //
    //    // Should probably send this error to a top pane alert module. (Future work.)
    //    // this.state.error = "An error occurred during logout. Please try again later. " +
    //    //    "If you want to force the logout, please ";
    //
    //    // HOWEVER, we will be logging them out because we don't have the module
    //    // referenced above.
    //    this._resetState();
    //    this._changed();
    //  });
  }

  _handleLoginRegistrationResponse(response, refluxAction) {
    response.json().then(serverResponse => {
      console.log(serverResponse);
      if (serverResponse && "token" in serverResponse) {
        var jwt = serverResponse['token'];
        refluxAction.completed(jwt);
        // this._getClaimsPromise(jwt).then(claims => {
        //   //claimsPromise.then(claims => {
        //     console.log('claims returned are:', claims);
        //     // Check if this worked or not.
        //     if ("error" in claims && claims["error"] == false) {
        //       refluxAction.completed(jwt, claims['claims']);
        //     } else {
        //       refluxAction.failed(claims["error"]);
        //     }
        //   //});
        // });
      } else {
        // use error returned by server?
        refluxAction.failed(JSON.stringify(serverResponse));
      }
    });
  }

  _isAuthenticated () {
    return this._getJWT();
    //return this._getClaims() && this._getJWT();
  }

  _getClaims() {
    var jwt = this._getJWT();
    if (jwt === null) {
      return null;
    }
    return JSON.parse(atob(jwt.split('.')[1]));
  }

  _getJWT() {
    var jwt = localStorage.getItem("jwt");
    if (!jwt) {
      return null;
    }
    return jwt;
  }

  _changed () {
    this.trigger(this.state);
  }

  // _getClaims() {
  //   var claims = localStorage.getItem("claims");
  //   if (!claims) {
  //     return {};
  //   }
  //   return JSON.parse(claims);
  // }

  // _getClaimsPromise(jwt) {
  //   console.log('all cookies is', cookie.loadAll());
  //   console.log('csrf token is', cookie.load('csrftoken'));
  //   return fetch(Endpoints["eauthUser"],
  //     {
  //       method: 'GET',
  //       headers: {
  //         'Content-Type':'application/json',
  //         'Authorization': 'JWT ' + jwt,
  //         'Accept': 'application/json',
  //         'X-CSRFToken': cookie.load('csrftoken'),
  //         //'Cache': 'no-cache'
  //       },
  //       credentials: "include"
  //     }).then(res => {
  //       console.log("claims promise worked :)");
  //       return res.json().then(data => {
  //         return Promise.resolve({"claims": data, "error": false});
  //       }).catch(error => {
  //         return Promise.resolve({"claims": error, "error": true});
  //       });
  //     }).catch(error => {
  //       console.log("error during claims promise", error);
  //       //return Promise.resolve({"claims": "fake", "error": null});
  //       //return Promise.resolve().then(() => {
  //         return Promise.resolve({"error": "An error occurred. Please try again later."});
  //       //})
  //     });
  // }

  _resetState () {
    this.state = {
      error: false,
      loading: false,
      // claims: null,
      jwt: null,
      isAuthenticated: false
    };

    localStorage.removeItem('jwt');
    //localStorage.removeItem('claims');

    this._deleteCookies();
  }

  _deleteCookies() {
    cookie.remove('csrftoken', { path: '/' });
    cookie.remove('sessionid', { path: '/' });
  }

}

export default AuthStore;
