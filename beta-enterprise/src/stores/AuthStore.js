import Reflux from 'reflux';
import AuthActions from './../actions/AuthActions';
import Endpoints from './../constants/endpoints.js';

//var renderTimeout = 250; // set a timeout to simulate async response time

class AuthStore extends Reflux.Store {
  constructor () {
    super();
    this.init();
    this.listenables = AuthActions;
  }

  init () {
    // pull cached token if one exists
    this.state = {
      error: false,
      loading: false,
      key: localStorage.getItem('key'),
      claims: localStorage.getItem('claims'),
      isAuthenticated: this._isAuthenticated()
    };
  }

  onLogin (email, password) {
    this.loading = true;
    this._changed();

    console.log(Endpoints["eauthLogin"]);

    // this.axios.post(
    //   Endpoints["eauthLogin"],
    //   {email: email, password: password}
    // ).then(res => {
    //   console.log('res', res);
    //   AuthActions.login.completed(res);
    // });

    fetch(
      Endpoints["eauthLogin"], {
        method: 'post',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({"email": email, "password": password})
      }
    ).then(res => {
      var data = res.json();
      data.then(data => {
        AuthActions.login.completed(data);
      });
    });
  }

  onLoginCompleted (authResponse) {
    console.log(authResponse);

    if (authResponse && "key" in authResponse) {
      this.state.key = authResponse['key'];
      //this.state.jwt = authResponse.jwt;
      this._getClaims().then(claims => {
        this.state.claims = claims;
        this.state.error = false;
        this.state.isAuthenticated = true;
        localStorage.setItem('key', this.state.key);
      });

      // this.state.error = false;
      // this.state.isAuthenticated = true;
      // localStorage.setItem('key', this.state.key);

    } else {
      this.state.error = 'Username or password invalid.';
    }

    this.state.loading = false;
    this._changed();
  }

  onLogout () {
    // clear it all
    fetch(Endpoints["eauthLogout"],
    {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      credentials: "include"
    }).then(res => {
       this._resetState();
       localStorage.removeItem('key');
       localStorage.removeItem('claims');
       this._changed();
     });
  }

  _isAuthenticated () {
    // helper
    return localStorage.getItem('claims') != null &&
       localStorage.getItem('key') != null;
  }

  _changed () {
    this.trigger(this.state);
  }

  _getClaims() {
    var claims = localStorage.getItem('claims');
    if (!claims) {
      return fetch(Endpoints["eauthUser"],
        {
          method: 'get',
          headers: {'Content-Type':'application/json',
                    'Authorization': 'Token ' + this.state.key},
          credentials: "include"
        }).then(res => {
          res.json().then(data => {
            localStorage.setItem('claims', data);
          });
        });
    } else {
      return new Promise((resolve, reject) => {
        resolve(claims);
      });
    }
  }

  // _parseJwt () {
  //   var jwt = localStorage.getItem('jwt');
  //   if (jwt === null) {
  //     return null;
  //   }
  //   return JSON.parse(atob(jwt.split('.')[1]));
  // }

  _resetState () {
    this.state = {
      error: false,
      loading: false,
      claims: null,
      key: null,
      isAuthenticated: false
    };
  }

}

export default AuthStore;
