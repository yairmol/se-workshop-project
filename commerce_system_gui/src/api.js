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
  }).then((res) => res.data)
    .catch((err) => alert(`failed to enter the system due to ${err}`))
}

export const exit = (token) => {
  const url = "http://127.0.0.1:5000/api/exit";
  return axios({
    method: "delete",
    url: url,
    data: {
      token: token
    }
  }).then((res) => {
    return res.data;
  }).catch((err) => alert(`failed to exit the system due to ${err}`))

}

export const register = (token, user_data) => {
  // const url = `${base_route}/${routes.login}`;
  const url = "http://127.0.0.1:5000/api/register";
  alert(url);
  return axios({
    method: "post",
    url: url,
    data: {
      token: token,
      ...user_data
    }
  }).then((res) => res.data.status)
    .catch((err) => alert(err))
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
  }).then((result) => result.data.status)
    .catch((err) => alert(`failed to login due to ${err}`))
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
  }).then((res) => res.data.status).catch((err) => alert(err))
}

export const get_user_transactions = (token) =>
    axios({
      method: "get",
      url: `http://127.0.0.1:5000/api/transactions?token=${token}`,
    }).then((res) => res.data)
        .catch((err) => alert(`can't find user transactions due to ${err}`));


export const get_product_info = (token, shop_id, product_id) => {
  // const url = `${base_route}/${routes.login}`;
  const url = `http://127.0.0.1:5000/api/shops/${shop_id}/products/${product_id}`;
  return axios({
    params: {
      token: token
    },
    method: "get",
    url: url,
  }).then((res) => res.data)
    .catch((err) => alert(err))
}
export const get_permissions = (token, shop_id) =>
{
  const url = `http://127.0.0.1:5000/api/permissions/${shop_id}`;
  return axios({
    params: {
      token: token
    },
    method: "get",
    url: url,
  }).then((res) => res.data)
    .catch((err) => alert(err))
}
export const edit_product = (token, shop_id, product_id, name, price, description, categories) =>
{
  const details = `shop id: ${shop_id} product id: ${product_id} name: ${name} price: ${price} description: ${description} categories: ${categories}`
  alert(details)
  // const url = "http://127.0.0.1:5000/api/edit_product";  // PATH?
  // return axios({
  //   method: "put",
  //   url: url,
  //   data: {
  //     token: token,
  //     shop_id: shop_id,
  //     product_id: product_id,
  //     product_name: name,
  //     price: price,
  //     description: description,
  //     categories: categories
  //   }
  // }).then((result) => result.data.status)
  //   .catch((err) => alert(`failed to edit product info due to ${err}`))
}

export const delete_product = (token, shop_id, product_id) =>
{
  const details = `shop id: ${shop_id} product id: ${product_id} `
  alert(details)
}

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