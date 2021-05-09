// put here api calls.
const axios = require("axios");
const urljoin = require('url-join');

const host = "https://127.0.0.1"
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
    user: "user",
    all_shops: "all_shops",
    all_user_names: "all_user_names",
    all_shops_ids_and_names: "all_shops_ids_and_names",
  search: "search",
  cart: "cart",
  transactions: "transactions",
  system: "system",
  appointments: "appointments",
  managers: "managers",
  owners: "owners",
  promotions: "promotions",
  discounts: "discounts",
}

const base_route = `${host_port}/${routes.base}`;

export const isValidToken = (token) => {
  const url = `${base_route}/validate_token`;
  // alert(url)
  return axios({
    method: "get",
    url: url,
    params: {
      token: token
    }
  }).then((res) => res.data.is_valid)
      .catch((err) => alert(`failed to enter the system due to ${err}`))
}

export const enter = () => {
  const url = `${base_route}/enter`;
  // alert(url)
  return axios({
    method: "post",
    url: url,
  }).then((res) => res.data)
      .catch((err) => alert(`failed to enter the system due to ${err}`))
}

export const exit = (token) => {
  const url = `${base_route}/exit`;
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
  const url = `${base_route}/register`;
  return axios({
    method: "post",
    url: url,
    data: {
      token: token,
      ...user_data
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  })
      .catch((err) => alert(err))
}

export const login = (token, username, password) => {
  // const url = `${base_route}/${routes.login}`;
  const url = `${base_route}/login`;

  return axios({
    method: "post",
    url: url,
    data: {
      token: token,
      username: username,
      password: password,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to login due to ${err}`))
}

export const logout = (token) => {
  // const url = `${base_route}/${routes.login}`;
  const url = `${base_route}/logout`;

  return axios({
    method: "put",
    url: url,
    data: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(err))
}

export const get_cart_info = (token) => {
  const url = `${base_route}/cart`;
  return axios({
    url: url,
    method: "get",
    params: {
      token: token
    },
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get cart info due to ${err}`))
}

export const save_product_to_cart = (token, shop_id, product_id, amount_to_buy) => {
  const url = `${base_route}/cart/${shop_id}/${product_id}`;
  return axios({
    url: url,
    method: "post",
    data: {
      token: token,
      amount_to_buy: amount_to_buy
    },
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get cart info due to ${err}`))
}

export const remove_product_from_cart = (token, shop_id, product_id, amount) => {
  const url = `${base_route}/cart/${shop_id}/${product_id}`;
  return axios({
    url: url,
    method: "delete",
    data: {
      token: token,
      amount: amount,
    },
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to remove from cart info due to ${err}`))
}

export const get_user_transactions = (token) =>
    axios({
      method: "get",
      url: `${base_route}/transactions?token=${token}`,
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`can't find user transactions due to ${err}`));



export const get_product_info = (token, shop_id, product_id) => {
  // const url = `${base_route}/${routes.login}`;
  const url = `http://127.0.0.1:5000/api/shops/${shop_id}/products/${product_id}`;
  return axios({
    params: {
      token: token
    },
    method: "get",
    url: url,
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(err))
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
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(err))
}
export const edit_product = (token, shop_id, product_id, name, price, description, categories) =>
{
  const details = `shop id: ${shop_id} product id: ${product_id} name: ${name} price: ${price} description: ${description} categories: ${categories}`
  alert(details)
  const url = `http://127.0.0.1:5000/api/shops/${shop_id}/products/${product_id}`;
  return axios({
    method: "put",
    url: url,
    data: {
      token: token,
      product_name: name,
      price: price,
      description: description,
      categories: categories
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to edit product info due to ${err}`))
}

// export const delete_product = (token, shop_id, product_id) =>
// {
//   const details = `shop id: ${shop_id} product id: ${product_id} `
//   alert(details)
// }

export const get_shop_transactions = (token, shop_id) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.transactions)}`,
      data: {
        token: token
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shop transactions due to ${err}`));

export const get_system_transactions = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.system, routes.transactions)}`,
      data: {
        token: token
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get system transactions due to ${err}`));

export const get_system_transactions_of_shops = (token, shop_id) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.system, routes.transactions, routes.shops)}`,
      data: {
        token: token,
          shop_id: shop_id
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get system transactions of shop due to ${err}`));;

export const get_system_transactions_of_user = (token, username) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.system, routes.transactions, routes.user)}`,
      data: {
        token: token,
          username: username
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get system transactions of user due to ${err}`));;


export const get_shop_info = (token, shop_id) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString())}`,
      data: {
        token: token,
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shop info due to ${err}`));

export const get_all_shops_info = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.all_shops)}`,
      data: {
        token: token,
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  })
        .catch((err) => alert(`failed to get all shops info due to ${err}`))

export const get_all_shops_ids_and_names = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.all_shops_ids_and_names)}`,
      data: {
        token: token,
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shops ids and names due to ${err}`));



export const get_all_user_names = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.all_user_names)}`,
      data: {
        token: token,
      }
    }).then((res) => res.data)

export const purchase_product = (token, shop_id, product_id, amount, details) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.cart, shop_id.toString(), product_id.toString())}`,
      data: {
          token: token,
          amount : amount,
          details : details

      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to purchase product due to ${err}`));

export const purchase_shopping_bag = (token, shop_id, details) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.cart, shop_id.toString())}`,
      data: {
          token: token,
          details : details
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to purchase shopping bag due to ${err}`));

export const purchase_cart = (token,details) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.cart)}`,
      data: {
          token: token,
          details: details
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to purchase cart due to ${err}`));

export const open_shop = (token, details) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.shop)}`,
      data: {
          token: token,
          details: details
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result // @todo: need to return shop id?
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to open shop due to ${err}`));

export const get_personal_purchase_history = (token) =>
    axios({
      method: "get",
      url: `${base_route}/${urljoin(routes.transactions)}`,
      data: {
          token: token,
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get personal purchase history due to ${err}`));

export const add_product_to_shop = (token, shop_id, info) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.shop, shop_id.toString(), routes.products)}`,
      data: {
          token: token,
          info:info
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to add product due to ${err}`));

export const delete_product = (token, shop_id, product_id) =>
    axios({
      method: "DELETE",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.products, product_id.toString())}`,
      data: {
          token: token,
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to delete product due to ${err}`));

