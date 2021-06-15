// put here api calls.
const axios = require("axios");
const urljoin = require('url-join');

const host = "http://127.0.0.1"
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
  products: "products",
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
  purchase_policies: "purchase_policies",
  offers: "offers",
}

const base_route = `${host_port}/${routes.base}`;

export const isValidToken = (token) => {
  const url = `${base_route}/validate_token`;
  return axios({
    method: "get",
    url: url,
    params: {
      token: token
    }
  }).then((res) => {
    return res.data.is_valid
  })
  // .catch((err) => alert(`failed to enter the system due to ${err}`))
}

export const enter = () => {
  const url = `${base_route}/enter`;
  return axios({
    method: "post",
    url: url,
  }).then((res) => {
    if (res.data.status) {
      return res.data
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to enter the system due to ${err}`))
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
  }).catch((err) => alert(err))
}

export const login = (token, username, password) => {
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

export const search_products = (token, product_name, keywords, categories, filters) => {
  const url = `${base_route}/search`;
  return axios({
    url: url,
    method: "put",
    data: {
      token: token,
      product_name: product_name,
      keywords: keywords,
      categories: categories,
      filters: filters,
    },
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to search products due to ${err}`))
}

export const get_all_categories = (token) => {
  const url = `${base_route}/allCategories`;
  return axios({
    method: "get",
    url: url,
    params: {
      token: token
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`can't find all categories due to ${err}`))
};

export const get_user_transactions = (token) => {
  return axios({
    method: "get",
    url: `${base_route}/transactions`,
    params: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`can't find user transactions due to ${err}`));
}

export const get_product_info = (token, shop_id, product_id) => {
  const url = `${base_route}/shops/${shop_id}/products/${product_id}`;
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
  })
  .catch((err) => alert(`failed to get product info ${err}`))
}

export const get_permissions = (token, shop_id) => {
  const url = `${base_route}/permissions/${shop_id}`;
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
  }).catch((err) => alert(`failed to get user permissions due to ${err}`))
}

