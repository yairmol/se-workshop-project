import {Fab, Paper, Typography} from "@material-ui/core";
import React, {useState} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import {edit_product, add_product_to_shop, delete_product} from "../api";
import AddIcon from '@material-ui/icons/Add';
import ShopProduct from "./ShopProduct";
import RemoveProductPopup from "./PopUps/RemoveProductPopup";
import EditProductPopup from "./PopUps/EditProductPopup";
import AddProductPopup from "./PopUps/AddProductPopup";
import OffersPopup from "./PopUps/OffersPopup";

const useStyles = makeStyles((theme) => ({
  mainFeaturedPost: {
    position: 'relative',
    // backgroundColor: theme.palette.grey[800],
    // color: theme.palette.common.white,
    marginBottom: theme.spacing(4),
    // backgroundImage: 'url(https://source.unsplash.com/random)',
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
    width: "100%",
  },
  overlay: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    right: 0,
    left: 0,
    // backgroundColor: 'rgba(0,0,0,.3)',
  },
  empty_msg: {
    fontSize: theme.typography.pxToRem(30),
    color: theme.palette.text.secondary,
    padding: 50,
  },
  mainFeaturedPostContent: {
    position: 'relative',
    padding: theme.spacing(3),
    [theme.breakpoints.up('md')]: {
      padding: theme.spacing(6),
      paddingRight: 0,
    },
  },
  heading: {
    fontSize: theme.typography.pxToRem(20),
    flexBasis: '33.33%',
    flexShrink: 0,
    fontWeight: 530,
    padding: theme.spacing(1)
  },
}))

export default function Products({shop_id, products, auth, permissions, reload}) {

  // for add product
  const [open_add_product, set_add_product] = useState(false)
  const open_add_product_window = () => {
    set_add_product(true)
  }
  // for editing product
  const [product_for_edit, set_product_for_edit] = useState([])
  const [open_edit_product, set_edit_product] = useState(false)
  const open_edit_product_window = (product) => {
    set_product_for_edit(product)
    set_edit_product(true)
  }

  const [product_for_offer, set_product_for_offer] = useState([])
  const [open_offers, set_manage_offers] = useState(false)
  const open_manage_offers = (product) => {
    set_product_for_offer(product)
    set_manage_offers(true)
  }

  // for removing product
  const [product_for_remove, set_product_for_remove] = useState([])
  const [open_remove_product, set_remove_product] = useState(false)
  const open_remove_product_window = (product) => {
    set_product_for_remove(product)
    set_remove_product(true)
  }

  const edit_product_func = (product_id, name, price, description, categories, purchaseTypes) => {
    auth.getToken().then((token) =>
      edit_product(token, shop_id, product_id, name, price, description, categories, purchaseTypes).then((res) =>
        reload().then(_ => {
            if (res) {
              alert("Successfully Edited Product (product id = " + product_id + ")")
            }
          }
        )))
  }

  const add_product_func = (name, price, quantity, description, categories) => {
    const product_info = {product_name: name, price: price, quantity: quantity, description: description, categories: categories}
    auth.getToken().then(token =>
      add_product_to_shop(token, shop_id, product_info).then((res) =>
        reload().then(_ => {
            if (res) {
              alert("Successfully Added Product (product id = " + res + ")")
            }
          }
        )))
  }

  const remove_product_func = (product_id) => {
    auth.getToken().then((token) =>
      delete_product(token, shop_id, product_id).then((res) =>
        reload().then(_ => {
          if (res) {
            alert("Successfully Deleted Product (product id = " + product_id + ")")
          }
        })
      )
    )
  }

  const classes = useStyles();
  return (
    <>
      <Grid item lg={6}>
        <Typography className={classes.heading}>Products &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
          <Fab color="primary" onClick={open_add_product_window}
               aria-label="add" style={{height: '15px', width: '35px'}}>
            <AddIcon/>
          </Fab>
        </Typography>
        {(products && products.length > 0) ?
          products.map((product, index) => <div style={{width: '200%'}}>
            <ShopProduct
              permissions={permissions}
              edit_product_func={open_edit_product_window}
              remove_product_func={open_remove_product_window}
              manage_offers_func={open_manage_offers}
              key={index} product={product}/></div>)
          : <Paper><Typography className={classes.empty_msg}/>Shop has no products</Paper>
        }
      </Grid>
      {open_remove_product ?
        (<RemoveProductPopup
          product={product_for_remove}
          close_window_func={() => {
            set_remove_product(false)
          }}
          remove_product_func={remove_product_func}
        />)
        : []}
      {open_edit_product ?
        (<EditProductPopup
          product={product_for_edit}
          close_window_func={() => {
            set_edit_product(false)
          }}
          edit_product_func={edit_product_func}
        />)
        : []}
      {open_add_product ?
        (<AddProductPopup
          close_window_func={() => {
            set_add_product(false)
          }}
          add_product_func={add_product_func}
        />)
        : []}
      {open_offers &&
        <OffersPopup close={() => {set_manage_offers(false)}} shopId={shop_id} product={product_for_offer}/>}
    </>
  );
}

