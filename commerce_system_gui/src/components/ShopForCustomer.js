import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import React, {useCallback, useEffect, useState} from "react";
import Grid from "@material-ui/core/Grid";
import {useAuth} from "./use-auth";
import {get_product_info, get_shop_info, save_product_to_cart} from "../api";
import {useParams} from "react-router-dom";
import {Paper} from "@material-ui/core";
import Button from "@material-ui/core/Button";
import {OfferPriceDialog} from "./Product"

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


const Product = ({product, shop_id}) => {
  const classes = useStyles();
  const auth = useAuth()

  const [purchaseTypeDialogOpen, setPTDOpen] = useState(false);
  // alert(JSON.stringify(product))
  const purchaseTypes = {
    'offer': {label: 'Make Offer', action: () => setPTDOpen(true)},
    'buy_now': {label: 'Buy Now', action: () => {}},
  }

  const onPurchaseTypeClick = (pt) => {
    purchaseTypes[pt].action()
  }

  const onSubmitBuy = (e) => {
    e.preventDefault()
    auth.getToken().then((token) => {
      save_product_to_cart(token, shop_id, product.product_id, 1).then((res) => {
        if (res) {
          alert("product was successfully added to cart")
        }
      })
    })
  }


  return (
      <Paper className={classes.paper}>
        <Grid container justify="center">
          <Grid item xs={12}>
            <Grid container justify="center" direction="column" spacing={3}>
              <Grid item><Typography>Product name: {product.product_name}</Typography></Grid>
              <Grid item><Typography>Price: {product.price}</Typography></Grid>
              <Grid item><Typography>Description: {product.description}</Typography></Grid>
              <Grid item><Typography>Categories: {product.categories}</Typography></Grid>
              <Grid item><Button onClick={onSubmitBuy} variant="outlined" color="primary">Add to Cart</Button></Grid>
              {product.purchase_types
                .filter((pt) => !pt.for_subs_only || auth.user)
                .map((pt) =>
                  <Grid item>
                    <Button onClick={(e) => onPurchaseTypeClick(pt.purchase_type)}
                            name={pt.purchase_type} variant="outlined" color="primary">
                      {purchaseTypes[pt.purchase_type].label}
                    </Button>
                  </Grid>)
              }
              {purchaseTypeDialogOpen &&
              <OfferPriceDialog shopId={shop_id} product={product} close={(e) => setPTDOpen(false)}/>}
            </Grid>
          </Grid>
        </Grid>
      </Paper>);
}

export const ShopForCustomer = () => {
  const {shop_id} = useParams()
  const classes = useStyles()

  const auth = useAuth();
  const [load, setLoad] = useState(true);
  const [shop_info, set_shop_info] = useState({products: [], "shop_name":"", "description":""})

  const load_customers = useCallback(() =>
    auth.getToken().then((token) =>
      get_shop_info(token, shop_id).then((res) => {
        set_shop_info(res)
      })
    )
  , [auth, shop_id])

  useEffect(() => {
    if (load) {
      load_customers().then((_) => {
        setLoad(false);
      })
    }
  }, [load, load_customers])

  return (!load &&
      <div className={classes.root}>
        <Grid container spacing={5} direction="column">
          <Typography className={classes.heading}>{shop_info.shop_name}</Typography>
          <Typography className={classes.secondaryHeading}>{shop_info.description}</Typography>
          <Grid container spacing={2}>
            <Grid item className="Grid">
              {shop_info.products.map((product) =>
                <Product product={product} shop_id={shop_id}/>
              )}
            </Grid>
          </Grid>
        </Grid>
      </div>
  );
};

