import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import {useCallback, useEffect, useState} from "react";
import Grid from "@material-ui/core/Grid";
import {useAuth} from "./use-auth";
import {
  get_permissions,
  get_shop_info,
} from "../api";
import {ShopWorkers} from "./ShopWorkers";
import {ShopTransactions} from "./Transactions";
import ShopProducts from './ShopProducts'
import Button from "@material-ui/core/Button";
import {useParams, Link as RouteLink} from "react-router-dom";


const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(50),
    flexBasis: '33.33%',
    flexShrink: 0,
    padding: 5
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(30),
    color: theme.palette.text.secondary,
    padding: 10,
    paddingBottom: 40
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
  const [worker_permissions, set_perms] = useState({'edit_product': false, 'delete_product': true})
  const auth = useAuth();

  const load_perms_func = useCallback(() => {
    return auth.getToken().then(async (token) => {
      return await get_permissions(token, shop_id).then((permissions) => {
        set_perms(permissions)
        return permissions
      })
    })
  }, [auth, shop_id])

  const load_info_func = useCallback(() =>
    auth.getToken().then((token) => {
      get_shop_info(token, shop_id).then((info) => {
        set_info(info)
        return info
      })
    })
  , [auth, shop_id])

  useEffect(() => {
    if (load_perms) {
      load_perms_func().then((perms) => {
        if (perms) {
          if (load_shop_info_bool) {
            load_info_func().then(_ => {
              set_load_info(false);
              set_load_perms(false);
            });
          }
        }
      })
    }
  }, [load_info_func, load_perms, load_perms_func, load_shop_info_bool])

  return (!load_perms ?
    <div className={classes.root}>
      <Grid container spacing={5} direction="column">
        <Typography className={classes.heading}>{shop_info.shop_name}</Typography>
        <Typography className={classes.secondaryHeading}>{shop_info.description}</Typography>
        <Grid container spacing={2}>
          <Grid item className="Grid">
            <div className={classes.grid_window}>
              <ShopProducts
                shop_id={shop_info.shop_id}
                products={shop_info.products}
                auth={auth}
                permissions={worker_permissions}
                reload={load_info_func}/></div>
          </Grid>
          <Grid item className="Grid">
            <div className={classes.grid_window}>
              {worker_permissions.watch_staff ?
                <ShopWorkers
                  shop_id={shop_id}
                  auth={auth}/> :
                <Typography>You don't have permissions to watch shop staff</Typography>
              }
            </div>
          </Grid>
          <Grid item className="Grid">
            {worker_permissions.watch_transactions ?
              <div className={classes.grid_window}>
                <ShopTransactions shop_id={shop_id}/>
              </div> :
              <Typography>You don't have Permission to watch the shop transactions</Typography>
            }
          </Grid>
          <Grid item className="Grid">
            {worker_permissions.manage_discounts ?
              <RouteLink to={{pathname: `/shops/${shop_id}/discounts`, header: "Discount Manager"}}>
                <Button variant="outlined" size="small" color="primary" fullWidth>
                  Manage Discounts
                </Button>
              </RouteLink> :
              <Typography>You don't have permission to manage discounts</Typography>
            }
          </Grid>
          <Grid item className="Grid">
            {worker_permissions.manage_purchase_condition ?
              <RouteLink to={{pathname: `/shops/${shop_id}/purchase_policies`, header: "Purchase Policies Manager"}}>
                <Button variant="outlined" size="small" color="primary" fullWidth>
                  Manage Purchase Policies
                </Button>
              </RouteLink> :
              <Typography>You don't have permission to manage purchase policies</Typography>
            }
          </Grid>
        </Grid>
      </Grid>
    </div> : <Typography>Loading...</Typography>
  );
};
