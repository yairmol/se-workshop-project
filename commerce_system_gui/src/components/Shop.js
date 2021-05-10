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
import {
  add_product_to_shop,
  appoint_shop_manager,
  appoint_shop_owner,
  delete_product, edit_manager_permissions,
  edit_product,
  get_cart_info,
  get_permissions,
  get_shop_info,
  get_shop_staff_info, promote_shop_owner,
  unappoint_manager, unappoint_shop_owner
} from "../api";
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
import {useParams} from "react-router-dom";

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

export const Shop = () => {
  const {shop_id} = useParams()
  const classes = useStyles();
  const [load_shop_info_bool, set_load_info] = useState(true)
  const [load_perms, set_load_perms] = useState(true)
  const [shop_info, set_info] = useState([])
  const [worker_permissions, set_perms] = useState({'edit': false, 'delete': true})

  const [load_workers_bool, set_load_workers] = useState(true)
  const [workers, set_workers] = useState([])

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

  const load_info_func = async () => {
    await auth.getToken().then((token) => {
        get_shop_info(token, shop_id).then((info) => {
          set_info(info)
        })
      })
  }

  useEffect(async () => {
    if (load_shop_info_bool) {
      await load_info_func()
    }
    set_load_info(false)
  }, [])

  const load_perms_func = async () => {
    await auth.getToken().then((token) =>
              get_permissions(token)).then((permissions) =>
              set_perms(permissions))
  }

  useEffect(async () => {
      if (load_perms) {
          await load_perms_func()
      }
      set_load_perms(false)
  }, [])

  const load_workers_func = async () => {
    await auth.getToken().then((token) => {
              get_shop_staff_info(token, shop_id).then((staff_info) => {
                  set_workers(staff_info)
              })
          })
  }

  useEffect(async () => {
      if (load_workers_bool) {
        await load_workers_func()
      }
      set_load_workers(false)
  }, [])

  const edit_product_func = (product_id, name, price, description, categories) => {
     auth.getToken().then(token =>
         edit_product(token, shop_info.shop_id, product_id, name, price, description, categories).then(_ =>
             load_info_func().then(_ =>
                alert("Successfully Edited Product (product id = " + product_id + ")")
             )))
  }

  const add_product_func = (product_id, name, price, description, categories) => {
     auth.getToken().then(token =>
         add_product_to_shop(token, shop_info.shop_id, product_id, name, price, description, categories).then(_ =>
             load_info_func().then(_ =>
                alert("Successfully Added Product (product id = " + product_id + ")")
             )))
  }

  const remove_product_func = (product_id) => {
    auth.getToken().then(token =>
        delete_product(token, shop_info.shop_id, product_id).then(_ =>
            load_info_func().then(_ =>
                alert("Successfully Deleted Product (product id = " + product_id + ")")
            )))
  }

  const promote_manager = (username) => {
    auth.getToken().then(token =>
        promote_shop_owner(token, shop_info.shop_id, username).then(_ =>
            load_info_func().then(_ =>
                alert("Successfully Promoted Manager " + username)
            )))
  }

  const edit_perms_func = (username, permissions) => {
      auth.getToken().then(token =>
       edit_manager_permissions(token, shop_info.shop_id, username, permissions).then(_ =>
           load_workers_func().then(_ =>
              alert("Successfully Edited Permissions Of Manager " + username)
           )))
  }

  const unappoint_owner_func = (username) => {
      auth.getToken().then(token =>
       unappoint_shop_owner(token, shop_info.shop_id, username).then(_ =>
           load_workers_func().then(_ =>
              alert("Successfully Unappointed Owner " + username)
           )))
  }

  const unappoint_manager_func = (username) => {
      auth.getToken().then(token =>
       unappoint_manager(token, shop_info.shop_id, username).then(_ =>
           load_workers_func().then(_ =>
              alert("Successfully Unappointed Manager " + username)
           )))
  }

  const appoint_owner_func = (username) => {
      auth.getToken().then(token =>
       appoint_shop_owner(token, shop_info.shop_id, username).then(_ =>
           load_workers_func().then(_ =>
              alert("Successfully Appointed Owner " + username)
           )))
  }

  const appoint_manager_func = (username, permissions) => {
      auth.getToken().then(token =>
       appoint_shop_manager(token, shop_info.shop_id, username, permissions).then(_ =>
           load_workers_func().then(_ =>
              alert("Successfully Unappointed Manager " + username)
           )))
  }

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
                  workers={workers}
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
                close_window_func={() => {
                  set_edit_perms(false)
                  }}
                edit_perms_func={edit_perms_func}
                promote_manager={promote_manager}
            />)
            : []}
        {open_remove_app ?
            (<RemoveAppointmentPopup
                worker={shop_worker_for_remove_app}
                close_window_func={() => {
                  set_remove_app(false)
                  }}
                unappoint_manager_func={unappoint_manager_func}
                unappoint_owner_func={unappoint_owner_func}
                  />)
            : []}
        {open_remove_product ?
            (<RemoveProductPopup
                product={product_for_remove}
                close_window_func={() => {
                  set_remove_app(false)
                  }}
                remove_product_func={remove_product_func}
                  />)
            : []}
        {open_edit_product ?
            (<EditProductPopup
                product={product_for_edit}
                close_window_func={() => {
                  set_remove_app(false)
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
        {open_add_appointment ?
            (<AddAppointmentPopup
                shop_id={shop_info.shop_id}
                close_window_func={() => {
                  set_add_appointment(false)
                  }}
                appoint_owner_func={appoint_owner_func}
                appoint_manager_func={appoint_manager_func}
            />)
            : []}
      </div>
  );
};