export const edit_product = (token, shop_id, product_id, name, price, description, categories, purchaseTypes) => {
  const url = `${base_route}/${routes.shops}/${shop_id}/${routes.products}/${product_id}`;
  return axios({
    method: "put",
    url: url,
    data: {
      token: token,
      product_name: name,
      price: price,
      description: description,
      categories: categories,
      purchase_types: purchaseTypes,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to edit product info due to ${err}`))
}

export const get_shop_transactions = (token, shop_id) => {
  return axios({
    method: "get",
    url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.transactions)}`,
    params: {
      token: token
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shop transactions due to ${err}`));
}

export const get_system_transactions = (token) => {
  return axios({
    method: "get",
    url: `${base_route}/${urljoin(routes.system, routes.transactions)}`,
    params: {
      token: token
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get system transactions due to ${err}`));
}

export const get_system_transactions_of_shops = (token, shop_id) => {
  return axios({
    method: "get",
    url: `${base_route}/${urljoin(routes.system, routes.transactions, routes.shops)}`,
    params: {
      token: token,
      shop_id: shop_id
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get system transactions of shop due to ${err}`));
}

export const get_system_transactions_of_user = (token, username) => {
  return axios({
    method: "get",
    url: `${base_route}/${urljoin(routes.system, routes.transactions, routes.user)}`,
    params: {
      token: token,
      username: username
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get system transactions of user due to ${err}`));
}

export const get_shop_info = (token, shop_id) => {
  return axios({
    method: "get",
    url: `${base_route}/${routes.shops}/${shop_id.toString()}`,
    params: {
      token: token
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shop info due to ${err}`));
}

export const get_all_shops_info = (token) => {
  return axios({
    method: "get",
    url: `${base_route}/${urljoin(routes.all_shops)}`,
    params: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get all shops info due to ${err}`))
}

export const get_all_shops_ids_and_names = (token) => {
  return axios({
    method: "get",
    url: `${base_route}/${urljoin(routes.all_shops_ids_and_names)}`,
    params: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shops ids and names due to ${err}`));
}

export const get_all_user_names = (token) => {
  return axios({
    method: "get",
    url: `${base_route}/${urljoin(routes.all_user_names)}`,
    params: {
      token: token,
    }
  }).then((res) => res.data)
}

const parsePaymentDetails = (paymentDetails) => ({
  card_number: paymentDetails.cardNumber,
  holder: paymentDetails.cardName,
  ccv: paymentDetails.cvv,
  month: paymentDetails.expDate.split('/')[0],
  year: paymentDetails.expDate.split('/')[1],
  id: paymentDetails.id
})

const parseDeilveryDetails = (deliveryDetails) => ({
  name: `${deliveryDetails.firstName} ${deliveryDetails.lastName}`,
  address: deliveryDetails.address,
  city: deliveryDetails.city,
  country: deliveryDetails.country,
  zip: deliveryDetails.zip,
})

export const purchase_product = (token, shop_id, product_id, amount, payment_details, delivery_details) => {
  return axios({
    method: "POST",
    url: `${base_route}/${urljoin(routes.cart, shop_id.toString(), product_id.toString())}`,
    data: {
      token: token,
      amount: amount,
      payment_details: parsePaymentDetails(payment_details),
      delivery_details: parseDeilveryDetails(delivery_details),

    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to purchase product due to ${err}`));
}

export const purchase_shopping_bag = (token, shop_id, payment_details, delivery_details) => {

  return axios({
    method: "POST",
    url: `${base_route}/${urljoin(routes.cart, shop_id.toString())}`,
    data: {
      token: token,
      payment_details: parsePaymentDetails(payment_details),
      delivery_details: parseDeilveryDetails(delivery_details),
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to purchase shopping bag due to ${err}`));
}

export const purchase_cart = (token, payment_details, delivery_details) => {

  return axios({
    method: "POST",
    url: `${base_route}/${urljoin(routes.cart)}`,
    data: {
      token: token,
      payment_details: parsePaymentDetails(payment_details),
      delivery_details: parseDeilveryDetails(delivery_details),
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to purchase cart due to ${err}`));
}

export const open_shop = (token, details) => {
  return axios({
    method: "POST",
    url: `${base_route}/${urljoin(routes.shops)}`,
    data: {
      token: token,
      ...details
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to open shop due to ${err}`));
}

export const add_product_to_shop = (token, shop_id, info) => {
  return axios({
    method: "POST",
    url: `${base_route}/${routes.shops}/${shop_id}/${routes.products}`,
    data: {
      token: token,
      ...info
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to add product due to ${err}`));
}

export const delete_product = (token, shop_id, product_id) => {
  const url =`${base_route}/${routes.shops}/${shop_id}/${routes.products}/${product_id}`
  alert(url);
  return axios({
    method: "DELETE",
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
  }).catch((err) => alert(`failed to delete product due to ${err}`));
}

export const appoint_shop_manager = (token, shop_id, username, permissions) => {
  return axios({
    method: "POST",
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
  }).catch((err) => alert(`failed to appoint manager due to ${err}`));
}

export const appoint_shop_owner = (token, shop_id, username) => {
  return axios({
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
}

export const promote_shop_owner = (token, shop_id, username) => {
  return axios({
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
}

export const edit_manager_permissions = (token, shop_id, username, permissions) => {
  return axios({
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
}

export const unappoint_manager = (token, shop_id, username) => {
  return axios({
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
}

export const unappoint_shop_owner = (token, shop_id, username) => {
  return axios({
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
}

export const get_shop_staff_info = (token, shop_id) => {
  return axios({
    method: "GET",
    url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.appointments)}`,
    params: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shop staff info due to ${err}`));
}

export const add_discount = (token, shop_id, has_cond, discount, condition) => {
  return axios({
    method: "POST",
    url: `${base_route}/${routes.shops}/${shop_id.toString()}/${routes.discounts}`,
    data: {
      token: token,
      has_cond: has_cond,
      discount: discount,
      condition: condition,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to add discount due to ${err}`));
}

export const move_discount_to = (token, shop_id, src_discount_id, dst_discount_id) => {
  return axios({
    method: "PUT",
    url: `${base_route}/${routes.shops}/${shop_id.toString()}/${routes.discounts}/${dst_discount_id}`,
    data: {
      token: token,
      src_discount_id: src_discount_id
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to move discount due to ${err}`));
}

export const remove_discount = (token, shop_id, discount_id) => {
  return axios({
    method: "DELETE",
    url: `${base_route}/${routes.shops}/${shop_id.toString()}/${routes.discounts}`,
    data: {
      token: token,
      discount_ids: [discount_id],
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to delete discount due to ${err}`));
}

export const get_shop_discounts = (token, shop_id) => {
  return axios({
    method: "GET",
    url: `${base_route}/${urljoin(routes.shops, shop_id.toString(), routes.discounts)}`,
    params: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shop discounts due to ${err}`));
}

export const get_appointments = (token) => {
  return axios({
    method: "GET",
    url: `${base_route}/appointments`,
    params: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get appointments due to ${err}`));
}

export const get_shop_policies = (token, shop_id) => {
  return axios({
    method: "GET",
    url: `${base_route}/${routes.shops}/${shop_id}/${routes.purchase_policies}`,
    params: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get shop purchase policies due to ${err}`));
}

export const add_policy = (token, shop_id, policy) => {
  return axios({
    method: "POST",
    url: `${base_route}/${routes.shops}/${shop_id}/${routes.purchase_policies}`,
    data: {
      token: token,
      ...policy
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to add purchase policy due to ${err}`));
}

export const remove_purchase_policy = (token, shop_id, policy_id) => {
  return axios({
    method: "DELETE",
    url: `${base_route}/${routes.shops}/${shop_id}/${routes.purchase_policies}/${policy_id}`,
    data: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to delete purchase policy due to ${err}`));
}

export const change_purchase_type = (token, shop_id, product_id, purchase_type_id, pt_args) => {
  return axios({
    method: "PUT",
    url: `${base_route}/${routes.cart}/${shop_id}/${product_id}`,
    data: {
      token: token,
      purchase_type_id: purchase_type_id,
      ...pt_args
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to change purchase type due to ${err}`));
}

export const make_offer = (token, shop_id, product_id, offer) => {
  return axios({
    method: "POST",
    url: `${base_route}/${routes.cart}/${shop_id}/${product_id}/offer`,
    data: {
      token: token,
      offer: offer,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to make price offer due to ${err}`));
}

export const get_offers = (token, shop_id, product_id) => {
  return axios({
    method: "GET",
    url: `${base_route}/${routes.shops}/${shop_id}/${product_id}/offers`,
    params: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get offers due to ${err}`));
}

export const reply_offer = (token, shop_id, product_id, offer_maker, action, additonal_params) => {
  return axios({
    method: "PUT",
    url: `${base_route}/${routes.shops}/${shop_id}/${product_id}/offers/${offer_maker}`,
    data: {
      token: token,
      action: action,
      ...additonal_params
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to ${action} offer by ${offer_maker} due to ${err}`));
}

export const get_user_purchase_offers = (token) => {
  return axios({
    method: "GET",
    url: `${base_route}/${routes.offers}`,
    params: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get purchase offers due to ${err}`));
}

export const accept_counter_offer = (token, shop_id, product_id) => {
  return axios({
    method: "PUT",
    url: `${base_route}/${routes.offers}/${product_id}`,
    data: {
      token: token,
      shop_id: shop_id,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to accept counter offer due to ${err}`));
}

export const delete_offer = (token, shop_id, product_id) => {
  return axios({
    method: "DELETE",
    url: `${base_route}/${routes.shops}/${shop_id}/${product_id}/${routes.offers}`,
    data: {
      token: token,
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.status
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to delete offer due to ${err}`));
}

export const get_stats = (token, actions, users, time_window) => {
  return axios({
    method: "POST",
    url: `${base_route}/stats/filtered`,
    data: {
      token,
      actions,
      users,
      time_window
    }
  }).then((res) => {
    if (res.data.status) {
      return res.data.result
    } else {
      throw new Error(res.data.description)
    }
  }).catch((err) => alert(`failed to get system stats due to ${err}`));
}