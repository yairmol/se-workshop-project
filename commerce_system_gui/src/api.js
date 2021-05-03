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
    appointments: "appointments",
    managers:"managers",
    owners:"owners",
    promotions: "promotions"
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
export const get_shop_info = (token, shop_id) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString())}`,
      data: {
        token: token,
      }
    });
export const save_product_to_cart = (token, shop_id, product_id, amount_to_buy) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.cart, shop_id.toString(), product_id.toString())}`,
      data: {
        token: token,
          amount_to_buy : amount_to_buy
      }
    });
export const get_cart_info = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.cart)}`,
      data: {
        token: token,
      }
    });
export const remove_product_from_cart = (token, shop_id, product_id, amount) =>
    axios({
      method: "DELETE",
      url: `${base_route}/${urljoin(routes.cart, shop_id.toString(), product_id.toString())}`,
      data: {
          token: token,
          amount: amount
      }
    });
export const purchase_product = (token, shop_id, product_id, amount, details) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.cart, shop_id.toString(), product_id.toString())}`,
      data: {
          token: token,
          amount : amount,
          details : details

      }
    });
export const purchase_shopping_bag = (token, shop_id, details) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.cart, shop_id.toString())}`,
      data: {
          token: token,
          details : details
      }
    });
export const purchase_cart = (token,details) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.cart)}`,
      data: {
          token: token,
          details: details
      }
    });
export const open_shop = (token, details) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.shop)}`,
      data: {
          token: token,
          details: details
      }
    });
export const get_personal_purchase_history = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.transactions)}`,
      data: {
          token: token,
      }
    });
export const add_product_to_shop = (token, shop_id, info) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.shop, shop_id.toString(), routes.products)}`,
      data: {
          token: token,
          info:info
      }
    });
export const edit_product_info = (token, shop_id, product_id, product_name, description, price, quantity, categories) =>
    axios({
      method: "PUT",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.products, product_id.toString())}`,
      data: {
          token: token,
          product_name : product_name,
          description : description,
          price: price,
          quantity: quantity,
          categories: categories
      }
    });
export const delete_product = (token, shop_id, product_id) =>
    axios({
      method: "DELETE",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.products, product_id.toString())}`,
      data: {
          token: token,
      }
    });
export const appoint_shop_manager = (token, shop_id, username, permissions) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.promotions)}`,
      data: {
          token: token,
          username: username,
          permissions: permissions
      }
    });
export const appoint_shop_owner = (token, shop_id, username) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.owners)}`,
      data: {
          token: token,
          username: username
      }
    });
export const promote_shop_owner = (token, shop_id, username) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.promotions)}`,
      data: {
          token: token,
          username: username
      }
    });
export const edit_manager_permissions = (token, shop_id, username, permissions) =>
    axios({
      method: "PUT",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.managers)}`,
      data: {
          token: token,
          username: username,
          permissions: permissions
      }
    });
export const unappoint_manager = (token, shop_id, username) =>
    axios({
      method: "DELETE",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.managers)}`,
      data: {
          token: token,
          username: username
      }
    });
export const unappoint_shop_owner = (token, shop_id, username) =>
    axios({
      method: "DELETE",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.owners)}`,
      data: {
          token: token,
          username: username
      }
    });
export const get_shop_staff_info = (token, shop_id) =>
    axios({
      method: "GET",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments)}`,
      data: {
          token: token,
      }
    });
export const get_shop_transaction_history = (token, shop_id) =>
    axios({
      method: "GET",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.transactions)}`,
      data: {
          token: token,
      }
    });
export const get_system_transactions = (token) =>
    axios({
      method: "GET",
      url: `${base_route}/${urljoin(routes.system, routes.appointments)}`,
      data: {
          token: token,
      }
    });
// export const server_error = (token) =>
//     axios({
//       method: "GET",
//       url: `${base_route}/${urljoin(routes.system, routes.appointments)}`,
//       data: {
//           token: token,
//       }
//     });