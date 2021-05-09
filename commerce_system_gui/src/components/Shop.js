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
import {useEffect, useState} from "react";
import Grid from "@material-ui/core/Grid";
import {useAuth} from "./use-auth";
import {get_cart_info, get_permissions, get_shop_info, get_shop_staff_info} from "../api";
import {ShopWorkers} from "./ShopWorkers";
import {ShopTransactions} from "./Transactions";
import ShopProducts from './ShopProducts'
import Button from "@material-ui/core/Button";
import EditWorkerPermissions from "./PopUps/EditPermissionsPopup";
import RemoveAppontment from "./PopUps/RemoveAppointmentPopup";
import RemoveAppointmentPopup from "./PopUps/RemoveAppointmentPopup";
import RemoveProductPopup from "./PopUps/RemoveProductPopup";
import EditProductPopup from "./PopUps/EditProductPopup";
import AddProductPopup from "./PopUps/AddProductPopup";
import AddAppointmentPopup from "./PopUps/AddApointmentPopup";

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

export const Shop = ({shop_id}) => {
  const classes = useStyles();
  const [load, set_load] = useState(true)
  const [shop_info, set_info] = useState([])
  const [worker_permissions, set_perms] = useState({'edit': false, 'delete': true})

  // for editing manager permissions
  const [shop_worker_for_perms, set_worker_for_perms] = useState([])
  const [open_edit_permissions, set_edit_perms] = useState(false)
  const open_edit_perms_window = (worker) => {
    set_worker_for_perms(worker)
    set_edit_perms(true)
  }

  //for removing appointment
  const [shop_worker_for_remove_app, set_worker_for_remove_app] = useState([])
  const [open_remove_app, set_remove_app] = useState(false)
  const open_remove_app_window = (worker) => {
    set_worker_for_remove_app(worker)
    set_remove_app(true)
  }

  // for removing product
  const [product_for_remove, set_product_for_remove] = useState([])
  const [open_remove_product, set_remove_product] = useState(false)
  const open_remove_product_window = (product) => {
    set_product_for_remove(product)
    set_remove_product(true)
  }

  // for editing product
  const [product_for_edit, set_product_for_edit] = useState([])
  const [open_edit_product, set_edit_product] = useState(false)
  const open_edit_product_window = (product) => {
    set_product_for_edit(product)
    set_edit_product(true)
  }

  // for add product
  const [open_add_product, set_add_product] = useState(false)

  // for add appointment
  const [open_add_appointment, set_add_appointment] = useState(false)

  const auth = useAuth();
  const username = "yossi" // = auth.user;
  useEffect(async () => {
      if (load) {
        await auth.getToken().then((token) => {
          get_shop_info(token, shop_id).then((info) => {
            set_info(info)
          }).then((res) =>
          get_permissions(token)).then((permissions) =>
          set_perms(permissions))
        })
      }
      set_load(false)
    }, [])

  return (
      <div className={classes.root}>
        <Grid container spacing={5} direction="column">
          <Typography className={classes.heading}>{shop_info.shop_name}</Typography>
          <Typography className={classes.secondaryHeading}>{shop_info.description}</Typography>
          <Grid container spacing={2}>
            <Grid item className="Grid">
              <div className={classes.grid_window}><ShopProducts
                  permissions={worker_permissions}
                  remove_product_func={open_remove_product_window}
                  add_product_func={() => {set_add_product(true)}}
                  edit_product_func={open_edit_product_window}
                  products={shop_info.products}/></div>
            </Grid>
            <Grid item className="Grid">
              <div className={classes.grid_window}><ShopWorkers
                  add_appointment_func={() => {set_add_appointment(true)}}
                  remove_appointment_func={open_remove_app_window}
                  edit_permissions_func={open_edit_perms_window}
                  user={username}
                  shop_id={shop_id}/></div>
            </Grid>
            <Grid item className="Grid" >
              <div className={classes.grid_window}><ShopTransactions shop_id={shop_id}/></div>
            </Grid>
          </Grid>
        </Grid>
        {open_edit_permissions ?
            (<EditWorkerPermissions
                worker={shop_worker_for_perms}
                close_window_func={() => {set_edit_perms(false)}} />)
            : []}
        {open_remove_app ?
            (<RemoveAppointmentPopup
                worker={shop_worker_for_remove_app}
                close_window_func={() => {set_remove_app(false)}} />)
            : []}
        {open_remove_product ?
            (<RemoveProductPopup
                product={product_for_remove}
                close_window_func={() => {set_remove_product(false)}} />)
            : []}
        {open_edit_product ?
            (<EditProductPopup
                product={product_for_edit}
                close_window_func={() => {set_edit_product(false)}} />)
            : []}
        {open_add_product ?
            (<AddProductPopup
                close_window_func={() => {set_add_product(false)}} />)
            : []}
        {open_add_appointment ?
            (<AddAppointmentPopup
                shop_id={shop_info.shop_id}
                close_window_func={() => {set_add_appointment(false)}} />)
            : []}
      </div>
  );
};
