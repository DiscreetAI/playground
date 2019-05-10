// import Reflux from 'reflux';
// // import cookie from 'react-cookies';
// import RepoActions from './../actions/RepoActions';
// import AuthStore from './AuthStore';
// import Endpoints from './../constants/endpoints.js';
//
//
// class RepoStore extends Reflux.Store {
//   constructor () {
//     super();
//     this.init();
//     this.listenables = RepoActions;
//   }
//
//   init () {
//     this.state = {
//       repoWasFound: false,
//       repoData: {},
//       repoStatus: {},
//       repoLogs: [],
//     };
//   }
//
//
//   onGetRepoData() {
//     if (!AuthStore.state.isAuthenticated) {
//       return;
//     }
//
//     let jwt_string = AuthStore.state.jwt;
//     let claims = AuthStore.state.claims;
//
//
//   }
//
//
//   _getClaims() {
//
//   }
//
//
//
//
//
//
//   onLogin (email, password) {
//     this._resetState();
//     this.loading = true;
//     this._changed();
//
//     var endpoint = Endpoints["eauthLogin"];
//     fetch(
//       endpoint, {
//         method: 'POST',
//         headers: {
//           'Content-Type':'application/json',
//           'Accept': 'application/json',
//         },
//         body: JSON.stringify({"email": email, "password": password}),
//       }
//     ).then(response => {
//       this._handleLoginRegistrationResponse(response, AuthActions.login);
//     });
//   }
//
//   onLoginCompleted (jwt) {
//     this.state.jwt = jwt;
//     localStorage.setItem('jwt', jwt);
//     this.state.claims = this._getClaims();
//     this.state.error = false;
//     this.state.isAuthenticated = true;
//     this.state.loading = false;
//     this._deleteCookies();
//     this._changed();
//   }
//
//   onLoginFailed (errorMessage) {
//     this._resetState();
//     this.state.error = errorMessage;
//     this._changed();
//   }
//
//   onRegistration (registrationObject) {
//     this._resetState();
//     this.loading = true;
//     this._changed();
//
//     fetch(
//       Endpoints["eauthRegistration"], {
//         method: 'POST',
//         headers: {
//           'Content-Type':'application/json',
//           'Accept': 'application/json',
//         },
//         body: JSON.stringify(registrationObject),
//       }
//     ).then(response => {
//       this._handleLoginRegistrationResponse(response, AuthActions.registration);
//     });
//   }
//
//   onRegistrationCompleted (jwt) {
//     this.state.jwt = jwt;
//     localStorage.setItem('jwt', jwt);
//     this.state.claims = this._getClaims();
//     this.state.error = false;
//     this.state.isAuthenticated = true;
//     this.state.loading = false;
//     this._deleteCookies();
//     this._changed();
//   }
//
//   onRegistrationFailed(errorMessage) {
//     this._resetState();
//     this.state.error = errorMessage;
//     this._changed();
//   }
//
//
//   _handleLoginRegistrationResponse(response, refluxAction) {
//     response.json().then(serverResponse => {
//       if (serverResponse && "token" in serverResponse) {
//         var jwt = serverResponse['token'];
//         refluxAction.completed(jwt);
//       } else {
//         // TODO: Use error returned by server.
//         refluxAction.failed(JSON.stringify(serverResponse));
//       }
//     });
//   }
//
//
//   _changed () {
//     this.trigger(this.state);
//   }
//
//
// }
//
// export default RepoStore;
