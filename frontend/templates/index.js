import React from 'react';
import ReactDOM from 'react-dom';
import './index2.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<App />, document.getElementById('content'));
registerServiceWorker();
