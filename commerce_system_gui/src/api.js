// put here api calls.
const axios = require("axios");
const urljoin = require('url-join');

const host = "127.0.0.1"
const port = 5000

const host_port = `${host}:${port}`

const routes = {
  base: "api",  // this route is a prefix for any other route
  enter: "enter",
  exit: "exit",
  register: "register",
  login: "login",
  logout: "logout",
  shops: "shops",
  search: "search",
  cart: "cart",
  transactions: "transactions",
  system: "system",
}

const base_route = `${host_port}/${routes.base}`;

export const enter = () => {
  const url = "http://127.0.0.1:5000/api/enter";
  return axios({
    method: "post",
    url: url,
  }).then((res) => {
    const token = res.data;
    // alert(token);
    // alert(token.toString());
    return token;
  }).catch((err) => alert(`failed to enter the system due to ${err}`))

}

export const login = (token, username, password) => {
  // const url = `${base_route}/${routes.login}`;
  const url = "http://127.0.0.1:5000/api/login";
  alert(url);
  return axios({
    method: "post",
    url: url,
    data: {
      token: token,
      username: username,
      password: password,
    }
  })
}

export const logout = (token) => {
  // const url = `${base_route}/${routes.login}`;
  const url = "http://127.0.0.1:5000/api/logout";
  alert(url);
  return axios({
    method: "put",
    url: url,
    data: {
      token: token,
    }
  }).then((res) => res.data).catch((err) => alert(err))
}

export const get_user_transactions = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${routes.transactions}`,
      data: {
        token: token
      }
    });


export const get_shop_transactions = (token, shop_id) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.transactions)}`,
      data: {
        token: token
      }
    });

export const get_system_transactions = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.system, routes.transactions)}`,
      data: {
        token: token
      }
    });