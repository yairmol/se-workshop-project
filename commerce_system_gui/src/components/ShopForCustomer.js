import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Card, Checkbox, CircularProgress, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle,
  Divider, FormControlLabel, FormGroup,
  Link,
  List,
  ListItem,
  Paper
} from "@material-ui/core";
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import React, {useEffect, useState} from "react";
import Grid from "@material-ui/core/Grid";
import {useAuth} from "./use-auth";
import {
  add_product_to_shop,
  appoint_shop_manager,
  appoint_shop_owner,
  delete_product, edit_manager_permissions,
  edit_product,
  get_cart_info,
  get_permissions,
  get_shop_info,
  get_shop_staff_info, promote_shop_owner, save_product_to_cart,
  unappoint_manager, unappoint_shop_owner
} from "../api";
import {ShopWorkers} from "./ShopWorkers";
import {ShopTransactions} from "./Transactions";
import Products from './CustomerPageProducts'
import Button from "@material-ui/core/Button";
import EditWorkerPermissions from "./PopUps/EditPermissionsPopup";
import RemoveAppontment from "./PopUps/RemoveAppointmentPopup";
import RemoveAppointmentPopup from "./PopUps/RemoveAppointmentPopup";
import RemoveProductPopup from "./PopUps/RemoveProductPopup";
import EditProductPopup from "./PopUps/EditProductPopup";
import AddProductPopup from "./PopUps/AddProductPopup";
import AddAppointmentPopup from "./PopUps/AddApointmentPopup";
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

  const load_customers = async () => {
    auth.getToken().then((token) =>{
      get_shop_info(token, shop_id).then((res) => {
        set_shop_info(res)
      })
    })
  }

  const buy_product = async (product, amount) => {
    auth.getToken().then((token) =>{
      save_product_to_cart(token, shop_id, product.product_id, amount).then(_ => {
        load_customers().then(_ => set_open_buy(false))
      })
    })
  }

  useEffect(async () =>{
    if (load) {
      await load_customers()
    }
    setLoad(false);
  })

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

