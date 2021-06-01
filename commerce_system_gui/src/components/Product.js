import {useEffect, useState} from "react";
import {
  delete_product,
  edit_product,
  get_permissions,
  get_product_info,
  make_offer,
  save_product_to_cart
} from "../api";
import React from "react";
import {
  useParams, Link as RouteLink
} from "react-router-dom";
import {useAuth} from "./use-auth";
import Button from "@material-ui/core/Button";
import {makeStyles} from '@material-ui/core/styles';
import {
  Checkbox,
  Dialog, DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  FormGroup,
  InputAdornment,
  Paper,
  TextField
} from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";


const useStyles = makeStyles((theme) => ({
  root: {
    maxWidth: 2000,
  },
  media: {
    height: 500,
  },
  paper: {
    margin: theme.spacing(2),
    padding: theme.spacing(2),
  }
}));


const OfferPriceDialog = ({shopId, product, close}) => {
  const [price, setPrice] = useState(0);
  const auth = useAuth();

  const onSubmit = () => {
    auth.getToken().then((token) => make_offer(token, shopId, product.product_id, price)).then((res) => {
      if (res) {
        alert('offer successfully made')
      }
    })
    close()
  }

  return (<div>
      <Dialog
        open={true}
        onClose={close}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          Offer Price for Product {product.product_name}
        </DialogTitle>
        <DialogContent>
        <form autoComplete="off">
            <TextField autoFocus margin="dense" id="price" label="Offered Price" fullWidth value={price}
                       onChange={(e) => setPrice(parseInt(e.target.value))} />
        </form>
        </DialogContent>
        <DialogActions>
          <Button onClick={onSubmit} color="primary">
            Done
          </Button>
          <Button onClick={close} color="primary">
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}


export const Product = ({shop_name}) => {
  const classes = useStyles();
  const auth = useAuth()

  const [product, setProduct] = useState(false);
  let {shop_id, product_id} = useParams();

  // const [permissions, setPermissions] = useState(false);
  const [name, setName] = useState(product.product_name);
  const [price, setPrice] = useState(product.price);
  const [loaded, setLoaded] = useState(false);
  const [description, setDescription] = useState(product.description);
  const [categories, setCategories] = useState(product.categories);
  const [purchaseTypeDialogOpen, setPTDOpen] = useState(false);

  const purchaseTypes = {
    'offer': {label: 'Make Offer', action: () => setPTDOpen(true)},
    'buy_now': {label: 'Buy Now', action: () => {}},
  }

  useEffect(async () => {
    if (!loaded) {
      if (!product) {
        await get_product_info(await auth.getToken(), shop_id, product_id).then((res) => {
          setProduct(res)
        });
      }
      // if (!permissions) {
      //   await get_permissions(await auth.getToken(), shop_id).then((res) => {
      //     setPermissions(res)
      //   });
      // }
      setLoaded(true);
    }
  })


  const onSubmitEdit = async (e) => {
    e.preventDefault()
    // WHAT TO DO WITH then.. ?
    edit_product(await auth.getToken(), shop_id, product_id, name, price, description, categories)
      .then((res) => res.status ? alert("edit product successfully") : alert(res.description))

  }
  const onSubmitDelete = async (e) => {
    e.preventDefault()
    await delete_product(await auth.getToken, shop_id, product_id)
  }

  const onSubmitBuy = (e) => {
    e.preventDefault()
    auth.getToken().then((token) => {
      save_product_to_cart(token, shop_id, product_id, 1).then((res) => {
        if (res) {
          alert("product was successfully added to cart")
        }
      })
    })
  }

  const onPurchaseTypeClick = (pt) => {
    purchaseTypes[pt].action()
  }


  return (loaded &&
    <form>
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
              {/*  <Grid item>*/}
              {/*    <Grid container direction="row">*/}
              {/*      {permissions.edit ? <Button onClick={onSubmitEdit} variant="outlined" color="primary">*/}
              {/*        Edit Product </Button> : <> </>}*/}
              {/*      {permissions.delete ? <Button onClick={onSubmitDelete} variant="outlined" color="primary" href="/">*/}
              {/*        Delete Product </Button> : <> </>}*/}
              {/*    </Grid>*/}
              {/*  </Grid>*/}
            </Grid>
          </Grid>
        </Grid>
      </Paper>
    </form>);

}
// <Card className={classes.root}>
//   <CardActionArea>
//     {/*<CardMedia*/}
//     {/*  className={classes.media}*/
//     }
//     {/*  image="/static/images/cards/contemplative-reptile.jpg"*/
//     }
//     {/*  title="Contemplative Reptile"*/
//     }
//     {/*/>*/
//     }
//   </CardActionArea>
//   <CardContent>
//     <Typography gutterBottom variant="h2" component="h1">
//       {
//         product.product_name
//       }
//       -{shop_name}
//     </Typography>
//     <Typography variant="body1" color="textSecondary" component="p">
//       <table>
//         <tr>
//           <td>Price:
//             {
//               product.price
//             }
//           </td>
//           <td><TextField id="standard-basic" label="New Price"/></td>
//         </tr>
//         <tr>
//           <td>Description:
//             {
//               product.description
//             }
//           </td>
//           <td><TextField id="standard-basic" label="New Description"/></td>
//         </tr>
//         <tr>
//           <td>Categories:
//             {
//               product.categories
//             }
//           </td>
//           <td><TextField id="standard-basic" label="New Categories"/></td>
//         </tr>
//       </table>
//     </Typography>
//   </CardContent>
//
//   {/* For Regular User */
//   }
//   <CardActions>
//     <Button variant="contained" color="primary" href="purchase_product/${product_id}">
//       Buy Now
//     </Button>
//   </CardActions>
//   {/* For Owner/Manager */}
//   <CardActions>
//     {permissions.edit ? <Button onClick={onSubmitEdit} variant="contained" color="primary" href="purchase_product/${product_id}">
//       Edit Product
//     </Button> : <> </>}
//     {permissions.delete ? <Button onClick={onSubmitDelete} variant="contained" color="primary" href="purchase_product/${product_id}">
//       Delete Product
//     </Button> : <> </>}
//   </CardActions>
// </Card>
