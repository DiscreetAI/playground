import React from 'react';
import { render } from 'react-dom'
import { BrowserRouter } from 'react-router-dom';
import App from './components/app';
import InitializeActions from './actions/initializeActions';
import registerServiceWorker from './utils/registerServiceWorker';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';

import { library } from '@fortawesome/fontawesome-svg-core'
import { faSignOutAlt, faPlus } from '@fortawesome/free-solid-svg-icons'

library.add(faPlus, faSignOutAlt);

InitializeActions.initApp();
render((
  <BrowserRouter>
      <App />
  </BrowserRouter>
), document.getElementById('app'));
registerServiceWorker();
