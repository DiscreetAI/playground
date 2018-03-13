import React from 'react';
import { Switch, Route } from 'react-router-dom';

import PrivateRoute from './utils/PrivateRoute';

import Home from './components/homePage';
import SignIn from './components/signin';
import Secret from './components/secret';
import NotFoundPage from './components/notFoundPage';


var Routes = () => (
  <Switch>
    <Route exact path="/" name="app" component={Home} />
    <Route path="/signin" name="app" component={SignIn} />
    <PrivateRoute name="secret" path="/secret" component={Secret} />
    <Route component={NotFoundPage} />
  </Switch>
);

export default Routes;