export const appoint_shop_manager = (token, shop_id, username, permissions) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.promotions)}`,
      data: {
          token: token,
          username: username,
          permissions: permissions
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to appoint manager due to ${err}`));

export const appoint_shop_owner = (token, shop_id, username) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.owners)}`,
      data: {
          token: token,
          username: username
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to appoint shop owner due to ${err}`));

export const promote_shop_owner = (token, shop_id, username) =>
    axios({
      method: "POST",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.promotions)}`,
      data: {
          token: token,
          username: username
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to promote shop manager due to ${err}`));

export const edit_manager_permissions = (token, shop_id, username, permissions) =>
    axios({
      method: "PUT",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.managers)}`,
      data: {
          token: token,
          username: username,
          permissions: permissions
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to edit manager permissions due to ${err}`));

export const unappoint_manager = (token, shop_id, username) =>
    axios({
      method: "DELETE",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.managers)}`,
      data: {
          token: token,
          username: username
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to un appoint manager due to ${err}`));

export const unappoint_shop_owner = (token, shop_id, username) =>
    axios({
      method: "DELETE",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments, routes.owners)}`,
      data: {
          token: token,
          username: username
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to un appoint shop owner due to ${err}`));

export const get_shop_staff_info = (token, shop_id) =>
    axios({
      method: "GET",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments)}`,
      data: {
          token: token,
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shop staff info  due to ${err}`));

export const get_shop_transaction_history = (token, shop_id) =>
    axios({
      method: "GET",
      url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.transactions)}`,
      data: {
          token: token,
      }
    }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shop transaction history due to ${err}`));