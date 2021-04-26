// put here api calls.
const axios = require("axios");
const urljoin = require('url-join');

const host = "localhost"
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
  system: "system"
}

const base_route = urljoin(host_port, routes.base);

const get_user_transactions = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${routes.transactions}`,
      data: {
        token: token
      }
    })


const get_shop_transactions = (token, shop_id) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.transactions)}`,
      data: {
        token: token
      }
    })

const get_system_transactions = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.system, routes.transactions)}`,
      data: {
        token: token
      }
    })