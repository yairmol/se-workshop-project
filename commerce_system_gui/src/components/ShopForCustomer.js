import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import React, {useCallback, useEffect, useState} from "react";
import Grid from "@material-ui/core/Grid";
import {useAuth} from "./use-auth";
import {get_shop_info, save_product_to_cart} from "../api";
import Products from './CustomerPageProducts'
import {useParams} from "react-router-dom";
import BuyProductPopup from "./PopUps/BuyProductPopup";

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
    },
    heading: {
        fontSize: theme.typography.pxToRem(50),
        flexBasis: '33.33%',
        flexShrink: 0,
        padding:5
    },
    secondaryHeading: {
        fontSize: theme.typography.pxToRem(30),
        color: theme.palette.text.secondary,
        padding:10,
        paddingBottom:40
    },
    info: {
        fontSize: theme.typography.pxToRem(15),

    },
    accordion: {
        flexGrow: 1
    },
    paper: {
        padding: theme.spacing(3),
        display: 'flex',
        overflow: 'auto',
        flexDirection: 'column',
    },
    grid_window: {
        width: '600px'
    },
}));

export const ShopForCustomer = () => {
  const {shop_id} = useParams()
  const classes = useStyles()

  const auth = useAuth();
  const [load, setLoad] = useState(true);
  const [shop_info, set_shop_info] = useState({products: [], "shop_name":"", "description":""})

  const [open_buy, set_open_buy] = useState(false)
  const [b_product, set_buy_product] = useState({})

  const open_buy_window = (product) => {
    set_buy_product(b_product)
    set_open_buy(true)
  }

  const load_customers = useCallback(() =>
    auth.getToken().then((token) =>
      get_shop_info(token, shop_id).then((res) => {
        set_shop_info(res)
      })
    )
  , [auth, shop_id])

  const buy_product = async (product, amount) => {
    auth.getToken().then((token) =>{
      save_product_to_cart(token, shop_id, product.product_id, amount).then(_ => {
        load_customers().then(_ => set_open_buy(false))
      })
    })
  }

  useEffect(() => {
    if (load) {
      load_customers().then((_) => {
        setLoad(false);
      })
    }
  }, [load, load_customers])

  return (
      <div className={classes.root}>
        <Grid container spacing={5} direction="column">
          <Typography className={classes.heading}>{shop_info.shop_name}</Typography>
          <Typography className={classes.secondaryHeading}>{shop_info.description}</Typography>
          <Grid container spacing={2}>
            <Grid item className="Grid">
              <div className={classes.grid_window}><Products
                  buy_product_popup={open_buy_window}
                  products={shop_info.products}/></div>
            </Grid>
          </Grid>
        </Grid>
        { open_buy ? <BuyProductPopup add_to_cart_func={buy_product} product={b_product}/> : [] }
      </div>
  );
};

