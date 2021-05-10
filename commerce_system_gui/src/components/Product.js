import {useEffect, useState} from "react";
import {delete_product, edit_product, get_permissions, get_product_info, save_product_to_cart} from "../api";
import React from "react";
import {
  useParams, Link as RouteLink
} from "react-router-dom";
import {useAuth} from "./use-auth";
import Button from "@material-ui/core/Button";
import {makeStyles} from '@material-ui/core/styles';
import {Paper, TextField} from "@material-ui/core";
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
