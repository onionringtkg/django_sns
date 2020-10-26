import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

// ルーティングに必要なライブラリのインポート
import {Route, BrowserRouter} from 'react-router-dom';
import Login from './components/Login';
import { CookiesProvider } from 'react-cookie';

// ルーティングを行う
const routing = (
  <React.StrictMode>
    <BrowserRouter>
    {/* CookiesProvider：Cookieの処理が可能な範囲を囲む */}
    <CookiesProvider>

      <Route exact path="/" component={Login} />
      <Route exact path="/profiles" component={App} />

    </CookiesProvider>
    </BrowserRouter>
  </React.StrictMode>
)

ReactDOM.render(
  routing,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
